param(
    [Parameter(Position=0)]
    [string]$Mode = "web"
)

$GREEN = "Green"
$YELLOW = "Yellow"

Write-Host "========================================" -ForegroundColor $GREEN
Write-Host "   ЗАПУСК НАГРУЗОЧНОГО ТЕСТИРОВАНИЯ" -ForegroundColor $GREEN
Write-Host "========================================" -ForegroundColor $GREEN

New-Item -ItemType Directory -Force -Path "locust-reports" | Out-Null

switch ($Mode) {
    "web" {
        Write-Host "Запуск Locust с веб-интерфейсом..." -ForegroundColor $YELLOW
        locust -f locust/locustfile.py --host=http://localhost:8080
    }
    "headless" {
        Write-Host "Запуск Locust в фоновом режиме..." -ForegroundColor $YELLOW
        locust -f locust/locustfile.py --headless -u 50 -r 5 --run-time 2m --host=http://localhost:8080 --csv=locust-reports/report
    }
    "docker" {
        Write-Host "Запуск Locust через Docker Compose..." -ForegroundColor $YELLOW
        docker-compose -f docker-compose.locust.yml up
    }
    "users" {
        Write-Host "Запуск теста только для users..." -ForegroundColor $YELLOW
        locust -f locust/locustfile_users.py --host=http://localhost:8080
    }
    "mixed" {
        Write-Host "Запуск смешанного теста..." -ForegroundColor $YELLOW
        locust -f locust/locustfile_mixed.py --host=http://localhost:8080
    }
    "report" {
        Write-Host "Генерация отчета..." -ForegroundColor $YELLOW
        python scripts/generate-locust-report.py
    }
    default {
        Write-Host "Использование: run-locust.ps1 {web|headless|docker|users|mixed|report}"
    }
}