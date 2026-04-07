"""Kafka producer/consumer helpers and risk labeling."""

import json
import logging
import time
from typing import Dict

from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable


logger = logging.getLogger(__name__)


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
