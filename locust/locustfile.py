from locust import HttpUser, task, between
import random
import json

class NocoDBUser(HttpUser):
    wait_time = between(1, 3)
    token = "Ee-iLvDNs-DPl4L_2x1vhJbpJtwW0xy0ZkQQ4qpq"
    
    def on_start(self):
        self.headers = {
            "xc-token": self.token,
            "Content-Type": "application/json"
        }
        self.table_ids = {
            "users": "mbey7k2hx6h1hz2",
            "projects": "mhlrv2e3lobieap",
            "teams": "mxsq7xo25e7fqr1",
            "teammembers": "mcm986gfvze2lif",
            "tasks": "moxi4r1y66f8uom",
            "submissions": "m12rr2st3lhfalx"
        }
    
    @task(5)
    def get_users(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['users']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /users"
        )
    
    @task(4)
    def get_projects(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['projects']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /projects"
        )
    
    @task(3)
    def get_teams(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['teams']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /teams"
        )
    
    @task(3)
    def get_tasks(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['tasks']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /tasks"
        )
    
    @task(2)
    def get_submissions(self):
        self.client.get(
            f"/api/v2/tables/{self.table_ids['submissions']}/records",
            headers=self.headers,
            params={"limit": 20, "offset": 0},
            name="GET /submissions"
        )
    
    @task(1)
    def search_users(self):
        emails = ["ivan", "anna", "alex", "elena", "dmitry", "petr", "olga"]
        self.client.get(
            f"/api/v2/tables/{self.table_ids['users']}/records",
            headers=self.headers,
            params={"where": f"(Email,like,%{random.choice(emails)}%)", "limit": 10},
            name="GET /users/search"
        )