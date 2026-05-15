from playwright.sync_api import sync_playwright, expect
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://127.0.0.1:5500/playwright/index.html")

    page.locator("#username").fill('Sample')

    page.locator("body")\
    .locator("#password")\
    .fill("pass")

    page.locator("body", has=page.locator("#submit-btn"))\
    .locator("#submit-btn").click()

    expect(page.locator("#form-result")).to_be_visible()

    page.hover("#menu")

    new_tab = page.locator("#new-tab")
    with context.expect_page() as p:
        new_tab.click()
    
    detail = p.value
    detail.wait_for_load_state()

    for i in range(detail.locator('p').count()):
        print(detail.locator('p').nth(i).text_content())

    detail.close()

    cards_container = page.locator("#infinite")
    print(cards_container.count())
    for i in range(3):
        cards_container.evaluate("el => el.scrollTop = el.scrollHeight")
        time.sleep(0.3)
    
    for i in range(cards_container.locator('.card').count()):
        print("card-",i+1," value: ", cards_container.locator('.card').nth(i).text_content())
    expect(cards_container.locator('.card', has_text="Item 5")).to_be_visible()

    
    frame = page.frame_locator("iframe")
    frame.locator("#frame-btn").click()

    page.locator("#username").click() # click to focus
    # page.mouse.wheel(0,1000)
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.type("New Data",delay=100)

    total_items = page.evaluate("() => document.querySelectorAll('.card').length")
    print("Items count using JS execution in selenium: ",total_items)
     
    browser.close()