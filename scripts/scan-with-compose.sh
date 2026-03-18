#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

mkdir -p trivy-reports

echo -e "${GREEN}Запуск Trivy через Docker Compose${NC}"

echo -e "${YELLOW}Сканирование образа nocodb/nocodb:latest${NC}"
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/trivy-reports:/reports \
  aquasec/trivy:latest \
  image --severity=CRITICAL,HIGH --format=table \
  --output=/reports/trivy-output.txt \
  nocodb/nocodb:latest

echo -e "${YELLOW}Сканирование Python зависимостей${NC}"
docker run --rm \
  -v $(pwd):/project \
  -v $(pwd)/trivy-reports:/reports \
  aquasec/trivy:latest \
  fs --severity=CRITICAL,HIGH --format=table \
  --output=/reports/trivy-fs.txt \
  /project

echo -e "${GREEN}Отчеты сохранены в ./trivy-reports/${NC}"
ls -la trivy-reports/