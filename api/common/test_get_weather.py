import pytest
import allure
from lib.utils.logger import get_logger

logger = get_logger()

@pytest.mark.parametrize("client", ["admin", "corp", "user"], indirect=True)
def test_get_weather(client, request):
    resp = client.get("/admin-api/job/weather/get")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    # 根据参数值断言
    if result["code"] == 0:
        assert result["code"] == 0
    else:
        assert result["code"] == 400