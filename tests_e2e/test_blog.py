from playwright.sync_api import Page, expect
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


def test_home_page_loads_and_has_title(page: Page):
    expect(page).to_have_title("Django Girls blog")
    expect(page.get_by_role("heading", name="Django Girls Blog")).to_be_visible()
    expect(page.locator("text=Log in")).to_be_visible()


def test_successful_admin_login(login_as_admin: Page):
    page = login_as_admin

    page.goto(f"{BASE_URL}/admin/")
    expect(page.get_by_role("heading", name="Site administration")).to_be_visible()


def test_create_post_via_regular_form_and_see_on_homepage(login_as_admin: Page):
    page = login_as_admin

    page.goto(f"{BASE_URL}/post/new")

    post_title = f"Пост для E2E-теста — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    post_text = "Этот пост был создан через форму на сайте"
    page.fill('input[name="title"]', post_title)
    page.fill('textarea[name="text"]', post_text)

    page.get_by_role("button", name="Save").click()

    expect(page).to_have_url(page.url)
    expect(page.get_by_role("heading", name=post_title)).to_be_visible()

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    expect(page.get_by_role("heading", name=post_title)).to_be_visible()
    expect(page.get_by_text(post_text)).to_be_visible()


def test_create_post_and_open_its_detail_page(login_as_admin: Page):
    page = login_as_admin

    page.goto(f"{BASE_URL}/post/new")

    post_title = f"Пост для E2E-теста — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    post_text = "Этот пост был создан через форму на сайте"
    page.fill('input[name="title"]', post_title)
    page.fill('textarea[name="text"]', post_text)
    page.get_by_role("button", name="Save").click()

    expect(page).to_have_url(page.url)
    expect(page.get_by_role("heading", name=post_title)).to_be_visible()

    page.goto(BASE_URL)

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(500)

    page.get_by_role("heading", name=post_title).click()

    expect(page).to_have_url(page.url)
    expect(page.get_by_role("heading", name=post_title)).to_be_visible()
    expect(page.get_by_text(post_text)).to_be_visible()
