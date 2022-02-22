from locust import HttpUser, task


class ApiUser(HttpUser):
    @task
    def test_get_joke(self):
        self.client.get("/joke")
