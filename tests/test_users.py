
import pytest
from tests.utils.loader import load_yaml

test_data = load_yaml("users.yaml")

@pytest.mark.parametrize("case", test_data["get_user"])
def test_get_user_info(client, case):
    resp = client.get(f"/users/{case['id']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == case["id"]
    assert resp.json()["name"] == case["expected_name"]

@pytest.mark.parametrize("case", test_data["create_user"])
def test_create_user(client, case):
    payload = {"name": case["name"], "email": case["email"]}
    resp = client.post("/users", json=payload)
    assert resp.status_code == case["expected_status"]
    assert resp.json()["name"] == case["name"]
