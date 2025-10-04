import pytest
import allure
import time
import random
import json

from lib.utils.loader import load_yaml
from lib.utils.http_client import ApiClient

from lib.utils.logger import get_logger
logger = get_logger()


@allure.parent_suite("共通")
@allure.suite("用户体系")
@allure.feature("用户注册")
@pytest.mark.parametrize("case", load_yaml("common/user_register.yaml"))
def test_user_register(config, case):
    """
    测试用户注册功能，支持多种场景。
    """
    allure.dynamic.title(case["casename"])

    # --- 数据准备 ---
    # 获取payload并转换为字符串，便于替换占位符
    payload_str = json.dumps(case["payload"])

    # 动态生成唯一标识，确保每次测试数据的唯一性
    random_str = f"{int(time.time())}{random.randint(100, 999)}"
    random_int = f"{random.randint(10000000, 99999999)}"

    # 替换占位符
    payload_str = payload_str.replace("{{random_str}}", random_str)
    payload_str = payload_str.replace("{{random_int}}", random_int)

    # 将字符串转换回JSON对象
    payload = json.loads(payload_str)

    allure.attach(json.dumps(payload, indent=2, ensure_ascii=False),
                  name="Request Payload",
                  attachment_type=allure.attachment_type.JSON)

    # --- 执行请求 ---
    # 对于注册这类公开接口，我们需要一个不带token的干净ApiClient
    # 我们直接从config中获取base_url来实例化它
    base_url = config['base_url']
    unauthed_client = ApiClient(base_url=base_url)

    if case["condition"] == 1:
        # 条件为1时，先注册一个用户，再用相同的loginName注册，测试重复注册场景
        logger.debug("入参：",payload)
        pre_payload = {
            "mail": payload["loginName"],
            "scene":11
        }
        pre_resp = unauthed_client.post("/admin-api/infra/verificationcode/send-mail", json=pre_payload)
        logger.debug(pre_payload)
        assert pre_resp.status_code == 200
    else:
        # 条件为0时，直接发送验证码
        pass

    resp = unauthed_client.post("/admin-api/job/individual-user/individual-user-register", json=payload)

    allure.attach(resp.text,
                  name="Response",
                  attachment_type=allure.attachment_type.JSON)

    # --- 结果断言 ---
    assert resp.status_code == 200
    result = resp.json()
    validate = case["validate"]

    assert result["code"] == validate["code"]
    if "message" in validate:
        assert validate["message"] in result["message"]
