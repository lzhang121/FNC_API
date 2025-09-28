import pytest
import allure

@allure.parent_suite("用户端") 
@allure.suite("数据字典") 
@allure.feature("数据字典")
@pytest.mark.parametrize("client", ["user"], indirect=True)
def test_get_dictdatabytype(client, request):
    resp = client.get("/admin-api/infra/dict-data/getDictDataByType?dictType=personal_end_job_distance")
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0