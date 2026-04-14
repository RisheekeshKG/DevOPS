# 🏥 Intelligent Patient Risk Monitoring with MLOps & Arduino

> Real-time patient vitals monitoring powered by Arduino sensors, a cloud MLOps pipeline, and continuous model improvement — built on the **7 Cs of MLOps** framework.

---

## 📌 Introduction

Healthcare systems worldwide face a critical challenge: **detecting patient deterioration early enough to intervene**. Traditional monitoring relies on periodic manual checks, which can miss rapid changes in a patient's condition. Delayed response to deteriorating vitals is a leading cause of preventable in-hospital deaths.

**Intelligent Patient Risk Monitoring** addresses this by combining low-cost Arduino hardware with production-grade machine learning to deliver **continuous, automated, real-time risk scoring** for every patient — 24 hours a day, 7 days a week.

### What this system does

1. **Collects** raw patient vitals every second via Arduino-connected sensors (heart rate, SpO2, temperature, blood pressure, ECG)
2. **Cleanses** and filters noisy sensor data at the edge before transmission
3. **Streams** data reliably to a cloud pipeline via MQTT and Kafka
4. **Trains and deploys** ML models (LSTM / XGBoost) using a full MLOps pipeline
5. **Scores** every reading in real time — classifying patient risk as Low, Medium, or High
6. **Alerts** clinical staff instantly when risk thresholds are crossed
7. **Improves continuously** through automated drift detection, retraining, and feedback loops

### Why MLOps matters in healthcare

A model trained once and left to run will silently degrade as patient populations shift, seasonal patterns change, or sensor calibration drifts. MLOps ensures the system **never stops learning** — every deployment is tracked, every degradation is caught, and every retrain is triggered automatically.

### Risk classification

| Score | Risk Level | Clinical Action |
|---|---|---|
| < 0.35 | 🟢 Low | Log and monitor passively |
| 0.35 – 0.70 | 🟡 Medium | Alert nursing staff |
| > 0.70 | 🔴 High | Immediate escalation to physician |

### Key design targets

- **End-to-end latency**: < 200ms (clinical safety ceiling)
- **Model P99 inference**: < 50ms
- **Uptime**: 99.9% (continuous operations)
- **Retraining**: Automatic on drift detection or weekly schedule

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [System Workflow](#-system-workflow-6-steps)
- [7 Cs of MLOps](#-7-cs-of-mlops)
- [System Architecture](#-system-architecture)
- [Hardware & Sensors](#-hardware--sensors)
- [Tech Stack](#-tech-stack)
- [Quickstart](#-quickstart)
- [Arduino Firmware](#-arduino-firmware)
- [MLOps Pipeline](#-mlops-pipeline)
- [Inference API](#-inference-api)
- [Latency Benchmarking](#-latency-benchmarking)
- [Deployment](#-deployment)
- [Monitoring & Alerting](#-monitoring--alerting)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Contributing](#-contributing)

---

## 🔄 System Workflow (6 Steps)

The system operates as a continuous closed loop across six stages. Each stage feeds directly into the next, and the output of the final stage feeds back into the first via automated retraining.

```
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1 — Arduino sensors (data collection)                         │
│  HR (MAX30102) · SpO2 · Temp (DS18B20) · ECG (AD8232) · BP (MPX5050)│
└───────────────────────────┬─────────────────────────────────────────┘
                            │ raw analog / I2C signals
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2 — Edge gateway (ESP32 / Arduino Mega)                       │
│  Sensor aggregation → Noise filtering → Normalise → Edge TinyML     │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ MQTT over WiFi
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3 — Real-time data ingestion                                  │
│  MQTT Broker (Mosquitto) → Kafka stream → InfluxDB time-series      │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 4 — MLOps pipeline (train → evaluate → deploy)                │
│  Feature Eng → LSTM/XGBoost training → MLflow → Docker → FastAPI    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 5 — Real-time inference & monitoring                          │
│  Risk score 0–1 → Evidently AI drift detection → Auto-retrain       │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 6 — Alerting & clinical dashboard                             │
│  Grafana dashboard · SMS/push alerts · Audit logging (Postgres/S3)  │
└─────────────────────────────────────────────────────────────────────┘
         │
         │ Continuous feedback loop (outcomes → labelled data → retrain)
         └──────────────────────────────────────────────────────────────►
```

### Step 1 — Arduino sensor data collection

Arduino-connected sensors sample patient vitals at 1Hz. Each sensor module is chosen for clinical accuracy and low-power operation:

- **MAX30102** — optical heart rate and SpO2 (blood oxygen) via I2C
- **DS18B20 / MLX90614** — body temperature via 1-Wire or I2C
- **MPX5050 / BMP280** — blood pressure estimation via analog or I2C
- **AD8232** — single-lead ECG signal via analog pin

### Step 2 — Edge gateway (ESP32)

The ESP32 acts as an intelligent edge gateway. It aggregates all sensor streams, applies a Kalman filter and Z-score outlier rejection to remove noise, normalises values to a 0–1 range, and optionally runs a lightweight TinyML model for instant local alerts — bypassing the cloud entirely for emergency cases.

### Step 3 — Real-time data ingestion

Cleansed readings are published over MQTT to a Mosquitto broker. A Kafka consumer fans the stream into InfluxDB (time-series storage optimised for high-frequency vitals data). This decoupled architecture ensures no data is lost even under network interruptions.

### Step 4 — MLOps pipeline

Features are engineered from rolling windows (30-second rolling mean, HRV, trend slopes, lag features). Models are trained using scikit-learn (Random Forest / XGBoost) or PyTorch (LSTM for temporal patterns). Every experiment is tracked in MLflow. Validated models are packaged into Docker containers and served via FastAPI.

### Step 5 — Real-time inference & monitoring

Every incoming reading is scored by the deployed model in under 50ms. Evidently AI monitors the prediction distribution for data drift. When drift is detected — or on a weekly schedule — an automated retrain is triggered, the new model is validated, and CI/CD redeploys it with zero downtime.

### Step 6 — Alerting & clinical dashboard

Risk scores stream into Grafana for live visualisation. Medium-risk patients trigger push/SMS alerts to nursing staff. High-risk patients trigger immediate escalation. All predictions are logged to Postgres or S3 for clinical audit and compliance.

---

## 🔁 7 Cs of MLOps

This project is structured around the **7 Cs of MLOps** — a framework for managing the complete lifecycle of machine learning in production systems. In healthcare, where model degradation can have serious consequences, each phase is non-negotiable.

---

### C1 — Continuous Development (CDev)

> *Plan, develop, and iterate on machine learning models, code, and data pipelines.*

This is where the system begins. Every feature, model architecture, and pipeline component is version-controlled, documented, and designed for iteration.

**In this project:**
- Arduino sensor pipeline is designed for modularity — swap sensors without touching the ML layer
- Model architecture is configurable: `RandomForest`, `XGBoost`, or `LSTM` selected via config
- Feature engineering is iterative — rolling windows, HRV calculation, and lag features are added via a feature registry
- All experiments are tracked in MLflow so no iteration is ever lost

**Key files:**
```
mlops/
├── train_pipeline.py        # Model training entry point
├── feature_engineering.py   # Feature extraction from raw vitals
├── model_config.yaml         # Model type and hyperparameter config
└── experiments/              # MLflow experiment logs
```

---

### C2 — Continuous Integration (CI)

> *Test not only code but also data validation and model schema testing. When data or code changes, the ML pipeline automatically rebuilds and validates.*

Every push to the repository triggers a GitHub Actions workflow that validates both code quality and data integrity before any model is trained.

**In this project:**
- **Schema validation**: incoming sensor payloads are validated against a Pydantic schema — catches malformed readings like `spo2: 200` or `hr: -5` before they corrupt training data
- **Unit tests**: preprocessing functions, feature extractors, and alert logic are unit tested
- **Pipeline rebuild**: any change to `mlops/` or `firmware/` triggers a full pipeline rebuild
- **Data quality checks**: Great Expectations profiles are run against new data batches

**Schema validation example:**
```python
from pydantic import BaseModel, validator

class VitalsPayload(BaseModel):
    patient_id: str
    hr:         float
    spo2:       float
    temp:       float
    bp_sys:     float
    bp_dia:     float

    @validator('spo2')
    def spo2_in_range(cls, v):
        assert 0 < v <= 100, f"SpO2 out of range: {v}"
        return v

    @validator('hr')
    def hr_in_range(cls, v):
        assert 0 < v < 300, f"Heart rate out of range: {v}"
        return v
```

---

### C3 — Continuous Testing (CT)

> *Automated tests are run to validate model quality, performance, and reliability before deployment.*

No model reaches production without passing a battery of automated quality gates.

**In this project:**
- **Model quality**: AUC-ROC ≥ 0.92, F1 score ≥ 0.88 on held-out test set
- **Latency benchmark**: model P99 inference < 50ms, API end-to-end P95 < 150ms
- **Pipeline reliability**: stress test with 1,000 concurrent sensor readings
- **Regression test**: new model must not degrade accuracy on a frozen reference dataset

**Latency benchmark (runs in CI):**
```python
import time, numpy as np

def benchmark_inference(model, n_runs=1000):
    dummy = np.random.rand(1, 7)
    for _ in range(10):          # warm-up pass
        model.predict(dummy)

    latencies = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        model.predict(dummy)
        latencies.append((time.perf_counter() - t0) * 1000)

    latencies.sort()
    return {
        "p50_ms": round(latencies[int(n_runs * 0.50)], 2),
        "p90_ms": round(latencies[int(n_runs * 0.90)], 2),
        "p95_ms": round(latencies[int(n_runs * 0.95)], 2),
        "p99_ms": round(latencies[int(n_runs * 0.99)], 2),
    }

results = benchmark_inference(model)
assert results["p99_ms"] < 50, f"P99 latency {results['p99_ms']}ms exceeds 50ms gate"
```

**CT latency thresholds:**

| Metric | Target | Fail gate |
|---|---|---|
| Model P50 | < 5ms | > 10ms |
| Model P99 | < 50ms | > 50ms |
| API end-to-end P95 | < 100ms | > 150ms |
| Full pipeline P99 | < 200ms | > 200ms |
| Throughput | > 100 req/s | < 50 req/s |

---

### C4 — Continuous Deployment (CD)

> *Validated models are automatically deployed to production or staging environments, enabling frequent updates.*

**In this project:**
- **Model registry**: every passing model is registered in MLflow and promoted `Staging → Production` automatically if metrics improve
- **Docker packaging**: the inference API is containerised with the model artifact baked in
- **Blue-green deployment**: new container starts alongside the old one; traffic switches only after a health check passes
- **Rollback**: if health checks fail, traffic reverts to the previous version within 30 seconds

**Deployment flow:**
```
CT passes → MLflow registers model → Docker image built
    → Push to registry → Deploy to staging
    → Health check passes → Promote to production
    → Old container terminated
```

**docker-compose.yml:**
```yaml
services:
  mosquitto:
    image: eclipse-mosquitto
    ports: ["1883:1883"]

  influxdb:
    image: influxdb:2.7
    ports: ["8086:8086"]

  mlflow:
    image: ghcr.io/mlflow/mlflow
    ports: ["5000:5000"]

  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - MLFLOW_TRACKING_URI=http://mlflow:5000

  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]
```

---

### C5 — Continuous Monitoring (CM)

> *Deployed models are continuously monitored to track performance, detect data drift, and ensure the model remains accurate in real-world scenarios.*

**In this project:**
- **Data drift**: Evidently AI computes Population Stability Index (PSI) on incoming vitals every hour — PSI > 0.25 triggers auto-retrain
- **Prediction drift**: distribution of risk scores is monitored for unexpected shifts
- **Model accuracy**: retrospective accuracy computed against clinical outcomes (discharge, escalation events)
- **Infrastructure**: Prometheus scrapes API latency, error rates, and throughput every 15 seconds

**Drift check (runs hourly via cron):**
```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def check_drift(reference_df, current_df):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_df, current_data=current_df)
    result = report.as_dict()

    if result["metrics"][0]["result"]["dataset_drift"]:
        trigger_retrain(reason="data_drift")
        send_alert("Data drift detected — retraining scheduled")
```

---

### C6 — Continuous Feedback (CF)

> *Insights from monitoring data and user experience are gathered to improve the product and refine the model.*

**In this project:**
- **Clinician feedback UI**: nurses and physicians flag incorrect predictions (false positives generate alert fatigue; false negatives are safety risks)
- **Outcome labelling**: ICU transfers, discharge summaries, and code events are matched to prediction records as retrospective labels
- **FP/FN analysis**: weekly report shows which patient profiles the model most frequently misclassifies
- **Threshold tuning**: precision/recall tradeoffs reviewed monthly without requiring a full retrain

**Feedback data schema:**
```python
class ClinicalFeedback(BaseModel):
    prediction_id:  str
    patient_id:     str
    predicted_risk: str        # "low" | "medium" | "high"
    actual_outcome: str        # "stable" | "deteriorated" | "escalated"
    clinician_note: str
    timestamp:      datetime
```

---

### C7 — Continuous Operations (CO)

> *Maintaining the model in production with minimal downtime, including automated retraining, model updates, and infrastructure management.*

**In this project:**
- **Automated retraining**: Airflow DAG retrains weekly (Sunday 02:00 UTC) using the past 30 days of labelled data; drift-triggered retrains run on demand
- **Arduino OTA updates**: firmware updates pushed over-the-air to all ESP32 boards — no physical access required
- **Zero-downtime deploys**: blue-green deployments keep the API live during model updates
- **Auto-scaling**: Kubernetes HPA scales the inference service when throughput exceeds 80 req/s

**Airflow retraining DAG:**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG("weekly_retrain",
         schedule_interval="0 2 * * 0",
         start_date=datetime(2024, 1, 1),
         catchup=False) as dag:

    fetch    = PythonOperator(task_id="fetch_data",      python_callable=fetch_recent_data)
    validate = PythonOperator(task_id="validate_schema", python_callable=validate_data)
    train    = PythonOperator(task_id="train_model",     python_callable=train_model)
    test     = PythonOperator(task_id="run_ct_gates",    python_callable=run_ct_gates)
    deploy   = PythonOperator(task_id="deploy_model",    python_callable=deploy_to_production)

    fetch >> validate >> train >> test >> deploy
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  HARDWARE LAYER                          │
│  MAX30102 · DS18B20 · MPX5050 · AD8232  →  ESP32        │
└────────────────────────┬────────────────────────────────┘
                         │ MQTT / WiFi
┌────────────────────────▼────────────────────────────────┐
│                  INGESTION LAYER                         │
│  Mosquitto → Kafka → InfluxDB                           │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  MLOPS LAYER                             │
│  Feature Eng → MLflow Train → Evaluate → Docker Deploy  │
└────────────────────────┬────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────┐
│                  INFERENCE LAYER                         │
│  FastAPI → Risk Score → Evidently AI drift monitor      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                  OUTPUT LAYER                            │
│  Grafana dashboard · SMS/push alerts · Audit log        │
└─────────────────────────────────────────────────────────┘
         ↑ Continuous feedback loop (CO → CDev)
```

**End-to-end latency target: < 200ms**

---

## 🔌 Hardware & Sensors

| Sensor | Module | Measures | Interface |
|---|---|---|---|
| Heart Rate + SpO2 | MAX30102 | BPM + blood oxygen % | I2C |
| Body Temperature | DS18B20 / MLX90614 | °C (contact / non-contact) | 1-Wire / I2C |
| Blood Pressure | MPX5050 / BMP280 | Systolic / diastolic mmHg | Analog / I2C |
| ECG Signal | AD8232 | Electrical heart activity | Analog |

**Recommended microcontrollers:**
- **ESP32** — WiFi built-in, supports OTA, 240MHz dual-core — best choice
- **Arduino Mega + ESP8266** — larger GPIO count when more sensors are needed

**Wiring summary:**
```
MAX30102  → SDA (pin 21), SCL (pin 22)         [I2C]
DS18B20   → Digital pin 4                       [1-Wire, 4.7kΩ pull-up to 3.3V]
AD8232    → A0 (OUTPUT), D2 (LO+), D3 (LO-)    [Analog + digital]
MPX5050   → A1                                   [Analog, 0–5V range]
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Microcontroller | ESP32 / Arduino Mega |
| HR + SpO2 sensor | MAX30102 |
| Temperature sensor | DS18B20 / MLX90614 |
| Blood pressure sensor | MPX5050 / BMP280 |
| ECG sensor | AD8232 |
| MQTT broker | Mosquitto |
| Stream queue | Apache Kafka / RabbitMQ |
| Time-series DB | InfluxDB 2.x |
| ML framework | scikit-learn / PyTorch (LSTM) |
| Experiment tracking | MLflow |
| Drift detection | Evidently AI |
| Data validation | Great Expectations / Pydantic |
| Workflow orchestration | Apache Airflow |
| Inference API | FastAPI + Uvicorn |
| Containerisation | Docker + Docker Compose |
| Orchestration | Kubernetes (HPA) |
| Dashboard | Grafana + Prometheus |
| CI/CD | GitHub Actions |
| Audit storage | PostgreSQL / AWS S3 |

---

## 🚀 Quickstart

### Prerequisites

- Docker + Docker Compose
- Python 3.11+
- Arduino IDE with ESP32 board support
- MLflow tracking server (local or remote)

### 1. Clone the repository

```bash
git clone https://github.com/your-org/patient-risk-monitoring.git
cd patient-risk-monitoring
```

### 2. Start all backend services

```bash
docker-compose up -d
```

| Service | URL |
|---|---|
| Grafana dashboard | http://localhost:3005 |
| MLflow UI | http://localhost:5000 |
| FastAPI docs | http://localhost:8000/docs |
| InfluxDB UI | http://localhost:8086 |

### 3. Flash the Arduino firmware

Open `firmware/patient_monitor.ino` in Arduino IDE. Update WiFi credentials and MQTT broker IP at the top of the file, then upload to your ESP32.

### 4. Train the initial model

```bash
python mlops/train_pipeline.py --data data/patient_vitals.csv
```

### 5. Run the CT benchmark gates

```bash
python tests/benchmark_latency.py
```

### 6. Open the live dashboard

Navigate to `http://localhost:3005` — the pre-built Grafana dashboard shows live vitals, risk scores, and alert history.

---

## 🔧 Arduino Firmware

```cpp
#include <Wire.h>
#include <MAX30105.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <PubSubClient.h>

MAX30105 particleSensor;
OneWire oneWire(4);
DallasTemperature tempSensor(&oneWire);
WiFiClient espClient;
PubSubClient mqtt(espClient);

void setup() {
  Serial.begin(115200);
  particleSensor.begin(Wire, I2C_SPEED_FAST);
  particleSensor.setup();
  tempSensor.begin();
  WiFi.begin("YOUR_SSID", "YOUR_PASSWORD");
  mqtt.setServer("YOUR_BROKER_IP", 1883);
}

void loop() {
  long irValue = particleSensor.getIR();
  float bpm    = calculateBPM(irValue);   // implement BPM algorithm
  float spo2   = calculateSpO2();          // red + IR ratio method
  tempSensor.requestTemperatures();
  float temp   = tempSensor.getTempCByIndex(0);

  String payload = "{\"hr\":"    + String(bpm)  +
                   ",\"spo2\":" + String(spo2) +
                   ",\"temp\":" + String(temp)  + "}";
  mqtt.publish("patient/vitals", payload.c_str());
  delay(1000);
}
```

---

## 🤖 MLOps Pipeline

### Feature engineering

| Feature | Description | Window |
|---|---|---|
| `hr_rolling_mean` | Mean heart rate | 30 seconds |
| `spo2_rolling_min` | Minimum SpO2 | 30 seconds |
| `hrv` | Heart rate variability (RMSSD) | 60 seconds |
| `temp_trend` | Temperature slope | 5 minutes |
| `bp_pulse_pressure` | Systolic − diastolic | Instantaneous |
| `hr_lag_1` | Previous heart rate reading | 1 sample |

### Model training

```python
import mlflow, mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model(df):
    features = ["hr", "spo2", "temp", "bp_sys", "bp_dia",
                "hr_rolling_mean", "spo2_rolling_min"]
    X, y = df[features], df["risk_label"]   # 0=low, 1=medium, 2=high

    with mlflow.start_run():
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        mlflow.log_metric("accuracy", model.score(X_test, y_test))
        mlflow.sklearn.log_model(model, "patient_risk_model")
        mlflow.register_model("runs:/.../patient_risk_model", "PatientRiskModel")
```

---

## ⚡ Inference API

```python
from fastapi import FastAPI
import mlflow.pyfunc

app   = FastAPI()
model = mlflow.pyfunc.load_model("models:/PatientRiskModel/Production")

@app.post("/predict")
def predict(vitals: dict):
    features   = extract_features(vitals)
    risk_score = float(model.predict([features])[0])

    if risk_score < 0.35:
        level = "low"
    elif risk_score < 0.70:
        level = "medium"
        send_alert(vitals["patient_id"], "medium")
    else:
        level = "high"
        escalate_to_nurse(vitals["patient_id"])

    return {"risk_score": round(risk_score, 3), "level": level}
```

---

## 📊 Latency Benchmarking

### Stage-by-stage budget

| Stage | Typical latency | Notes |
|---|---|---|
| Sensor read | ~5ms | Hardware sampling rate |
| Edge preprocessing | ~5ms | Kalman filter + normalise |
| MQTT transmit | ~10ms | Local network |
| Feature engineering | ~3ms | Rolling window calculations |
| ML model inference | 2–18ms | Depends on model type |
| Alert dispatch | ~6ms | Push/SMS API call |
| **Total end-to-end** | **~30–50ms** | **Target: < 200ms** |

### Model latency by type

| Model | P50 | P99 | Notes |
|---|---|---|---|
| TFLite Micro (edge) | ~2ms | ~5ms | Runs on ESP32 directly |
| XGBoost | ~3ms | ~8ms | Fastest cloud option |
| Random Forest | ~4ms | ~12ms | Good accuracy/speed balance |
| LSTM (PyTorch) | ~15ms | ~40ms | Best for temporal patterns |

### End-to-end API benchmark

```python
import httpx, asyncio, statistics

async def benchmark_api(url, n=500):
    latencies = []
    payload = {"hr": 72, "spo2": 98, "temp": 36.6,
                "bp_sys": 120, "bp_dia": 80,
                "hr_rolling_mean": 71.5, "spo2_rolling_min": 97.0}

    async with httpx.AsyncClient() as client:
        for _ in range(n):
            t0 = asyncio.get_event_loop().time()
            await client.post(url, json=payload)
            latencies.append((asyncio.get_event_loop().time() - t0) * 1000)

    latencies.sort()
    return {
        "p50_ms": round(statistics.median(latencies), 1),
        "p95_ms": round(latencies[int(n * 0.95)], 1),
        "p99_ms": round(latencies[int(n * 0.99)], 1),
    }

results = asyncio.run(benchmark_api("http://localhost:8000/predict"))
```

---

## 🐳 Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install fastapi uvicorn mlflow scikit-learn pandas paho-mqtt evidently
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api.inference_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes HPA (auto-scaling)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: patient-risk-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: patient-risk-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80
```

---

## 📡 Monitoring & Alerting

### Grafana panels (pre-built dashboard)

- Live heart rate, SpO2, temperature, and blood pressure per patient
- Real-time risk score timeline (colour-coded by tier)
- Alert history and response times
- Model latency P50 / P95 / P99 trends
- Data drift PSI score over time

### Alert routing

| Risk level | Channel | SLA |
|---|---|---|
| Medium | Push notification to assigned nurse | < 30 seconds |
| High | SMS + push to nurse + pager to physician | < 10 seconds |
| Model degraded | Email to ML engineering team | < 5 minutes |
| Data drift detected | Slack to data team + auto-retrain | Immediate |

---

## ⚙️ CI/CD Pipeline

```yaml
# .github/workflows/mlops_pipeline.yml
name: MLOps CI/CD

on:
  push:
    paths: ['mlops/**', 'api/**', 'tests/**']

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Validate data schema
        run: python tests/validate_schema.py

      - name: Run unit tests
        run: pytest tests/unit/

      - name: Train model
        run: python mlops/train_pipeline.py --data data/test_sample.csv
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}

      - name: Run CT latency benchmark
        run: python tests/benchmark_latency.py --threshold-p99 50

      - name: Build Docker image
        run: docker build -t patient-risk-api:${{ github.sha }} .

      - name: Deploy to staging
        run: ./scripts/deploy_staging.sh

      - name: Promote to production
        if: github.ref == 'refs/heads/main'
        run: ./scripts/promote_production.sh
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request — CI gates run automatically

All PRs must pass CT latency benchmarks before merging.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with Arduino, Python, MLflow, FastAPI, Docker, Kafka, InfluxDB, and Grafana.*

*Structured on the 7 Cs of MLOps: **CDev · CI · CT · CD · CM · CF · CO***