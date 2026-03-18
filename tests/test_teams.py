import pytest
import json
from api_client import TABLE_IDS

class TestTeams:
    def test_teams_connection(self, client):
        response = client.get_records(TABLE_IDS["teams"])
        assert response.status_code == 200
        
    def test_teams_structure(self, client):
        response = client.get_records(TABLE_IDS["teams"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        teams = data.get("list", [])
        
        if not teams:
            pytest.skip("Таблица teams пуста")
        
        team = teams[0]
        assert "Id" in team
        
        name_fields = ["Name", "name", "Название", "Title"]
        has_name = any(f in team for f in name_fields)
    
    def test_teams_members_relation(self, client):
        teams_response = client.get_records(TABLE_IDS["teams"], limit=5)
        teams_data = teams_response.json()
        teams = teams_data.get("list", [])
        
        if not teams:
            pytest.skip("Нет команд для тестирования")
        
        members_response = client.get_records(TABLE_IDS["teammembers"], limit=20)
        members_data = members_response.json()
        members = members_data.get("list", [])