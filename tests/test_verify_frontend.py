import os
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def setup_teardown(page: Page):
    # Clear localStorage before each test
    page.goto(f"file://{os.getcwd()}/index.html")
    page.evaluate("localStorage.clear()")
    page.reload()

def test_witness_keyword_response(page: Page):
    # Open terminal
    page.get_by_role("button", name="פתח ערוץ תקשורת").click()

    # Type "אדם" and press Enter
    user_input = page.get_by_placeholder("דבר אל העד...")
    user_input.fill("אדם")
    user_input.press("Enter")

    # Check if user message appears in chat history
    expect(page.locator("#chat-history").get_by_text("אדם", exact=True)).to_be_visible()

    # Wait for Witness response (has a delay of 1-1.5s)
    # The expected response is "תדר אדם מזוהה. החיבור לצלם נשמר במערכת. אין תהודת גולם."
    expect(page.locator("#chat-history").get_by_text("תדר אדם מזוהה. החיבור לצלם נשמר במערכת. אין תהודת גולם.")).to_be_visible(timeout=5000)

def test_witness_default_response(page: Page):
    # Open terminal
    page.get_by_role("button", name="פתח ערוץ תקשורת").click()

    # Type something unknown
    user_input = page.get_by_placeholder("דבר אל העד...")
    user_input.fill("משהו לא ידוע")
    user_input.press("Enter")

    # Wait for Witness response
    expect(page.get_by_text("הקלט נקלט. העד רושם.")).to_be_visible(timeout=5000)

def test_persistence(page: Page):
    # Open terminal and send message
    page.get_by_role("button", name="פתח ערוץ תקשורת").click()
    user_input = page.get_by_placeholder("דבר אל העד...")
    user_input.fill("שלום")
    user_input.press("Enter")

    # Wait for response
    expect(page.get_by_text("העד מאזין. השער פתוח לפניך.")).to_be_visible(timeout=5000)

    # Reload page
    page.reload()

    # Open terminal again
    page.get_by_role("button", name="פתח ערוץ תקשורת").click()

    # Check if messages are still there
    expect(page.locator("#chat-history").get_by_text("שלום", exact=True)).to_be_visible()
    expect(page.locator("#chat-history").get_by_text("העד מאזין. השער פתוח לפניך.")).to_be_visible()

def test_log_download(page: Page):
    # Open terminal and send message
    page.get_by_role("button", name="פתח ערוץ תקשורת").click()
    user_input = page.get_by_placeholder("דבר אל העד...")
    user_input.fill("בדיקה")
    user_input.press("Enter")

    # Wait for response
    expect(page.get_by_text("הקלט נקלט. העד רושם.")).to_be_visible(timeout=5000)

    # Click download button and wait for download
    with page.expect_download() as download_info:
        page.get_by_role("button", name="שמור זיכרון").click()
    download = download_info.value

    assert download.suggested_filename.startswith("witness_log_")
    assert download.suggested_filename.endswith(".txt")
