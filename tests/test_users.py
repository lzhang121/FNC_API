
import pytest
from tests.utils.loader import load_yaml

test_data = load_yaml("users.yaml")

@pytest.mark.parametrize("role", ["admin", "enterprise", "personal"], indirect=True)
def test_get_user_info(client, role):
    resp = client.get("/admin-api/user/info")
    assert resp.status_code == 200
    print(resp.json())
