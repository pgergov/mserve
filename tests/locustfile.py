from faker import Faker
from locust import HttpUser, TaskSet, task, between

fake = Faker()


class ModelServingTaskSet(TaskSet):
    @task
    def vectorise(self):
        headers = {"Content-Type": "application/json"}
        # 250 words will vary between 1200 and 1800 characters
        text = fake.sentence(nb_words=250, variable_nb_words=True)
        payload = {"text": text}
        self.client.post("/vectorise", json=payload, headers=headers)

    @task
    def rerank(self):
        headers = {"Content-Type": "application/json"}
        query = "What is the best way to learn Python? How can I learn Python quickly?"
        # 250 words will vary between 1200 and 1800 characters
        segment = fake.sentence(nb_words=250, variable_nb_words=True)
        payload = {"pair": [query, segment]}
        self.client.post("/rerank", json=payload, headers=headers)


class ModelUser(HttpUser):
    tasks = [ModelServingTaskSet]
    wait_time = between(0.1, 0.2)
    host = "http://localhost:8080"
