# coding: utf-8
import requests
from mytask import UserMeta, task


class QuickstartUser(metaclass=UserMeta):
    """
    locust file demo. 

    cmd:
    locust -f locust_demo.py --list
    locust -f locust_demo.py --show-task-ratio
    """

    wait_time = 1

    def __init__(self):
        self.client = requests

    def on_start(self):
        self.client.post("/login", json={"username": "foo", "password": "bar"})

    @task
    def foo(self):
        print(type(self))
        print('foo')

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_item(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
