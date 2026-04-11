#!/bin/bash
# ========================================
# Deployment Script for Patient Monitoring System
# Usage: ./deploy.sh [production|staging]
# ========================================

set -e

# Configuration
ENVIRONMENT=${1:-production}
DEPLOY_DIR="/opt/patient-monitoring"
DOCKER_COMPOSE_FILE="$DEPLOY_DIR/docker-compose.yml"
BACKUP_DIR="$DEPLOY_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Patient Monitoring System Deployment${NC}"
echo -e "${GREEN}Environment: $ENVIRONMENT${NC}"
echo -e "${GREEN}Timestamp: $TIMESTAMP${NC}"
echo -e "${GREEN}========================================${NC}"

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}⚠️  This script requires sudo privileges${NC}"
    echo "Please run with: sudo $0 $ENVIRONMENT"
    exit 1
fi

# Step 1: Create backup
echo -e "\n${YELLOW}📦 Step 1: Creating backup...${NC}"
mkdir -p "$BACKUP_DIR"
if [ -f "$DOCKER_COMPOSE_FILE" ]; then
    cp "$DOCKER_COMPOSE_FILE" "$BACKUP_DIR/docker-compose.yml.$TIMESTAMP"
    echo "✅ Backup created: docker-compose.yml.$TIMESTAMP"
else
    echo "⚠️  No existing docker-compose.yml found, skipping backup"
fi

# Step 2: Pull latest Docker image
echo -e "\n${YELLOW}📥 Step 2: Pulling latest Docker image...${NC}"
cd "$DEPLOY_DIR"
docker compose pull app

# Step 3: Rebuild and restart app
echo -e "\n${YELLOW}🔨 Step 3: Rebuilding and starting services...${NC}"
docker compose up -d --build app

# Step 4: Wait for app to initialize
echo -e "\n${YELLOW}⏳ Step 4: Waiting for app to initialize (15s)...${NC}"
sleep 15

# Step 5: Health check
echo -e "\n${YELLOW}🏥 Step 5: Running health checks...${NC}"

# Check if container is running
if docker compose ps app --format json | grep -q "running"; then
    echo -e "${GREEN}✅ App container is running${NC}"
else
    echo -e "${RED}❌ App container is NOT running${NC}"
    echo -e "${YELLOW}Recent logs:${NC}"
    docker compose logs --tail=50 app
    exit 1
fi

# Check app logs for successful initialization
echo -e "\n${YELLOW}📋 Checking app logs...${NC}"
docker compose logs --tail=20 app

# Check if Kafka is reachable (basic check)
echo -e "\n${YELLOW}🔌 Checking Kafka connectivity...${NC}"
docker compose exec -T app python -c "
from kafka import KafkaProducer
import os
try:
    producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    producer.close()
    print('✅ Kafka connection successful')
except Exception as e:
    print(f'❌ Kafka connection failed: {e}')
    exit(1)
" || echo -e "${YELLOW}⚠️  Kafka check skipped or failed${NC}"

# Check if InfluxDB is reachable
echo -e "\n${YELLOW}🔌 Checking InfluxDB connectivity...${NC}"
docker compose exec -T app python -c "
import urllib.request
import os
try:
    url = os.getenv('INFLUXDB_URL', 'http://influxdb:8086')
    req = urllib.request.Request(f'{url}/ping')
    with urllib.request.urlopen(req, timeout=5):
        print('✅ InfluxDB connection successful')
except Exception as e:
    print(f'❌ InfluxDB connection failed: {e}')
    exit(1)
" || echo -e "${YELLOW}⚠️  InfluxDB check skipped or failed${NC}"

# Step 6: Show service status
echo -e "\n${YELLOW}📊 Final Service Status:${NC}"
docker compose ps

# Step 7: Display access URLs
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Deployment Completed Successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n📍 Access URLs:"
echo -e "   Grafana:     http://$(hostname -I | awk '{print $1}'):3000 (admin/admin)"
echo -e "   InfluxDB:    http://$(hostname -I | awk '{print $1}'):8086 (admin/admin12345)"
echo -e "   Kafka UI:    http://$(hostname -I | awk '{print $1}'):8081"
echo -e "\n📝 Useful commands:"
echo -e "   View logs:        docker compose logs -f app"
echo -e "   Restart app:      docker compose restart app"
echo -e "   Check status:     docker compose ps"
echo -e "   Stop services:    docker compose down"
echo -e "\n"
