import pytest
import allure

# 注意这里的变化：parametrize 的目标是 'client'
@allure.parent_suite("用户端") 
@allure.suite("job申请") 
@allure.feature("job申请")
@pytest.mark.parametrize("client", ["user"], indirect=True)
def test_get_jobapplications(client, request): # 不再需要 auth_token fixture
    # client 已经是带 'user' token 的实例了
    resp = client.get("/admin-api/job/applications?pageNo=1&pageSize=10")
    
    # allure.attach 的 name 可以更简洁
    allure.attach(
        resp.text,
        name=f"{request.node.name}_response",
        attachment_type=allure.attachment_type.JSON
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["code"] == 0