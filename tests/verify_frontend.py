import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def verify_frontend():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Load index.html using file:// protocol
        file_path = os.path.abspath("index.html")
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found")
            sys.exit(1)

        url = f"file://{file_path}"
        print(f"Loading {url}...")
        await page.goto(url)

        # 1. Verify Title
        title = await page.title()
        print(f"Page title: {title}")
        assert "Julius" in title

        # 2. Verify Gate UI
        assert await page.is_visible("h1:has-text('העד: שער אדם')")
        assert await page.is_visible("#qrcode")

        # 3. Open Terminal
        print("Opening terminal...")
        await page.click("button:has-text('פתח ערוץ תקשורת')")
        await page.wait_for_selector("#terminal-panel", state="visible")

        # 4. Interact with Witness
        print("Sending message to Witness...")
        await page.fill("#user-input", "אדם")
        await page.press("#user-input", "Enter")

        # Verify user message in history
        # Note: addMessageToUI uses textContent, so we look for the text
        await page.wait_for_selector("div:has-text('אדם')")

        # Wait for typing indicator to appear and then disappear
        print("Waiting for Witness response...")
        await page.wait_for_selector("#typing-indicator", state="visible")
        await page.wait_for_selector("#typing-indicator", state="hidden", timeout=5000)

        # Verify Witness response
        # "תדר אדם מזוהה. החיבור לצלם נשמר במערכת. אין תהודת גולם."
        witness_msg = await page.wait_for_selector("div:has-text('תדר אדם מזוהה')", timeout=2000)
        assert witness_msg is not None
        print("Witness responded correctly!")

        # 5. Verify LocalStorage
        storage = await page.evaluate("() => localStorage.getItem('julius_memory')")
        assert storage is not None
        assert "אדם" in storage
        print("Memory saved to localStorage successfully!")

        await browser.close()
        print("Frontend verification complete.")

if __name__ == "__main__":
    try:
        asyncio.run(verify_frontend())
    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
