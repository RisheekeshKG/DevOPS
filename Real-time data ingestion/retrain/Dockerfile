FROM python:3.11-slim

WORKDIR /app

COPY retrain/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.5.1

COPY retrain/retrain_model.py /app/retrain_model.py

CMD ["python", "retrain_model.py"]
