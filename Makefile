.PHONY: trivy-scan trivy-image trivy-fs trivy-json trivy-report

trivy-scan:
	@echo "🔍 Запуск Trivy сканирования..."
	@mkdir -p trivy-reports
	docker run --rm \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD)/trivy-reports:/reports \
		aquasec/trivy:latest \
		image --severity=CRITICAL,HIGH \
		--output=/reports/trivy-report.txt \
		nocodb/nocodb:latest

trivy-image:
	@echo "🔍 Сканирование Docker образа..."
	@mkdir -p trivy-reports
	docker run --rm \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD)/trivy-reports:/reports \
		aquasec/trivy:latest \
		image --severity=CRITICAL,HIGH,MEDIUM \
		--format=json \
		--output=/reports/trivy-image.json \
		nocodb/nocodb:latest

trivy-fs:
	@echo "🔍 Сканирование файловой системы..."
	@mkdir -p trivy-reports
	docker run --rm \
		-v $(PWD):/project \
		-v $(PWD)/trivy-reports:/reports \
		aquasec/trivy:latest \
		fs --severity=CRITICAL,HIGH \
		--output=/reports/trivy-fs.txt \
		/project

trivy-json:
	@echo "🔍 Сканирование в JSON формате..."
	@mkdir -p trivy-reports
	docker run --rm \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD)/trivy-reports:/reports \
		aquasec/trivy:latest \
		image --severity=CRITICAL,HIGH \
		--format=json \
		--output=/reports/trivy-report.json \
		nocodb/nocodb:latest

trivy-report:
	@echo "📊 Просмотр отчета..."
	@cat trivy-reports/trivy-report.txt 2>/dev/null || echo "Отчет не найден"

trivy-clean:
	@echo "🧹 Очистка отчетов..."
	@rm -rf trivy-reports/*