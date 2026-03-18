#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

mkdir -p trivy-reports
mkdir -p trivy-cache

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   АНАЛИЗ БЕЗОПАСНОСТИ С TRIVY${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}1. Сканирование Docker-образа NocoDB (таблица)${NC}"
docker-compose -f docker-compose.trivy.yml up trivy-scanner

echo -e "\n${YELLOW}2. Сканирование в JSON формате${NC}"
docker-compose -f docker-compose.trivy.yml up trivy-json

echo -e "\n${YELLOW}3. Сканирование файловой системы проекта${NC}"
docker-compose -f docker-compose.trivy.yml up trivy-fs

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}   ОТЧЕТЫ СОХРАНЕНЫ В ./trivy-reports/${NC}"
echo -e "${GREEN}========================================${NC}"
ls -la trivy-reports/