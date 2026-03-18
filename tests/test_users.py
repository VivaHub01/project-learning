import pytest
import json
from api_client import TABLE_IDS

class TestUsers:
    def test_users_connection(self, client):
        response = client.get_records(TABLE_IDS["users"])
        assert response.status_code == 200
        
    def test_users_structure(self, client):
        response = client.get_records(TABLE_IDS["users"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        records = data.get("list", [])
        
        if len(records) == 0:
            pytest.skip("Таблица users пуста")
        
        user = records[0]
        assert "Id" in user
        
        expected_fields = ["Email", "Name", "Role", "Group", "Department"]
        found_fields = [f for f in expected_fields if f in user]
        assert len(found_fields) > 0
    
    def test_users_data_quality(self, client):
        response = client.get_records(TABLE_IDS["users"], limit=20)
        data = response.json()
        users = data.get("list", [])
        
        if not users:
            pytest.skip("Таблица users пуста")
        
        email_count = 0
        name_count = 0
        
        for user in users:
            if "Email" in user and user["Email"]:
                email_count += 1
            if "Name" in user and user["Name"]:
                name_count += 1
        
        assert email_count > 0 or name_count > 0