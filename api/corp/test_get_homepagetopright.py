import pytest
import allure

@pytest.mark.parametrize("auth_token", ["corp"], indirect=True)
def test_get_homepagetopright(client, auth_token, request):
    resp = client.get("/admin-api/job/enterprise-home/homePageTopRight")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_{auth_token}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0

