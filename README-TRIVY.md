# Анализ безопасности с Trivy

## Быстрый старт

### Через Docker Compose
```bash
# Запустить все сканирования
docker-compose -f docker-compose.trivy.yml up

# Просмотреть результаты
cat trivy-reports/trivy-report.txt