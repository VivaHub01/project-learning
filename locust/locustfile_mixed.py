from locust import FastHttpUser, task, between
import random

class MixedLoadUser(FastHttpUser):
    wait_time = between(0.1, 1)
    token = "Ee-iLvDNs-DPl4L_2x1vhJbpJtwW0xy0ZkQQ4qpq"
    
    def on_start(self):
        self.headers = {"xc-token": self.token}
        self.tables = [
            ("users", "mbey7k2hx6h1hz2"),
            ("projects", "mhlrv2e3lobieap"),
            ("teams", "mxsq7xo25e7fqr1"),
            ("tasks", "moxi4r1y66f8uom"),
        ]
    
    @task
    def random_get(self):
        name, table_id = random.choice(self.tables)
        self.client.get(
            f"/api/v2/tables/{table_id}/records",
            headers=self.headers,
            params={"limit": random.randint(5, 50)},
            name=f"GET /{name}"
        )