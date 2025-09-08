import re
from faker import Faker
import pytest
from src.api.client import BookStoreClient, UserCreds

fake = Faker()

@pytest.mark.api
def test_full_bookstore_flow(base_url):
    client = BookStoreClient(base_url)
    username = f"{fake.user_name()}{fake.random_int(1000,9999)}"
    password = f"Aa{fake.random_number(digits=5)}@{fake.lexify(text='????')}"
    creds = UserCreds(userName=username, password=password)

    resp = client.create_user(creds)
    assert resp.status_code in (201, 406)
    user_id = None
    try:
        user_id = resp.json().get("userID")
    except Exception:
        pass
    if not user_id:
        m = re.search(r"[0-9a-f-]{36}", resp.text or "")
        if m:
            user_id = m.group(0)
    assert user_id

    resp = client.generate_token(creds)
    assert resp.status_code == 200
    assert resp.json().get("status") == "Success"
    assert "token" in resp.json()

    resp = client.is_authorized(creds)
    assert resp.status_code == 200
    assert resp.json() is True

    resp = client.list_books()
    assert resp.status_code == 200
    books = resp.json().get("books", [])
    assert len(books) >= 2
    isbns = [books[0]["isbn"], books[1]["isbn"]]

    resp = client.add_books(user_id, isbns)
    assert resp.status_code in (201, 400)

    resp = client.get_user(user_id)
    assert resp.status_code == 200
    user_isbns = [b["isbn"] for b in resp.json().get("books", [])]
    for i in isbns:
        assert i in user_isbns

@pytest.mark.api
def test_negative_password_rule(base_url):
    client = BookStoreClient(base_url)
    creds = UserCreds(userName="user_invalid", password="abcd1234")
    resp = client.create_user(creds)
    assert resp.status_code == 400
    assert "Passwords must have" in resp.text
