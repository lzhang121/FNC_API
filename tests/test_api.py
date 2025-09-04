def test_api_request(page):
    response = page.request.get("https://httpbin.org/get")
    assert response.status == 200
    assert "url" in response.json()
