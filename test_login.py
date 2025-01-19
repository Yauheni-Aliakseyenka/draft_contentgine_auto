import pytest
from playwright.sync_api import Page, Playwright


@pytest.fixture
def setup_browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


def test_super_admin_login(setup_browser: Page):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", "sa1@gmail.com")
    page.fill("[name='password']", "Ed91460b")

    page.get_by_role("button", name="Log In").click()

    assert page.wait_for_selector("._d0dff29"), "Dashboard is not loaded"

    assert page.is_visible(".daae4068"), "Not a super admin"

    assert page.is_visible("#recharts_measurement_span"), "Message about wrong email or password"







