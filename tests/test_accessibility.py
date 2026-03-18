import pytest
from api_client import TABLE_IDS

@pytest.mark.parametrize("table_name", ["users", "projects", "teams", "teammembers", "tasks", "submissions"])
def test_table_accessible(client, table_name):
    response = client.get_records(TABLE_IDS[table_name], limit=1)
    assert response.status_code == 200

@pytest.mark.parametrize("table_name,expected_min_records", [
    ("users", 1),
    ("projects", 0),
    ("teams", 0),
    ("teammembers", 0),
    ("tasks", 0),
    ("submissions", 0),
])
def test_table_has_min_records(client, table_name, expected_min_records):
    response = client.get_records(TABLE_IDS[table_name], limit=10)
    assert response.status_code == 200
    
    data = response.json()
    records = data.get("list", [])
    actual_records = len(records)