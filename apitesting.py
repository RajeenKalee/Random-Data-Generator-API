import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5000"

@pytest.fixture(scope="session")
def api():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        yield request_context
        request_context.dispose()

@pytest.fixture(scope="session")
def created_schema(api):
    schema = {
        "name": "shortTest",
        "fields": {"name": "name", "email": "email"},
        "count": 2
    }
    res = api.post(f"{BASE_URL}/schemas", data=schema)
    assert res.status == 201
    return schema["name"]

def test_home(api):
    res = api.get(f"{BASE_URL}/")
    assert res.status == 200
    assert "Random Data Generator API is running" in res.json()["message"]

def test_create_schema(api):
    schema = {
        "name": "createOnlyTest",
        "fields": {"name": "name"},
        "count": 1
    }
    res = api.post(f"{BASE_URL}/schemas", data=schema)
    assert res.status == 201
    assert "created successfully" in res.json()["message"]

def test_run_existing_schema(api, created_schema):
    res = api.get(f"{BASE_URL}/schemas/{created_schema}/run")
    assert res.status == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "name" in data[0] and "email" in data[0]

def test_run_missing_schema(api):
    res = api.get(f"{BASE_URL}/schemas/notThere/run")
    assert res.status == 404
    assert "not found" in res.json()["error"]
