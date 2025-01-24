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


@pytest.mark.parametrize(
    "email, password",
    [
        ("sa1@gmail.com", "111"),
        ("sa1@gmail.co", "Ed91460b"),
        ("sa1@gmail.co", "111")
    ]
)
def test_invalid_email(setup_browser: Page, email, password):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", email)
    page.fill("[name='password']", password)

    page.get_by_role("button", name="Log In").click()

    assert page.wait_for_selector(".f6d8d3ec"), "Error toaster is not displayed"


@pytest.mark.parametrize(
    "email, password, error_text",
    [
        ("sa1@gmail.com", "", "Please specify Password"),
        ("", "Ed91460b", "Please specify Email"),
        ("", "", "Please specify Email")
    ]
)
def test_required_fields_validation(setup_browser: Page, email, password, error_text):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", email)
    page.fill("[name='password']", password)

    page.get_by_role("button", name="Log In").click()

    assert page.text_content(".e859cbeb") == error_text, "Error message is not displayed"


def test_email_format_validation(setup_browser: Page):
    page = setup_browser
    page.goto("https://staging-app.pharosiq.com/signin")

    page.fill("[name='email']", "sa1gmail.com")
    page.fill("[name='password']", "Ed91460b")

    page.get_by_role("button", name="Log In").click()

    assert page.text_content(".e859cbeb") == "Please enter the email address in the format *@*.*", \
        "Error message is not displayed"


