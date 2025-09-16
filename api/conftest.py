import pytest
import requests
import json
from lib.utils.config import load_config
from lib.utils.logger import get_logger
from lib.utils.http_client import create_logged_session

logger = get_logger()

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        choices=["dev", "test", "prod"],
        help="运行环境: dev / test / prod"
    )

@pytest.fixture(scope="session")
def config(pytestconfig):
    env = pytestconfig.getoption("--env")
    return load_config(env)

@pytest.fixture
def auth_token(config, request):
    role = getattr(request, "param", "admin")
    username = config["users"][role]["username"]
    password = config["users"][role]["password"]

    login_url = f"{config['base_url'].rstrip('/')}/admin-api/auth/auth/login"
    payload = json.dumps({"username": username, "password": password})
    headers = {"Content-Type": "application/json"}

    resp = requests.post(login_url, headers=headers, data=payload)
    resp.raise_for_status()
    return resp.json().get("data", {}).get("token").get("accessToken")

@pytest.fixture
def client(auth_token, config):
    return create_logged_session(config['base_url'], auth_token)
