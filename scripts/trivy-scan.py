#!/usr/bin/env python3
import subprocess
import json
import sys
import os
from datetime import datetime

class TrivyScanner:
    def __init__(self):
        self.report_dir = "trivy-reports"
        os.makedirs(self.report_dir, exist_ok=True)
        
    def scan_image(self, image="nocodb/nocodb:latest", severity="CRITICAL,HIGH"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.report_dir, f"trivy_{timestamp}.json")
        
        abs_report_dir = os.path.abspath(self.report_dir)
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"/var/run/docker.sock:/var/run/docker.sock",
            "-v", f"{abs_report_dir}:/reports",
            "aquasec/trivy:latest",
            "image",
            "--severity", severity,
            "--format", "json",
            "--output", f"/reports/trivy_{timestamp}.json",
            image
        ]
        
        print(f"Выполняется: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Сканирование завершено. Отчет: {output_file}")
                return output_file
            else:
                print(f"❌ Ошибка сканирования: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print("❌ Таймаут сканирования")
            return None
        except FileNotFoundError:
            print("❌ Docker не найден. Установите Docker Desktop")
            return None
    
    def scan_filesystem(self, path=".", severity="CRITICAL,HIGH"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.report_dir, f"trivy_fs_{timestamp}.json")
        
        abs_path = os.path.abspath(path)
        abs_report_dir = os.path.abspath(self.report_dir)
        
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{abs_path}:/project",
            "-v", f"{abs_report_dir}:/reports",
            "aquasec/trivy:latest",
            "fs",
            "--severity", severity,
            "--format", "json",
            "--output", f"/reports/trivy_fs_{timestamp}.json",
            "/project"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ Сканирование ФС завершено. Отчет: {output_file}")
                return output_file
            else:
                print(f"❌ Ошибка сканирования ФС: {result.stderr}")
                return None
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            return None
    
    def analyze_report(self, report_file):
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            results = []
            for result in data.get("Results", []):
                for vuln in result.get("Vulnerabilities", []):
                    results.append({
                        "package": vuln.get("PkgName"),
                        "severity": vuln.get("Severity"),
                        "installed": vuln.get("InstalledVersion"),
                        "fixed": vuln.get("FixedVersion", "Not fixed"),
                        "title": vuln.get("Title", ""),
                    })
            return results
        except Exception as e:
            print(f"❌ Ошибка анализа отчета: {e}")
            return []

def main():
    scanner = TrivyScanner()
    
    print("=" * 50)
    print("СКАНИРОВАНИЕ БЕЗОПАСНОСТИ TRIVY")
    print("=" * 50)
    
    print("\n1. Сканирование Docker-образа nocodb/nocodb:latest...")
    report = scanner.scan_image()
    
    if report and os.path.exists(report):
        vulns = scanner.analyze_report(report)
        
        critical = sum(1 for v in vulns if v["severity"] == "CRITICAL")
        high = sum(1 for v in vulns if v["severity"] == "HIGH")
        medium = sum(1 for v in vulns if v["severity"] == "MEDIUM")
        
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ")
        print("=" * 50)
        print(f"Всего уязвимостей: {len(vulns)}")
        print(f"  CRITICAL: {critical}")
        print(f"  HIGH: {high}")
        print(f"  MEDIUM: {medium}")
        
        if critical > 0:
            print("\nКРИТИЧЕСКИЕ УЯЗВИМОСТИ:")
            for v in vulns:
                if v["severity"] == "CRITICAL":
                    print(f"  - {v['package']}: {v['installed']} -> {v['fixed']}")
        
        print(f"\n📁 Отчет сохранен: {report}")
    else:
        print("\n❌ Сканирование не удалось")
        print("\nВозможные причины:")
        print("  - Docker Desktop не запущен")
        print("  - Нет доступа к Docker socket")
        print("  - Проблемы с сетью")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Сканирование прервано пользователем")
        sys.exit(1)