"""Weekly model retraining script.

Pulls recent patient vitals from InfluxDB, labels them using the rule-based
RiskLabeler, combines with the original training dataset, retrains the DNN,
and saves new artifacts only if the new model outperforms the existing one.
"""

import json
import logging
import os
import sys
import urllib.request
import urllib.parse

import joblib
import numpy as np
import pandas as pd
import random
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from torch.utils.data import DataLoader, TensorDataset


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
SEED = 42
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "devops-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "devops-org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "patient_vitals")
QUERY_RANGE = os.getenv("RETRAIN_QUERY_RANGE", "-7d")

ORIGINAL_CSV = os.getenv("ORIGINAL_CSV_PATH", "/app/human_vital_signs_dataset_2024.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "/app/human_vital_sign_model2.pth")
SCALER_PATH = os.getenv("SCALER_PATH", "/app/scaler2.pkl")
LABEL_ENCODER_PATH = os.getenv("LABEL_ENCODER_PATH", "/app/label_encoder2.pkl")

HIDDEN_SIZE = 128
LEARNING_RATE = 0.0001
NUM_EPOCHS = 20
BATCH_SIZE = 32

# Feature columns in training order
FEATURE_COLS = [
    "Heart Rate",
    "Body Temperature",
    "Oxygen Saturation",
    "Systolic Blood Pressure",
    "Diastolic Blood Pressure",
]


def set_seed(seed: int = SEED) -> None:
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


# ------------------------------------------------------------------
# DNN (must mirror the training architecture exactly)
# ------------------------------------------------------------------
class DNN(nn.Module):
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


# ------------------------------------------------------------------
# Rule-based labeler (same logic as kafka_prod_cons.RiskLabeler)
# ------------------------------------------------------------------
def rule_based_score(hr: float, spo2: float, temp: float, bp_sys: float, bp_dia: float) -> float:
    risk = 0.0
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


def rule_based_label(score: float) -> str:
    if score > 0.70:
        return "High Risk"
    if score >= 0.35:
        return "High Risk"
    return "Low Risk"


# ------------------------------------------------------------------
# Pull data from InfluxDB
# ------------------------------------------------------------------
def query_influxdb(range_str: str) -> pd.DataFrame:
    """Query InfluxDB for recent patient vitals using Flux."""
    flux_query = f"""
from(bucket: "{INFLUXDB_BUCKET}")
  |> range(start: {range_str})
  |> filter(fn: (r) => r._measurement == "patient_vitals")
  |> filter(fn: (r) => r._field == "hr" or r._field == "spo2" or r._field == "temp" or r._field == "bp_sys" or r._field == "bp_dia")
  |> pivot(rowKey: ["_time", "patient_id"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "patient_id", "hr", "spo2", "temp", "bp_sys", "bp_dia"])
"""
    endpoint = f"{INFLUXDB_URL}/api/v2/query"
    params = urllib.parse.urlencode({"org": INFLUXDB_ORG})
    url = f"{endpoint}?{params}"

    body = json.dumps({"query": flux_query, "type": "flux"}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Token {INFLUXDB_TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/csv")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as exc:
        logger.error("Failed to query InfluxDB: %s", exc)
        return pd.DataFrame()

    if not raw.strip():
        logger.warning("Empty response from InfluxDB")
        return pd.DataFrame()

    # Parse CSV response — InfluxDB returns annotated CSV
    lines = raw.strip().split("\n")
    # Filter out annotation lines (start with #) and blank lines
    data_lines = [l for l in lines if l and not l.startswith("#")]
    if len(data_lines) < 2:
        return pd.DataFrame()

    from io import StringIO
    csv_text = "\n".join(data_lines)
    df = pd.read_csv(StringIO(csv_text))

    # Rename to match training columns
    rename_map = {
        "hr": "Heart Rate",
        "spo2": "Oxygen Saturation",
        "temp": "Body Temperature",
        "bp_sys": "Systolic Blood Pressure",
        "bp_dia": "Diastolic Blood Pressure",
    }
    df = df.rename(columns=rename_map)

    # Keep only the columns we need
    keep = [c for c in FEATURE_COLS if c in df.columns]
    if len(keep) != len(FEATURE_COLS):
        logger.warning("InfluxDB data missing some feature columns: got %s", keep)
        return pd.DataFrame()

    return df[keep].dropna()


# ------------------------------------------------------------------
# Load original dataset
# ------------------------------------------------------------------
def load_original_dataset() -> pd.DataFrame:
    if not os.path.exists(ORIGINAL_CSV):
        logger.error("Original CSV not found at %s", ORIGINAL_CSV)
        return pd.DataFrame()

    df = pd.read_csv(ORIGINAL_CSV)
    df = df.drop_duplicates()

    # Keep only relevant columns
    keep_cols = FEATURE_COLS + ["Risk Category"]
    missing = [c for c in keep_cols if c not in df.columns]
    if missing:
        logger.error("Original CSV missing columns: %s", missing)
        return pd.DataFrame()

    return df[keep_cols]


# ------------------------------------------------------------------
# Training
# ------------------------------------------------------------------
def train_model(df: pd.DataFrame) -> tuple:
    """Train the DNN and return (model, scaler, label_encoder, metrics_dict)."""
    set_seed()

    label_encoder = LabelEncoder()
    df = df.copy()
    df["Risk Category"] = label_encoder.fit_transform(df["Risk Category"])

    X = df.drop("Risk Category", axis="columns").values
    y = df["Risk Category"].values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    X_test_t = torch.tensor(X_test, dtype=torch.float32)
    y_test_t = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

    train_loader = DataLoader(
        TensorDataset(X_train_t, y_train_t),
        batch_size=BATCH_SIZE,
        shuffle=True,
        generator=torch.Generator().manual_seed(SEED),
    )
    test_loader = DataLoader(
        TensorDataset(X_test_t, y_test_t),
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    input_size = X_train.shape[1]
    model = DNN(input_size=input_size, hidden_size=HIDDEN_SIZE, output_size=1)

    # Xavier init
    def init_weights(m):
        if isinstance(m, nn.Linear):
            torch.nn.init.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)

    model.apply(init_weights)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(NUM_EPOCHS):
        model.train()
        epoch_loss = 0
        for inputs, labels in train_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()

        train_loss = epoch_loss / len(train_loader)
        model.eval()
        test_loss = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                test_loss += loss.item()
        test_loss = test_loss / len(test_loader)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            logger.info(
                "Epoch [%d/%d], Train Loss: %.4f, Test Loss: %.4f",
                epoch + 1, NUM_EPOCHS, train_loss, test_loss,
            )

    # Evaluate
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            predicted = (torch.sigmoid(outputs) >= 0.5).numpy().flatten()
            y_true.extend(labels.numpy().flatten())
            y_pred.extend(predicted)

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }

    return model, scaler, label_encoder, metrics


# ------------------------------------------------------------------
# Evaluate existing model
# ------------------------------------------------------------------
def evaluate_existing_model() -> dict | None:
    """Load existing artifacts and return their test metrics, or None if unavailable."""
    if not all(os.path.exists(p) for p in [MODEL_PATH, SCALER_PATH, LABEL_ENCODER_PATH]):
        logger.info("No existing model artifacts found — will save new model regardless.")
        return None

    try:
        scaler = joblib.load(SCALER_PATH)
        label_encoder = joblib.load(LABEL_ENCODER_PATH)
        input_size = int(getattr(scaler, "n_features_in_", 5))

        model = DNN(input_size=input_size, hidden_size=HIDDEN_SIZE, output_size=1)
        state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
        model.load_state_dict(state_dict)
        model.eval()

        # Quick validation on original data
        orig_df = load_original_dataset()
        if orig_df.empty:
            return None

        orig_df_copy = orig_df.copy()
        le_temp = LabelEncoder()
        orig_df_copy["Risk Category"] = le_temp.fit_transform(orig_df_copy["Risk Category"])

        X = orig_df_copy.drop("Risk Category", axis="columns").values
        y = orig_df_copy["Risk Category"].values
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)

        X_scaled = scaler.transform(X_test)
        X_t = torch.tensor(X_scaled, dtype=torch.float32)

        with torch.no_grad():
            logits = model(X_t)
            preds = (torch.sigmoid(logits) >= 0.5).numpy().flatten()

        return {
            "accuracy": accuracy_score(y_test, preds),
            "f1": f1_score(y_test, preds, zero_division=0),
        }
    except Exception as exc:
        logger.warning("Could not evaluate existing model: %s", exc)
        return None


# ------------------------------------------------------------------
# Single retraining run
# ------------------------------------------------------------------
def run_retrain() -> None:
    logger.info("=" * 60)
    logger.info("Starting model retraining pipeline")
    logger.info("=" * 60)

    # 1. Load original dataset
    logger.info("Loading original dataset from %s ...", ORIGINAL_CSV)
    orig_df = load_original_dataset()
    if orig_df.empty:
        logger.error("Cannot proceed without original dataset.")
        return
    logger.info("Original dataset: %d rows", len(orig_df))

    # 2. Query InfluxDB for recent data
    logger.info("Querying InfluxDB for data in range %s ...", QUERY_RANGE)
    influx_df = query_influxdb(QUERY_RANGE)
    if influx_df.empty:
        logger.warning("No data from InfluxDB — training on original dataset only.")
    else:
        logger.info("InfluxDB data: %d rows", len(influx_df))

        # 3. Add pseudo-labels using rule-based labeler
        labels = []
        for _, row in influx_df.iterrows():
            score = rule_based_score(
                row["Heart Rate"],
                row["Oxygen Saturation"],
                row["Body Temperature"],
                row["Systolic Blood Pressure"],
                row["Diastolic Blood Pressure"],
            )
            labels.append(rule_based_label(score))
        influx_df["Risk Category"] = labels
        label_dist = influx_df["Risk Category"].value_counts().to_dict()
        logger.info("InfluxDB label distribution: %s", label_dist)

        # 4. Combine datasets
        orig_df = pd.concat([orig_df, influx_df], ignore_index=True)
        logger.info("Combined dataset: %d rows", len(orig_df))

    # 5. Evaluate existing model
    logger.info("Evaluating existing model ...")
    old_metrics = evaluate_existing_model()
    if old_metrics:
        logger.info("Existing model — Accuracy: %.2f%%, F1: %.2f%%",
                     old_metrics["accuracy"] * 100, old_metrics["f1"] * 100)

    # 6. Train new model
    logger.info("Training new model ...")
    new_model, new_scaler, new_le, new_metrics = train_model(orig_df)
    logger.info(
        "New model — Accuracy: %.2f%%, Precision: %.2f%%, Recall: %.2f%%, F1: %.2f%%",
        new_metrics["accuracy"] * 100,
        new_metrics["precision"] * 100,
        new_metrics["recall"] * 100,
        new_metrics["f1"] * 100,
    )

    # 7. Compare and decide whether to save
    should_save = True
    if old_metrics:
        if new_metrics["f1"] <= old_metrics["f1"]:
            logger.info(
                "New model F1 (%.2f%%) did NOT improve over existing (%.2f%%). Skipping save.",
                new_metrics["f1"] * 100, old_metrics["f1"] * 100,
            )
            should_save = False
        else:
            logger.info(
                "New model F1 (%.2f%%) improved over existing (%.2f%%). Saving!",
                new_metrics["f1"] * 100, old_metrics["f1"] * 100,
            )

    if should_save:
        torch.save(new_model.state_dict(), MODEL_PATH)
        joblib.dump(new_scaler, SCALER_PATH)
        joblib.dump(new_le, LABEL_ENCODER_PATH)
        logger.info("Saved new model artifacts to %s, %s, %s", MODEL_PATH, SCALER_PATH, LABEL_ENCODER_PATH)
    else:
        logger.info("Keeping existing model artifacts.")

    logger.info("=" * 60)
    logger.info("Retraining pipeline complete.")
    logger.info("=" * 60)


# ------------------------------------------------------------------
# Scheduler
# ------------------------------------------------------------------
def main() -> None:
    import time

    # RETRAIN_INTERVAL_SECONDS: how often to retrain (default: 7 days)
    interval = int(os.getenv("RETRAIN_INTERVAL_SECONDS", str(7 * 24 * 60 * 60)))
    # RETRAIN_INITIAL_DELAY_SECONDS: wait before first run (default: 60s to let data accumulate)
    initial_delay = int(os.getenv("RETRAIN_INITIAL_DELAY_SECONDS", "60"))
    # RETRAIN_MODE: "once" for a single run, "schedule" for recurring (default: schedule)
    mode = os.getenv("RETRAIN_MODE", "schedule")

    if mode == "once":
        logger.info("Running in one-shot mode.")
        run_retrain()
        return

    logger.info(
        "Retrain scheduler started — initial delay: %ds, interval: %ds (%.1f days)",
        initial_delay, interval, interval / 86400,
    )

    logger.info("Waiting %ds before first retraining run ...", initial_delay)
    time.sleep(initial_delay)

    while True:
        try:
            run_retrain()
        except Exception as exc:
            logger.error("Retraining failed: %s", exc, exc_info=True)

        logger.info("Next retraining in %d seconds (%.1f days). Sleeping ...", interval, interval / 86400)
        time.sleep(interval)


if __name__ == "__main__":
    main()

