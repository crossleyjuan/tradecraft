from locust import HttpLocust, TaskSet, task
import json
import random

json_example = {
    "userId": "A3SGXH7AUHU8GW",
    "profileName": "delmartian",
#    "helpfulness": "1/1 (Fraction of users who found it helpful)",
    "score": 5.0,
    "summary": "Good Quality Dog Food",
    "text": """I have bought several of the Vitality canned dog food products and have
found them all to be of good quality. The product looks more like a stew than
a processed meat and it smells better. My Labrador is finicky and she
appreciates this product better than most."""
}

class UserBehavior(TaskSet):
    products = []
    def on_start(self):
        for x in range(1, 10):
            self.products.append(x)

    @task(1)
    def post(self):
        index = int(random.uniform(0, len(self.products)))
        productId = self.products[index]
        json_example["score"] = int(random.uniform(0, 10))
        self.client.post("/reviews/%d" % productId, data=json.dumps(json_example), headers = {'content-type': 'application/json'})

    @task(2)
    def get(self):
        index = int(random.uniform(0, len(self.products)))
        productId = self.products[index]
        data = self.client.get("/reviews/%d" % productId)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
