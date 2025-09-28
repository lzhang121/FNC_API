import pytest
import allure

@allure.parent_suite("用户端") 
@allure.suite("区域列表") 
@allure.feature("区域列表")
@pytest.mark.parametrize("client", ["user"], indirect=True)
def test_get_areaslist(client, request):
    resp = client.get("/admin-api/system/areaManage/getAreasList")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0