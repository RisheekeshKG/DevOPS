"""Kafka producer/consumer helpers and risk labeling."""

import json
import logging
import os
import time
from typing import Dict

import joblib
import numpy as np

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not found. ModelRiskPredictor will operate in Rule-based Fallback mode.")

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable


if TORCH_AVAILABLE:
    class DNN(nn.Module):
        """DNN architecture used during training."""

        def __init__(self, input_size: int, hidden_size: int, output_size: int):
            super().__init__()
            self.fc1 = nn.Linear(input_size, hidden_size)
            self.relu = nn.ReLU()
            self.fc2 = nn.Linear(hidden_size, hidden_size)
            self.fc3 = nn.Linear(hidden_size, output_size)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            out = self.fc1(x)
            out = self.relu(out)
            out = self.fc2(out)
            out = self.relu(out)
            out = self.fc3(out)
            return out
else:
    # Minimal stub if torch is missing
    class DNN:
        def __init__(self, *args, **kwargs): pass


class RiskLabeler:
    """Labels incoming readings with low/medium/high risk."""

    @staticmethod
    def score(reading: Dict[str, object]) -> float:
        risk = 0.0
        hr = float(reading.get("hr", 72))
        spo2 = float(reading.get("spo2", 98))
        temp = float(reading.get("temp", 37.0))
        bp_sys = float(reading.get("bp_sys", 112))
        bp_dia = float(reading.get("bp_dia", 72))

        if hr < 50 or hr > 120:
            risk += 0.25
        elif hr < 60 or hr > 100:
            risk += 0.10

        if spo2 < 90:
            risk += 0.35
        elif spo2 < 95:
            risk += 0.15

        if temp < 36.0 or temp > 38.5:
            risk += 0.20
        elif temp < 36.5 or temp > 38.0:
            risk += 0.10

        if bp_sys < 80 or bp_sys > 160 or bp_dia < 50 or bp_dia > 100:
            risk += 0.20

        return min(1.0, risk)

    @staticmethod
    def label(score: float) -> str:
        if score > 0.70:
            return "high"
        if score >= 0.35:
            return "medium"
        return "low"


class ModelRiskPredictor:
    """Loads trained artifacts (.pth/.pkl) and predicts risk from live readings."""

    def __init__(
        self,
        model_path: str,
        scaler_path: str,
        label_encoder_path: str,
        hidden_size: int = 128,
    ):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.label_encoder_path = label_encoder_path
        self.hidden_size = hidden_size
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        if not TORCH_AVAILABLE:
            logger.info("Torch unavailable — skipping artifact load. ModelRiskPredictor will use RiskLabeler rules.")
            return

        if not os.path.exists(self.model_path):
            logger.warning("Model file not found: %s. Falling back to rules.", self.model_path)
            return
        if not os.path.exists(self.scaler_path):
            logger.warning("Scaler file not found: %s. Falling back to rules.", self.scaler_path)
            return
        if not os.path.exists(self.label_encoder_path):
            logger.warning("Label encoder file not found: %s. Falling back to rules.", self.label_encoder_path)
            return

        try:
            self.scaler = joblib.load(self.scaler_path)
            self.label_encoder = joblib.load(self.label_encoder_path)

            input_size = int(getattr(self.scaler, "n_features_in_", 6))
            self.model = DNN(input_size=input_size, hidden_size=self.hidden_size, output_size=1)
            state_dict = torch.load(self.model_path, map_location=torch.device("cpu"))
            self.model.load_state_dict(state_dict)
            self.model.eval()

            logger.info(
                "Loaded model artifacts: model=%s scaler=%s label_encoder=%s input_features=%d",
                self.model_path,
                self.scaler_path,
                self.label_encoder_path,
                input_size,
            )
        except Exception as exc:
            logger.error("Failed to load model artifacts: %s. Falling back to rules.", exc)
            self.model = None

    @staticmethod
    def _raw_feature_vector(reading: Dict[str, object]) -> np.ndarray:
        # Match training artifacts: 5 vital-sign features in training order (HR, Temp, SpO2, SysBP, DiaBP).
        return np.array(
            [
                float(reading.get("hr", 72)),
                float(reading.get("temp", 37.0)),
                float(reading.get("spo2", 98)),
                float(reading.get("bp_sys", 112)),
                float(reading.get("bp_dia", 72)),
            ],
            dtype=np.float64,
        )

    def _aligned_features(self, reading: Dict[str, object]) -> np.ndarray:
        values = self._raw_feature_vector(reading)
        expected = int(getattr(self.scaler, "n_features_in_", values.shape[0]))
        if values.shape[0] == expected:
            return values.reshape(1, -1)

        if values.shape[0] > expected:
            logger.warning("Truncating feature vector from %d to %d", values.shape[0], expected)
            return values[:expected].reshape(1, -1)

        logger.warning("Padding feature vector from %d to %d", values.shape[0], expected)
        padded = np.zeros(expected, dtype=np.float64)
        padded[: values.shape[0]] = values
        return padded.reshape(1, -1)

    def predict(self, reading: Dict[str, object]) -> tuple[float, str]:
        if not TORCH_AVAILABLE or self.model is None:
            # Rule-based fallback
            score = RiskLabeler.score(reading)
            label = RiskLabeler.label(score)
            return score, label

        features = self._aligned_features(reading)
        scaled = self.scaler.transform(features)
        inputs = torch.tensor(scaled, dtype=torch.float32)

        with torch.no_grad():
            logits = self.model(inputs)
            positive_class_prob = float(torch.sigmoid(logits).item())

        cls = 1 if positive_class_prob >= 0.5 else 0
        label = str(self.label_encoder.inverse_transform([cls])[0]).strip().lower()

        classes = [str(c).strip().lower() for c in self.label_encoder.classes_]
        high_idx = next((i for i, name in enumerate(classes) if "high" in name), None)
        if high_idx is None:
            # Fallback: preserve previous behavior if no explicit high-risk class name exists.
            high_risk_score = positive_class_prob
        else:
            high_risk_score = positive_class_prob if high_idx == 1 else (1.0 - positive_class_prob)

        return high_risk_score, label


class KafkaProdCons:
    """Wraps Kafka producer and consumer setup/operations."""

    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str = "monitoring-group",
        max_init_retries: int = 30,
        retry_wait_seconds: float = 2.0,
    ):
        self.topic = topic
        self.producer = None
        self.consumer = None

        last_error = None
        for attempt in range(1, max_init_retries + 1):
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8"),
                    acks="all",
                    retries=5,
                    compression_type="gzip",
                )
                self.consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=bootstrap_servers,
                    group_id=group_id,
                    auto_offset_reset="latest",
                    enable_auto_commit=True,
                    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                    key_deserializer=lambda m: m.decode("utf-8") if m else "unknown",
                    consumer_timeout_ms=1000,
                )
                logger.info("Kafka producer/consumer initialized on attempt %d", attempt)
                return
            except NoBrokersAvailable as exc:
                last_error = exc
                logger.warning(
                    "Kafka not ready yet (attempt %d/%d). Retrying in %.1fs...",
                    attempt,
                    max_init_retries,
                    retry_wait_seconds,
                )
                time.sleep(retry_wait_seconds)

        raise NoBrokersAvailable(
            f"Kafka unavailable after {max_init_retries} attempts"
        ) from last_error

    def publish(self, key: str, value: Dict[str, object]) -> None:
        self.producer.send(self.topic, key=key, value=value)

    def flush(self) -> None:
        self.producer.flush()

    def close(self) -> None:
        self.producer.flush()
        self.producer.close()
        self.consumer.close()
