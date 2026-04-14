FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --default-timeout=1000 -r /app/requirements.txt

# Attempt torch install but allow build to proceed if it timeouts (resilient mode)
RUN pip install --no-cache-dir --default-timeout=1000 --index-url https://download.pytorch.org/whl/cpu torch==2.5.1 || \
    echo "Warning: Torch install failed. System will run in rule-based fallback mode."

COPY . /app

CMD ["python", "main_workflow.py"]
