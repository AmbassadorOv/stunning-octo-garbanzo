import os
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.skipif(os.environ.get("CI") == "true", reason="Skipping UI tests in CI")
def test_witness_gate_ui(page: Page):
    # Navigate to index.html using the file:// protocol
    current_dir = os.getcwd()
    file_path = f"file://{current_dir}/index.html"
    page.goto(file_path)

    # 1. Verify Title
    expect(page).to_have_title("Julius: The Witness Gate")

    # 2. Verify Heading
    heading = page.get_by_role("heading", name="העד: שער אדם")
    expect(heading).to_be_visible()

    # 3. Open Terminal
    open_button = page.get_by_role("button", name="פתח ערוץ תקשורת")
    open_button.click()

    # 4. Verify Terminal Panel is visible
    terminal_panel = page.locator("#terminal-panel")
    expect(terminal_panel).to_be_visible()

    # 5. Send a message to the Witness
    user_input = page.locator("#user-input")
    user_input.fill("אדם")
    user_input.press("Enter")

    # 6. Verify Witness Response
    # The response is "תדר אדם מזוהה. החיבור לצלם נשמר במערכת. אין תהודת גולם."
    # There's a simulated delay, so we use expect with auto-waiting
    witness_msg = page.get_by_text("תדר אדם מזוהה. החיבור לצלם נשמר במערכת. אין תהודת גולם.")
    expect(witness_msg).to_be_visible(timeout=5000)

if __name__ == "__main__":
    # This block allows running the test script directly if needed
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()
        try:
            current_dir = os.getcwd()
            file_path = f"file://{current_dir}/index.html"
            page.goto(file_path)

            # Open terminal
            page.get_by_role("button", name="פתח ערוץ תקשורת").click()

            # Send message
            page.locator("#user-input").fill("אדם")
            page.locator("#user-input").press("Enter")

            # Wait for response
            page.wait_for_selector("text=תדר אדם מזוהה", timeout=5000)

            # Take screenshot
            os.makedirs("verification", exist_ok=True)
            page.screenshot(path="verification/witness_response.png")
            print("Screenshot saved to verification/witness_response.png")

        finally:
            browser.close()
