import requests
import json

class NocoDBClient:
    def __init__(self, base_url="http://localhost:8080", token=None):
        self.base_url = base_url
        self.token = token or "Ee-iLvDNs-DPl4L_2x1vhJbpJtwW0xy0ZkQQ4qpq"
        self.headers = {
            "xc-token": self.token,
            "Content-Type": "application/json"
        }
    
    def get_records(self, table_id, view_id=None, limit=100, offset=0, where=""):
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        params = {
            "offset": offset,
            "limit": limit,
            "where": where
        }
        if view_id:
            params["viewId"] = view_id
        
        response = requests.get(url, headers=self.headers, params=params)
        return response
    
    def create_record(self, table_id, data):
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        response = requests.post(url, headers=self.headers, json=data)
        return response
    
    def update_record(self, table_id, record_id, data):
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        payload = {
            "Id": record_id,
            **data
        }
        response = requests.patch(url, headers=self.headers, json=payload)
        return response
    
    def delete_record(self, table_id, record_id):
        url = f"{self.base_url}/api/v2/tables/{table_id}/records"
        payload = {"Id": record_id}
        response = requests.delete(url, headers=self.headers, json=payload)
        return response

TABLE_IDS = {
    "users": "mbey7k2hx6h1hz2",
    "projects": "mhlrv2e3lobieap",
    "teams": "mxsq7xo25e7fqr1",
    "teammembers": "mcm986gfvze2lif",
    "tasks": "moxi4r1y66f8uom",
    "submissions": "m12rr2st3lhfalx"
}