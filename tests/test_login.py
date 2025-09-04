from pages.login_page import LoginPage

def test_login_success(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("admin", "123456")
    assert page.url == "https://example.com/dashboard"
