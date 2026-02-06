import pytest
import os
from playwright.sync_api import Page, expect

def test_page_loads(page: Page):
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")

    # Check title
    expect(page).to_have_title("Julius: The Witness Gate")

    # Check headers
    expect(page.locator("h1")).to_have_text("העד: שער אדם")

def test_chat_interaction_and_witness_response(page: Page):
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")

    # Open terminal
    page.click("button:has-text('פתח ערוץ תקשורת')")

    # Check terminal is visible
    expect(page.locator("#terminal-panel")).to_be_visible()

    # Send message "שלום"
    input_field = page.locator("#user-input")
    input_field.fill("שלום")
    input_field.press("Enter")

    # Verify user message appears
    expect(page.locator("#chat-history")).to_contain_text("אורח")
    expect(page.locator("#chat-history")).to_contain_text("שלום")

    # Verify typing indicator appears
    expect(page.locator("#typing-indicator")).to_be_visible()

    # Wait for response (simulated delay is 1-1.5s)
    page.wait_for_selector("#typing-indicator", state="hidden", timeout=5000)

    # Verify Witness response
    expect(page.locator("#chat-history")).to_contain_text("👁️ העד")
    expect(page.locator("#chat-history")).to_contain_text("העד מאזין. השער פתוח לפניך.")

def test_witness_keyword_adam(page: Page):
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")
    page.evaluate("localStorage.clear()")
    page.reload()

    page.click("button:has-text('פתח ערוץ תקשורת')")

    input_field = page.locator("#user-input")
    input_field.fill("מה זה אדם?")
    input_field.press("Enter")

    # Wait for typing indicator to disappear
    page.wait_for_selector("#typing-indicator", state="hidden", timeout=5000)

    # Verify specific response
    expect(page.locator("#chat-history")).to_contain_text("תדר אדם מזוהה. החיבור לצלם נשמר במערכת. אין תהודת גולם.")

def test_persistence(page: Page):
    path = os.path.abspath("index.html")
    page.goto(f"file://{path}")
    page.evaluate("localStorage.clear()")
    page.reload()

    page.click("button:has-text('פתח ערוץ תקשורת')")

    input_field = page.locator("#user-input")
    input_field.fill("בדיקת זיכרון")
    input_field.press("Enter")

    # Wait for response
    page.wait_for_selector("#typing-indicator", state="hidden", timeout=5000)

    # Reload page
    page.reload()

    # Open terminal again
    page.click("button:has-text('פתח ערוץ תקשורת')")

    # Verify message still there
    expect(page.locator("#chat-history")).to_contain_text("בדיקת זיכרון")
