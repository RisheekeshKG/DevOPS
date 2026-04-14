# Docker Commands for Real-time Data Ingestion & Clinical Dashboard

## 1) Navigate to the project root
Ensure you are in the directory containing the `Real-time data ingestion` and `DEVOPS_project` folders.

## 2) Build and start all backend services
```bash
cd "Real-time data ingestion"
docker compose up -d --build
```
This command starts:
- **Kafka & Zookeeper**: Real-time message streaming.
- **InfluxDB**: Time-series storage for vitals.
- **App**: The patient telemetry simulator.
- **API Bridge**: WebSocket server for frontend connectivity (Port 8001).
- **Grafana**: Analytical dashboarding (Port 3000).

## 3) Start the React Frontend
Open a new terminal:
```bash
cd "DEVOPS_project/HealthCare_MLOPS"
npm install
npm run dev
```
The dashboard will be available at: `http://localhost:5173`

## 4) Check service status
```bash
docker compose ps
```

## 5) View logs
```bash
docker compose logs -f api-bridge  # WebSocket bridge logs
docker compose logs -f app         # Simulator logs
docker compose logs -f
```

## 6) Common Troubleshooting
If the WebSocket fails to connect:
- Ensure port `8001` is not blocked.
- Check `api-bridge` logs for Kafka connection success.

## 7) Open User Interfaces
- **Clinical Dashboard**: [http://localhost:5173](http://localhost:5173) (Premium Real-time View)
- **Grafana Monitoring**: [http://localhost:3005](http://localhost:3005) (Analytical View, admin/admin)
- **InfluxDB UI**: [http://localhost:8086](http://localhost:8086) (Data Explorer)
- **Kafka UI**: [http://localhost:8081](http://localhost:8081) (Topic Monitoring)

## 8) Stop all services
```bash
docker compose down
```
To remove data volumes as well:
```bash
docker compose down -v
```
