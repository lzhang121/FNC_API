import pytest
import json
from lib.utils.config import load_config
from lib.utils.logger import get_logger
from lib.utils.http_client import ApiClient # 导入我们新的类

logger = get_logger()

# --- 这部分保持不变 ---
def pytest_addoption(parser):
    parser.addoption(
        "--env", action="store", default="test01",
        choices=["test01", "test03", "prod"], help="运行环境"
    )

@pytest.fixture(scope="session")
def config(pytestconfig):
    env = pytestconfig.getoption("--env")
    return load_config(env)
# --- 不变的部分结束 ---


# 创建一个 session 级别的缓存
@pytest.fixture(scope="session")
def clients_cache():
    return {}

@pytest.fixture(scope="function") # 依然是 function 级别，但内部逻辑会使用缓存
def client(config, clients_cache, request):
    # 默认角色为 admin，或从 parametrize 中获取
    role = getattr(request, "param", "admin")

    # 如果该角色的 client 已在缓存中，直接返回
    if role in clients_cache:
        logger.info(f"从缓存中复用 '{role}' 角色的 client")
        return clients_cache[role]

    # --- 如果缓存中没有，则执行登录并创建 client ---
    logger.info(f"为 '{role}' 角色创建新的 client")
    base_url = config['base_url']
    
    # 检查密码是否存在，避免因环境变量缺失而出错
    try:
        username = config["users"][role]["username"]
        password = config["users"][role]["password"]
        if not password:
            raise ValueError(f"'{role}' 角色的密码未设置，请检查环境变量。")
    except KeyError:
        pytest.fail(f"配置中未找到 '{role}' 用户的信息。")

    # 使用一个临时的、无 token 的 client 来执行登录
    login_client = ApiClient(base_url=base_url)
    login_payload = {"username": username, "password": password}
    
    resp = login_client.post("/admin-api/auth/auth/login", json=login_payload)
    resp.raise_for_status() # 如果登录失败则抛出异常
    
    token = resp.json()["data"]["token"]["accessToken"]
    
    # 创建带 token 的 client
    authed_client = ApiClient(base_url=base_url, token=token)
    
    # 将新创建的 client 存入缓存
    clients_cache[role] = authed_client
    
    return authed_client