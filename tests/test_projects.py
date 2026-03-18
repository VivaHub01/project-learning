import pytest
import json
from api_client import TABLE_IDS

class TestProjects:
    def test_projects_connection(self, client):
        response = client.get_records(TABLE_IDS["projects"])
        assert response.status_code == 200
        
    def test_projects_structure(self, client):
        response = client.get_records(TABLE_IDS["projects"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        projects = data.get("list", [])
        
        if not projects:
            pytest.skip("Таблица projects пуста")
        
        project = projects[0]
        assert "Id" in project
        
        descriptive_fields = ["Title", "Description", "Name", "Название", "Описание"]
        found_descriptive = [f for f in descriptive_fields if f in project]
    
    def test_projects_required_fields(self, client):
        response = client.get_records(TABLE_IDS["projects"], limit=10)
        data = response.json()
        projects = data.get("list", [])
        
        if not projects:
            pytest.skip("Таблица projects пуста")
        
        for project in projects:
            assert "Id" in project