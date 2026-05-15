from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time

driver = webdriver.Chrome()
# driver.get("file:///" + os.path.abspath("demo.html"))
driver.get("http://127.0.0.1:5500/demo.html")

time.sleep(1)

def move_to_element(element):
    rect = element.rect
    x = rect['x'] + rect['width']/2
    y = rect['y'] + rect['height']/2

    driver.execute_async_script("""
        const x = arguments[0];
        const y = arguments[1];
        const done = arguments[2];
        moveCursorSmooth(x, y).then(done);
    """, x, y)


search = driver.find_element(By.ID, "searchBox")
move_to_element(search)
search.send_keys("Smooth SVG Cursor")

checkbox = driver.find_element(By.ID, "agreeBox")
move_to_element(checkbox)
checkbox.click()

textarea = driver.find_element(By.ID, "comments")
move_to_element(textarea)
textarea.send_keys("Now it is clean and stable.")

submit = driver.find_element(By.ID, "submitBtn")
move_to_element(submit)
submit.click()

time.sleep(5)
driver.quit()
