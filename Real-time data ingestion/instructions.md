# Docker Commands for Real-time Data Ingestion

## 1) Go to project folder
```bash
cd "/Users/risheekeshkg/Documents/Project Work/DevOPS/Real-time data ingestion"
```

## 2) Build and start all services
```bash
docker compose up -d --build
```

## 3) Check service status
```bash
docker compose ps
```

## 4) View logs
```bash
docker compose logs -f app
docker compose logs -f kafka
docker compose logs -f influxdb
docker compose logs -f
```

## 5) Start only app service (if infra already running)
```bash
docker compose up -d app
```

This app is configured to run continuously by default. If you want a finite run, set `WORKFLOW_DURATION_SECONDS` to a positive number in `docker-compose.yml` or your shell before starting it.

## 6) Rebuild only app service
```bash
docker compose up -d --build app
```

## 7) Restart one service
```bash
docker compose restart app
```

## 8) Stop all services
```bash
docker compose stop
```

## 9) Stop and remove containers/network
```bash
docker compose down
```

## 10) Full reset (removes volumes too)
```bash
docker compose down -v
```

## 11) Open UIs
- InfluxDB: http://localhost:8086
- Kafka UI: http://localhost:8080

## 12) Common quick recovery
```bash
docker compose down
docker compose up -d --build
docker compose logs -f app
```
