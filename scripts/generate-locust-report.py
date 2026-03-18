import csv
import json
import os
from datetime import datetime

def generate_report():
    report_dir = "locust-reports"
    if not os.path.exists(report_dir):
        print("❌ Отчеты не найдены")
        return
    
    csv_files = [f for f in os.listdir(report_dir) if f.endswith('_stats.csv')]
    if not csv_files:
        print("❌ CSV файлы не найдены")
        return
    
    latest_csv = max(csv_files, key=lambda f: os.path.getctime(os.path.join(report_dir, f)))
    csv_path = os.path.join(report_dir, latest_csv)
    
    stats = {
        "total_requests": 0,
        "failures": 0,
        "avg_response_time": 0,
        "requests_per_second": 0,
        "endpoints": []
    }
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stats["total_requests"] += int(row["Request Count"])
            stats["failures"] += int(row["Failure Count"])
            stats["endpoints"].append({
                "name": row["Name"],
                "requests": int(row["Request Count"]),
                "failures": int(row["Failure Count"]),
                "avg_ms": float(row["Average Response Time"]),
                "min_ms": float(row["Min Response Time"]),
                "max_ms": float(row["Max Response Time"]),
                "rps": float(row["Requests/s"])
            })
    
    if stats["endpoints"]:
        stats["avg_response_time"] = sum(e["avg_ms"] for e in stats["endpoints"]) / len(stats["endpoints"])
        stats["requests_per_second"] = sum(e["rps"] for e in stats["endpoints"])
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "source_file": latest_csv,
        "statistics": stats
    }
    
    report_file = os.path.join(report_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "="*50)
    print("ОТЧЕТ О НАГРУЗОЧНОМ ТЕСТИРОВАНИИ")
    print("="*50)
    print(f"Всего запросов: {stats['total_requests']}")
    print(f"Ошибок: {stats['failures']} ({stats['failures']/stats['total_requests']*100:.2f}%)")
    print(f"Ср. время ответа: {stats['avg_response_time']:.2f} мс")
    print(f"Запросов/сек: {stats['requests_per_second']:.2f}")
    print("\nДетали по endpoints:")
    for e in stats["endpoints"]:
        print(f"  {e['name']}: {e['requests']} запр, {e['avg_ms']:.1f} мс")
    print(f"\n📁 Отчет сохранен: {report_file}")

if __name__ == "__main__":
    generate_report()