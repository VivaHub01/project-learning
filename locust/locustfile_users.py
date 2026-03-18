from locust import HttpUser, task, between
import random

class UsersOnlyUser(HttpUser):
    wait_time = between(0.5, 2)
    token = "Ee-iLvDNs-DPl4L_2x1vhJbpJtwW0xy0ZkQQ4qpq"
    
    def on_start(self):
        self.headers = {"xc-token": self.token, "Content-Type": "application/json"}
        self.table_id = "mbey7k2hx6h1hz2"
    
    @task(10)
    def get_users(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"limit": 50, "offset": 0}
        )
    
    @task(5)
    def get_user_by_id(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"where": "(Id,eq,1)", "limit": 1}
        )
    
    @task(3)
    def search_by_email(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"where": "(Email,like,%test%)", "limit": 10}
        )