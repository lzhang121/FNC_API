import pytest
import allure

@allure.parent_suite("企业端") 
@allure.suite("主业页右上角") 
@allure.feature("主业页右上角")
@pytest.mark.parametrize("client", ["corp"], indirect=True)
def test_get_homepagetopright(client, request):
    resp = client.get("/admin-api/job/enterprise-home/homePageTopRight")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0

