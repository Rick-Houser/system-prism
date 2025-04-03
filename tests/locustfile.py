from locust import HttpUser, task, between

class FlaskUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def get_tasks(self):
        self.client.get("/tasks")

    @task
    def add_task(self):
        self.client.post("/tasks", json={"task": "Load test task"})