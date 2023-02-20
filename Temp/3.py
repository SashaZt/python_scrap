from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.znanylekarz.pl/")
    page.get_by_role("button", name="Zaakceptuj").click()
    page.get_by_placeholder("miasto lub dzielnica").click()
    page.locator("[data-test-id=\"location-dropdown\"]").get_by_role("link", name="Warszawa").click()
    page.get_by_role("button", name="Szukaj").click()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)