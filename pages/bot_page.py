import requests

BASE_URL = "http://localhost:5000"

class BotPage:
    def __init__(self):
        self.base_url = BASE_URL

    def create_bot(self, name, url):
        response = requests.post(f"{self.base_url}/bot/{name}", json={"url": url})
        return response

    def get_bot(self, name):
        response = requests.get(f"{self.base_url}/bot/{name}")
        return response

    def update_bot(self, name, intents):
        response = requests.put(f"{self.base_url}/bot/{name}", json={"intents": intents})
        return response

    def patch_bot(self, name, url):
        response = requests.patch(f"{self.base_url}/bot/{name}", json={"url": url})
        return response

    def delete_bot(self, name):
        response = requests.delete(f"{self.base_url}/bot/{name}")
        return response
