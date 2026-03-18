from locust import HttpUser, task, between
import random

class ProjectsOnlyUser(HttpUser):
    wait_time = between(1, 3)
    token = "Ee-iLvDNs-DPl4L_2x1vhJbpJtwW0xy0ZkQQ4qpq"
    
    def on_start(self):
        self.headers = {"xc-token": self.token, "Content-Type": "application/json"}
        self.table_id = "mhlrv2e3lobieap"
    
    @task(8)
    def get_projects(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0}
        )
    
    @task(2)
    def get_active_projects(self):
        self.client.get(
            f"/api/v2/tables/{self.table_id}/records",
            headers=self.headers,
            params={"where": "(Status,eq,active)", "limit": 20}
        )