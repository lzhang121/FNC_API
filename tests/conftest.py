
import pytest
import requests
import os
import json
import allure
from tests.utils.config import load_config
from tests.utils.logger import get_logger

logger = get_logger()

@pytest.fixture(scope="session")
def config(pytestconfig):
    env = pytestconfig.getoption("--env")
    logger.info(f"加载环境配置: {env}")
    return load_config(env)

@pytest.fixture(scope="session")
def base_url(config):
    return config["base_url"]

@pytest.fixture(scope="session")
def auth_token(base_url, config):
    payload = {"user": config["user"], "pwd": config["pwd"]}
    logger.info(f"请求登录接口: {payload}")
    resp = requests.post(f"{base_url}/login", json=payload)
    logger.debug(f"响应: {resp.status_code}, {resp.text}")
    return resp.json()["token"]

@pytest.fixture
def client(base_url, auth_token, request):
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {auth_token}"})

    def request_with_log(method, url, **kwargs):
        full_url = f"{base_url}{url}"
        logger.info(f"请求 {method.upper()} {full_url}")
        if kwargs.get("json"):
            logger.info(f"请求参数: {kwargs['json']}")
        resp = session.request(method, full_url, **kwargs)
        logger.info(f"响应状态码: {resp.status_code}")
        logger.debug(f"响应内容: {resp.text}")
        setattr(request.node, "api_request", {
            "method": method.upper(),
            "url": full_url,
            "payload": kwargs.get("json"),
            "status_code": resp.status_code,
            "response": resp.text
        })
        return resp

    session.request = request_with_log
    return session

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        choices=["dev", "test", "prod"],
        help="运行环境: dev / test / prod (默认 test)"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        failure_dir = os.path.join("logs", "failures")
        os.makedirs(failure_dir, exist_ok=True)
        api_request = getattr(item, "api_request", None)
        if api_request:
            file_path = os.path.join(failure_dir, f"{item.name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(api_request, f, ensure_ascii=False, indent=2)
            allure.attach(
                body=json.dumps(api_request, ensure_ascii=False, indent=2),
                name=f"{item.name}_request_response",
                attachment_type=allure.attachment_type.JSON
            )
            logger.error(f"用例失败，详细请求已保存: {file_path}")
