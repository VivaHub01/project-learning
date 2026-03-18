#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

mkdir -p locust-reports

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   ЗАПУСК НАГРУЗОЧНОГО ТЕСТИРОВАНИЯ${NC}"
echo -e "${GREEN}========================================${NC}"

case $1 in
  web)
    echo -e "${YELLOW}Запуск Locust с веб-интерфейсом...${NC}"
    locust -f locust/locustfile.py --host=http://localhost:8080
    ;;
  headless)
    echo -e "${YELLOW}Запуск Locust в фоновом режиме...${NC}"
    locust -f locust/locustfile.py --headless -u 50 -r 5 --run-time 2m --host=http://localhost:8080 --csv=locust-reports/report
    ;;
  docker)
    echo -e "${YELLOW}Запуск Locust через Docker Compose...${NC}"
    docker-compose -f docker-compose.locust.yml up
    ;;
  users)
    echo -e "${YELLOW}Запуск теста только для users...${NC}"
    locust -f locust/locustfile_users.py --host=http://localhost:8080
    ;;
  mixed)
    echo -e "${YELLOW}Запуск смешанного теста...${NC}"
    locust -f locust/locustfile_mixed.py --host=http://localhost:8080
    ;;
  report)
    echo -e "${YELLOW}Генерация отчета...${NC}"
    python scripts/generate-locust-report.py
    ;;
  *)
    echo "Использование: $0 {web|headless|docker|users|mixed|report}"
    ;;
esac