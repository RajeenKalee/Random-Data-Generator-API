import pytest
import json
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5151"

## Setup a Playwright API session ##
@pytest.fixture(scope="session")
def api():
    with sync_playwright() as p:
        request_context = p.request.new_context(
            base_url=BASE_URL,
            extra_http_headers={"Content-Type": "application/json"}  ## Needed for JSON POSTs ##
        )
        yield request_context
        request_context.dispose()

## Create a schema once for shared use across multiple tests ##
@pytest.fixture(scope="session")
def created_schema(api):
    schema = {
        "name": "shortTest",
        "fields": {
            "name": "full_name",           ## Output field "name" will use full_name generator ##
            "email": "email_address"       ## Output field "email" will use email_address generator ##
        },
        "count": 2
    }
    res = api.post("/schemas", data=json.dumps(schema))  ## Playwright needs data= with JSON string ##
    assert res.status == 201
    return schema["name"]

## Test that the root/home endpoint works ##
def test_home(api):
    res = api.get("/")
    assert res.status == 200
    assert "Random Data Generator API is running" in res.json()["message"]

## Test that we can create a new schema via POST ##
def test_create_schema(api):
    schema = {
        "name": "createOnlyTest",
        "fields": {
            "name": "full_name"
        },
        "count": 1
    }
    res = api.post("/schemas", data=json.dumps(schema))
    assert res.status == 201
    assert "created successfully" in res.json()["message"]

## Test that generating data from an existing schema returns valid output ##
def test_run_existing_schema(api, created_schema):
    res = api.get(f"/schemas/{created_schema}/data")  ## RESTful endpoint ##
    assert res.status == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert "name" in data[0] and "email" in data[0]

## Test that trying to run a missing schema returns a 404 ##
def test_run_missing_schema(api):
    res = api.get("/schemas/notThere/data")
    assert res.status == 404
    assert "not found" in res.json()["error"]

## Test NDJSON response format ##
def test_run_schema_ndjson_response(api, created_schema):
    headers = {"Accept": "application/x-ndjson"}
    res = api.get(f"/schemas/{created_schema}/data", headers=headers)
    assert res.status == 200
    lines = res.text().strip().split("\n")
    assert all(line.startswith("{") for line in lines)

## Test listing all schemas ##
def test_list_schemas(api, created_schema):
    res = api.get("/schemas")
    assert res.status == 200
    assert isinstance(res.json(), list)
    assert created_schema in res.json()

## Test schema creation with wrong field types ##
def test_create_schema_with_invalid_field_types(api):
    bad_schema = {
        "name": "badTypes",
        "fields": ["not", "a", "dict"],
        "count": "five"
    }
    res = api.post("/schemas", data=json.dumps(bad_schema))
    assert res.status == 400
    assert "Invalid input" in res.json()["error"]

## Test schema creation missing 'count' field ##
def test_create_schema_missing_fields(api):
    schema = {
        "name": "badSchema",
        "fields": {
            "name": "full_name"
        }
    }
    res = api.post("/schemas", data=json.dumps(schema))
    assert res.status == 400
    assert "Invalid input" in res.json()["error"]
