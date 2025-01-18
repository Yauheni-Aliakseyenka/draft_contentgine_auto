from playwright.sync_api import Page, expect


def test_super_admin_login(page):
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("name='email'", "sa1@gmail.com")
    page.fill("name='password'", "Ed91460b")

    page.get_by_role("button", name="Log In").click()



