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


def test_admin_login(setup_browser: Page):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", "a1@gmail.com")
    page.fill("[name='password']", "mF5950J8")

    page.get_by_role("button", name="Log In").click()

    assert page.wait_for_selector("._d0dff29"), "Dashboard is not loaded"

    assert page.is_visible("._409794c"), "Not an admin"


def test_guest_user(setup_browser: Page):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", "y.aliakseyenka+guest@paralect.com")
    page.fill("[name='password']", "136495aleX")

    page.get_by_role("button", name="Log In").click()

    assert page.wait_for_selector("._d0dff29"), "Dashboard is not loaded"

    assert page.is_visible("._f2b5494"), "Not a guest user"


def test_company_user(setup_browser: Page):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", "cu1@gmail.com")
    page.fill("[name='password']", "0B53iApk")

    page.get_by_role("button", name="Log In").click()

    assert page.wait_for_selector("._d0dff29"), "Dashboard is not loaded"

    assert page.locator("._a59591b").count() == 3, "Not a company user"




