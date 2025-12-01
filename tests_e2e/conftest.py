import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"
ADMIN_CREDENTIALS = {"username": "admin", "password": "pass"}


@pytest.fixture(scope="function", autouse=True)
def goto_home(page: Page):
    page.goto(BASE_URL)
    yield


@pytest.fixture(autouse=True, scope="function")
def clean_context(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def login_as_admin(page: Page):
    page.goto(f"{BASE_URL}/admin/login/?next=/")
    page.fill('input[name="username"]', ADMIN_CREDENTIALS["username"])
    page.fill('input[name="password"]', ADMIN_CREDENTIALS["password"])
    page.click('input[type="submit"]')

    yield page
