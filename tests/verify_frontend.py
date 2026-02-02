import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async_work_dir = os.getcwd()
    index_path = f"file://{async_work_dir}/index.html"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. Load the page
        print(f"Loading {index_path}...")
        await page.goto(index_path)

        # 2. Check title
        title = await page.title()
        print(f"Page title: {title}")
        assert "Julius Archive Gate" in title

        # 3. Check for the Gate content
        gate_header = await page.text_content("h1")
        print(f"Gate header: {gate_header}")
        assert "שער יוליוס: העד" in gate_header

        # 4. Open terminal
        print("Opening terminal...")
        await page.click("button:has-text('פתח מסוף תיעוד')")

        # 5. Check if terminal is visible
        is_visible = await page.is_visible("#terminal-panel")
        print(f"Terminal visible: {is_visible}")
        assert is_visible

        # 6. Send a message
        print("Sending message 'אדם'...")
        await page.fill("#user-input", "אדם")
        await page.press("#user-input", "Enter")

        # 7. Wait for response (simulated delay is 1-1.5s)
        print("Waiting for Witness response...")
        await asyncio.sleep(3) # Wait enough for the typing indicator to finish

        # 8. Verify response
        # The witness response for 'אדם' contains "תדר אדם מזוהה"
        chat_content = await page.text_content("#chat-history")
        print(f"Chat history excerpt: {chat_content[:200]}...")
        assert "תדר אדם מזוהה" in chat_content

        # 8.5 Verify "חיבור" keyword
        print("Sending message 'חיבור'...")
        await page.fill("#user-input", "חיבור")
        await page.press("#user-input", "Enter")
        await asyncio.sleep(3)
        chat_content = await page.text_content("#chat-history")
        assert "החיבור למרחב ה-Alignment הושלם" in chat_content

        # 9. Take a screenshot
        screenshot_path = "frontend_verification.png"
        await page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
