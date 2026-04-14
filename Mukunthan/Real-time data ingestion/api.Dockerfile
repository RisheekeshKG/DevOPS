FROM python:3.11-slim

WORKDIR /app

# Only install what's needed for the bridge
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.31.0 \
    aiokafka==0.12.0

COPY api_bridge.py /app/api_bridge.py

EXPOSE 8001

CMD ["python", "api_bridge.py"]
