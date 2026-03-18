import pytest
import json
from api_client import TABLE_IDS

class TestSubmissions:
    def test_submissions_connection(self, client):
        response = client.get_records(TABLE_IDS["submissions"])
        assert response.status_code == 200
        
    def test_submissions_structure(self, client):
        response = client.get_records(TABLE_IDS["submissions"], limit=5)
        assert response.status_code == 200
        
        data = response.json()
        submissions = data.get("list", [])
        
        if not submissions:
            pytest.skip("Таблица submissions пуста")
        
        submission = submissions[0]
        assert "Id" in submission
    
    def test_submissions_grades(self, client):
        response = client.get_records(TABLE_IDS["submissions"], limit=20)
        data = response.json()
        submissions = data.get("list", [])
        
        if not submissions:
            pytest.skip("Нет сдач для проверки оценок")
        
        graded = 0
        grade_fields = ["Grade", "Оценка", "grade", "score"]
        
        for sub in submissions:
            for field in grade_fields:
                if field in sub and sub[field] is not None:
                    graded += 1
                    break