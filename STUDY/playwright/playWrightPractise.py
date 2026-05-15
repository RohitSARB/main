from playwright.sync_api import sync_playwright
import time

# import time
# from math import hypot

# def smooth_mouse_move(page, start, end, duration=0.01):
#     """
#     Fast, smooth, human-like mouse movement
#     duration: total time in seconds (0.15–0.25 is natural)
#     """
#     x1, y1 = start
#     x2, y2 = end

#     steps = max(12, int(duration * 120))  # dynamic steps
#     delay = duration / steps

#     for i in range(steps + 1):
#         t = i / steps
#         # ease-in-out curve (human-like)
#         t = t * t * (3 - 2 * t)

#         x = x1 + (x2 - x1) * t
#         y = y1 + (y2 - y1) * t

#         page.mouse.move(x, y)
#         time.sleep(delay)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    # page = browser.new_page()
    # page.goto("https://example.com")
    # print(page.content())
    # print(page.title())

    context = browser.new_context(viewport={"width":1980/2, "height":1080})
    page = context.new_page()
    # page.goto("https://example.com")


    # # ✅ INJECT HERE (before navigation)
    # page.add_init_script("""
    # (() => {
    # const addCursor = () => {
    #     const cursor = document.createElement('div');
    #     cursor.style.width = '12px';
    #     cursor.style.height = '12px';
    #     cursor.style.border = '2px solid red';
    #     cursor.style.borderRadius = '50%';
    #     cursor.style.position = 'fixed';
    #     cursor.style.zIndex = '999999';
    #     cursor.style.pointerEvents = 'none';
    #     cursor.style.background = 'transparent';
    #     document.body.appendChild(cursor);

    #     document.addEventListener('mousemove', e => {
    #     cursor.style.left = e.clientX + 'px';
    #     cursor.style.top = e.clientY + 'px';
    #     });
    # };

    # if (document.readyState === 'loading') {
    #     document.addEventListener('DOMContentLoaded', addCursor);
    # } else {
    #     addCursor();
    # }
    # })();
    # """)

    # or
    # page.evaluate(paste JS code here)



    page.goto("http://127.0.0.1:5500/playwright/index.html")
    print(page.title())
    # page.locator("text=About us").click()
    # about_us = page.locator("text=About us")
    # about_us.wait_for(timeout=10000)

    # page.get_by_placeholder("Username").fill("Rohit")
    # page.fill("#username", "rohit") # 1. locator , 2. value
    page.locator("#username").highlight()
    page.locator("#username").fill("rohit") # locator is mainly used with css selectors
    # page.locator("#password").hover()
    page.locator("#password").focus()
    page.fill("#password", "123")

    page.get_by_text("Submit").click()
    # page.click("text=Submit")



    # page.on("mousemove", lambda m: print(m["x"], m["y"]))

    
    page.mouse.move(400,300)
    page.mouse.move(200,600)

    # smooth_mouse_move(page, (50, 50), (400, 300))
    # smooth_mouse_move(page, (400, 300), (200, 600))


    box = page.locator("#infinite").bounding_box()
    page.mouse.click(
        box['x'] + box["width"] /2,
        box['y'] + box["height"] /2
    )

    # box = page.locator("#infinite").bounding_box()
    # target_x = box["x"] + box["width"] / 2
    # target_y = box["y"] + box["height"] / 2

    # smooth_mouse_move(page, (200, 600), (target_x, target_y))
    # page.mouse.click(target_x, target_y)

    page.mouse.wheel(0,1000)

    
    page.once('dialog', lambda dialog: dialog.accept())
    page.click('#alert-btn')

    page.on('dialog', lambda dialog: dialog.dismiss())
    page.click('#confirm-btn')


    # container = page.locator("#infinite")
    # items = container.locator(".card")

    # # ✅ count initial items
    # prev_count = items.count()
    # print("Initially loaded:", prev_count)

    # while True:
    #     container.evaluate("el => el.scrollTop = el.scrollHeight")

    #     try:
    #         page.wait_for_function(
    #             "(container, prev) => container.querySelectorAll('.card').length > prev",
    #             arg=(container, prev_count),
    #             timeout=3000
    #         )
    #     except:
    #         print("No new items loaded. End reached.")
    #         break

    #     curr_count = items.count()
    #     prev_count = curr_count

    # print("Total items loaded:", prev_count)


    # 2nd way 

    container = page.locator("#infinite")
    for _ in range(5):
        container.evaluate("el => el.scrollTop = el.scrollHeight")
        time.sleep(0.5)

    items = container.locator(".card")
    print("Items loaded:", items.count())


    frame = page.frame_locator("iframe")
    print(frame.locator('#inside-frame').inner_text())

    # page.screenshot(path='page.png', full_page=True)

    # =====================
    # Network Interception
    # =====================
    def log_request(req):
        print("Request:", req.url)

    page.on("request", log_request)
    page.reload()


    context.close()
    browser.close()