import pytest
import allure


@allure.parent_suite("管理端") 
@allure.suite("通知列表") 
@allure.feature("通知列表")
@pytest.mark.parametrize("client", ["admin","corp"], indirect=True)
def test_get_gethomenoticelist(client, request):
    resp = client.get("/admin-api/system/notice/getHomeNoticeList")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0

