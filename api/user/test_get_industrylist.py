import pytest
import allure

@pytest.mark.parametrize("client", ["user"], indirect=True)
def test_get_industrylist(client, request):
    resp = client.get("/admin-api/system/industry/getIndustryList")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0