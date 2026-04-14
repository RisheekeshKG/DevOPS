"""FastAPI WebSocket bridge to broadcast Kafka vitals to the frontend."""

import asyncio
import json
import logging
import os
import time
from typing import Set

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api_bridge")

app = FastAPI(title="Patient Vitals API Bridge")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active WebSocket connections
connected_clients: Set[WebSocket] = set()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor-data")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID", "api-bridge-group")
SIMULATION_MODE = os.getenv("SIMULATION_MODE", "false").lower() == "true"

async def consume_and_broadcast():
    """Consumes messages from Kafka and sends them to all connected WS clients."""
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    
    retries = 5 if not SIMULATION_MODE else 0
    if retries > 0:
        # Wait for Kafka to be ready
        while retries > 0:
            try:
                await consumer.start()
                logger.info(f"Kafka consumer started on {KAFKA_TOPIC}")
                break
            except Exception as e:
                logger.error(f"Kafka connection failed: {e}. Retrying in 5s...")
                await asyncio.sleep(5)
                retries -= 1
    
    if retries == 0 or SIMULATION_MODE:
        if SIMULATION_MODE:
            logger.info("SIMULATION MODE ACTIVE: Generating synthetic patient data.")
        else:
            logger.error("Could not connect to Kafka. Falling back to SIMULATION MODE.")
        
        # Mock broadcasting loop
        import random
        patient_pool = os.getenv("PATIENT_IDS", "P001,P002,P003").split(",")
        try:
            while True:
                if connected_clients:
                    p_id = random.choice(patient_pool)
                    payload = {
                        "patient_id": p_id,
                        "hr": random.randint(60, 110),
                        "spo2": random.randint(92, 100),
                        "temp": round(random.uniform(36.2, 38.5), 1),
                        "bp_sys": random.randint(110, 140),
                        "bp_dia": random.randint(70, 90),
                        "risk_score": random.uniform(0.1, 0.9),
                        "risk_label": random.choice(["low", "medium", "high"]),
                        "timestamp": int(time.time())
                    }
                    msg = json.dumps(payload)
                    disconnected = []
                    # Use a list copy to avoid "Set changed size during iteration"
                    clients_to_notify = list(connected_clients)
                    if clients_to_notify:
                        logger.info(f"SIMULATION: Broadcasting to {len(clients_to_notify)} clients.")
                        for ws in clients_to_notify:
                            try:
                                await ws.send_text(msg)
                            except Exception:
                                disconnected.append(ws)
                    
                    for ws in disconnected:
                        if ws in connected_clients:
                            connected_clients.remove(ws)
                await asyncio.sleep(1.0)
        except Exception as e:
            logger.error(f"FATAL Simulation Loop Error: {e}")
            raise
        return

    try:
        async for msg in consumer:
            payload = msg.value
            if not connected_clients:
                continue
            
            # Broadcast to all connected clients
            disconnected = []
            message = json.dumps(payload)
            # Use a list copy to avoid "Set changed size during iteration"
            clients_to_notify = list(connected_clients)
            if clients_to_notify:
                logger.info(f"Broadcasting to {len(clients_to_notify)} clients: {payload.get('patient_id')}")
                for ws in clients_to_notify:
                    try:
                        await ws.send_text(message)
                    except Exception as e:
                        logger.warning(f"Failed to send to client: {e}")
                        disconnected.append(ws)
            
            # Cleanup disconnected clients
            for ws in disconnected:
                if ws in connected_clients:
                    connected_clients.remove(ws)
                
    finally:
        await consumer.stop()

@app.on_event("startup")
async def startup_event():
    # Start Kafka consumer task
    asyncio.create_task(consume_and_broadcast())

@app.get("/health")
async def health_check():
    return {"status": "healthy", "clients": len(connected_clients)}

@app.websocket("/ws/vitals")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_host = websocket.client.host if websocket.client else "unknown"
    connected_clients.add(websocket)
    logger.info(f"WebSocket client connected from {client_host}. Active connections: {len(connected_clients)}")
    try:
        while True:
            # Keep connection alive, though we mostly send data down-stream
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(connected_clients)}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
