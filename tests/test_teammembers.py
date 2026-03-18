import pytest
import json
from api_client import TABLE_IDS

class TestTeamMembers:
    def test_teammembers_connection(self, client):
        response = client.get_records(TABLE_IDS["teammembers"])
        assert response.status_code == 200
        
    def test_teammembers_structure(self, client):
        response = client.get_records(TABLE_IDS["teammembers"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        members = data.get("list", [])
        
        if not members:
            pytest.skip("Таблица teammembers пуста")
        
        member = members[0]
        assert "Id" in member
    
    def test_teammembers_roles(self, client):
        response = client.get_records(TABLE_IDS["teammembers"], limit=20)
        data = response.json()
        members = data.get("list", [])
        
        if not members:
            pytest.skip("Нет участников для проверки ролей")
        
        role_fields = ["RoleInTeam", "Role", "role", "position"]
        for member in members[:5]:
            for field in role_fields:
                if field in member:
                    break