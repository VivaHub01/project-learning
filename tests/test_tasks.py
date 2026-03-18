import pytest
import json
from api_client import TABLE_IDS

class TestTasks:
    def test_tasks_connection(self, client):
        response = client.get_records(TABLE_IDS["tasks"])
        assert response.status_code == 200
        
    def test_tasks_structure(self, client):
        response = client.get_records(TABLE_IDS["tasks"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        tasks = data.get("list", [])
        
        if not tasks:
            pytest.skip("Таблица tasks пуста")
        
        task = tasks[0]
        assert "Id" in task
        
        date_fields = ["Deadline", "CreatedAt", "UpdatedAt", "DueDate"]
        found_dates = [f for f in date_fields if f in task]
    
    def test_tasks_with_deadline(self, client):
        response = client.get_records(TABLE_IDS["tasks"], limit=20)
        data = response.json()
        tasks = data.get("list", [])
        
        if not tasks:
            pytest.skip("Нет задач для проверки")
        
        deadline_count = 0
        date_fields = ["Deadline", "DueDate", "Срок"]
        
        for task in tasks:
            if any(field in task for field in date_fields):
                deadline_count += 1