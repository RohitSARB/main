import asyncio
from playwright.async_api import async_playwright
from pymongo import MongoClient
from datetime import datetime

# ---------------- MongoDB ----------------
client = MongoClient("mongodb://localhost:27017")
db = client["playwright_db"]
collection = db["scraped_data"]
collection.create_index("uid", unique=True)

# ---------------- Worker ----------------
async def run_flow(user_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await page.goto(
                "http://127.0.0.1:5500/playwright/parallelism.html",
                wait_until="load",
                timeout=60000
            )

            await page.locator("#username").wait_for()

            await page.fill("#username", user_id)
            await page.fill("#password", "pass")
            await page.click("#submit-btn")
            await page.locator("#form-result").wait_for()

            # -------- Articles --------
            articles = []
            cards = await page.locator("#articles .card").all()
            for card in cards:
                articles.append({
                    "title": await card.locator("h3").text_content(),
                    "description": await card.locator("p").text_content()
                })

            # -------- New Tab --------
            async with context.expect_page() as p_new:
                await page.click("#new-tab")

            detail = await p_new.value
            await detail.wait_for_load_state("load")
            detail_texts = await detail.locator("p").all_text_contents()
            await detail.close()

            # -------- Infinite Scroll --------
            container = page.locator("#infinite")
            for _ in range(3):
                await container.evaluate("el => el.scrollTop = el.scrollHeight")
                await asyncio.sleep(0.4)

            products = await container.locator(".card").all_text_contents()

            # -------- Iframe --------
            frame = page.frame_locator("iframe")
            frame_text = await frame.locator("#frame-text").text_content()

            document = {
                "uid": user_id,
                "timestamp": datetime.utcnow(),
                "articles": articles,
                "details_tab": detail_texts,
                "products": products,
                "iframe_text": frame_text
            }

            try:
                collection.insert_one(document)
                print(f"[{user_id}] Stored successfully")
            except:
                print(f"[{user_id}] Duplicate skipped")

        except Exception as e:
            print(f"[{user_id}] ERROR → {e}")

        finally:
            await context.close()
            await browser.close()

# ---------------- Runner ----------------
async def main():
    users = ["user_1", "user_2", "user_3"]

    await asyncio.gather(
        *(run_flow(user) for user in users)
    )

asyncio.run(main())
