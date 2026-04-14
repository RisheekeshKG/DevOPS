import asyncio
import json
import random
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = set()

async def broadcast_mock_data():
    patients = ["P001", "P002", "P003"]
    while True:
        if connected_clients:
            for pid in patients:
                data = {
                    "patient_id": pid,
                    "hr": random.randint(60, 110),
                    "spo2": random.randint(90, 100),
                    "temp": round(random.uniform(36.1, 38.5), 1),
                    "bp_sys": random.randint(110, 140),
                    "bp_dia": random.randint(70, 90),
                    "risk_score": random.random(),
                    "risk_label": random.choice(["low", "medium", "high"]),
                    "timestamp": int(time.time())
                }
                # Broadcast
                message = json.dumps(data)
                for ws in list(connected_clients):
                    try:
                        await ws.send_text(message)
                    except:
                        connected_clients.remove(ws)
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup():
    asyncio.create_task(broadcast_mock_data())

@app.websocket("/ws/vitals")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
