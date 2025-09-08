import requests
from dataclasses import dataclass

BASE = "https://demoqa.com"

@dataclass
class UserCreds:
    userName: str
    password: str

class BookStoreClient:
    def __init__(self, base_url: str = BASE):
        self.base = base_url.rstrip('/')
        self.session = requests.Session()
        self.token = None

    def create_user(self, creds: UserCreds):
        url = f"{self.base}/Account/v1/User"
        return self.session.post(url, json=creds.__dict__)

    def generate_token(self, creds: UserCreds):
        url = f"{self.base}/Account/v1/GenerateToken"
        resp = self.session.post(url, json=creds.__dict__)
        if resp.status_code == 200 and 'token' in resp.json():
            self.token = resp.json()['token']
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        return resp

    def is_authorized(self, creds: UserCreds):
        url = f"{self.base}/Account/v1/Authorized"
        return self.session.post(url, json=creds.__dict__)

    def get_user(self, user_id: str):
        url = f"{self.base}/Account/v1/User/{user_id}"
        return self.session.get(url)

    def list_books(self):
        url = f"{self.base}/BookStore/v1/Books"
        return self.session.get(url)

    def add_books(self, user_id: str, isbns: list[str]):
        url = f"{self.base}/BookStore/v1/Books"
        payload = {"userId": user_id, "collectionOfIsbns": [{"isbn": i} for i in isbns]}
        return self.session.post(url, json=payload)
