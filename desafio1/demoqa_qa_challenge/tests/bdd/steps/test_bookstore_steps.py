import re
from dataclasses import dataclass, field
from typing import List, Optional

import pytest
from faker import Faker
from pytest_bdd import given, when, then, parsers

from src.api.client import BookStoreClient, UserCreds

fake = Faker()

@dataclass
class Ctx:
    client: Optional[BookStoreClient] = None
    creds: Optional[UserCreds] = None
    user_id: Optional[str] = None
    isbns: List[str] = field(default_factory=list)
    last_response: any = None

@pytest.fixture
def ctx():
    return Ctx()

@given("a new bookstore client")
def _client(ctx, base_url):
    ctx.client = BookStoreClient(base_url)

@given("random valid credentials")
def _valid_creds(ctx):
    username = f"{fake.user_name()}{fake.random_int(1000,9999)}"
    password = f"Aa{fake.random_number(digits=5)}@{fake.lexify(text='????')}"
    ctx.creds = UserCreds(userName=username, password=password)

@given(parsers.parse('invalid credentials with password "{pwd}"'))
def _invalid_creds(ctx, pwd):
    ctx.creds = UserCreds(userName="user_invalid", password=pwd)

@when("I create the user")
def _create_user(ctx):
    resp = ctx.client.create_user(ctx.creds)
    ctx.last_response = resp
    user_id = None
    if resp.headers.get("content-type","").startswith("application/json"):
        try:
            user_id = resp.json().get("userID")
        except Exception:
            user_id = None
    if not user_id:
        m = re.search(r"[0-9a-f-]{36}", resp.text or "")
        if m:
            user_id = m.group(0)
    ctx.user_id = user_id
    assert resp.status_code in (201, 406)
    assert ctx.user_id

@when("I try to create the user")
def _try_create_user(ctx):
    ctx.last_response = ctx.client.create_user(ctx.creds)

@when("I generate a token for the user")
def _gen_token(ctx):
    resp = ctx.client.generate_token(ctx.creds)
    ctx.last_response = resp
    assert resp.status_code == 200
    assert resp.json().get("status") == "Success"
    assert "token" in resp.json()

@then("the user is authorized")
def _authorized(ctx):
    resp = ctx.client.is_authorized(ctx.creds)
    ctx.last_response = resp
    assert resp.status_code == 200
    assert resp.json() is True

@when("I list available books")
def _list_books(ctx):
    resp = ctx.client.list_books()
    ctx.last_response = resp
    assert resp.status_code == 200
    books = resp.json().get("books", [])
    assert len(books) >= 2
    ctx.isbns = [books[0]["isbn"], books[1]["isbn"]]

@when("I add two books to the user")
def _add_books(ctx):
    resp = ctx.client.add_books(ctx.user_id, ctx.isbns)
    ctx.last_response = resp
    assert resp.status_code in (201, 400)

@then("the user should contain those two books")
def _user_contains(ctx):
    resp = ctx.client.get_user(ctx.user_id)
    ctx.last_response = resp
    assert resp.status_code == 200
    found = [b["isbn"] for b in resp.json().get("books", [])]
    for i in ctx.isbns:
        assert i in found

@then(parsers.parse("the response status should be {code:d}"))
def _resp_status(ctx, code):
    assert ctx.last_response.status_code == code

@then(parsers.parse('the error message should contain "{text}"'))
def _resp_contains(ctx, text):
    assert text in ctx.last_response.text
