FROM python:3.11-slim

WORKDIR /app

COPY retrain/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --default-timeout=1000 -r /app/requirements.txt

# Attempt torch install but allow build to proceed if it timeouts (resilient mode)
RUN pip install --no-cache-dir --default-timeout=1000 --index-url https://download.pytorch.org/whl/cpu torch==2.5.1 || \
    echo "Warning: Torch install failed. Retraining will be disabled."

COPY retrain/retrain_model.py /app/retrain_model.py
COPY influxDB.py /app/influxDB.py

CMD ["python", "retrain_model.py"]
