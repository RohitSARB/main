# selenium_scraper_human.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import random
import pyautogui # type: ignore
from pymongo import MongoClient # type: ignore
from pymongo.errors import BulkWriteError, DuplicateKeyError # type: ignore
from datetime import datetime

# ------------------ HUMAN UTILITIES ------------------

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

def human_pause(a=0.2, b=0.6):
    time.sleep(random.uniform(a, b))

def human_scroll(scrolls=3):
    for _ in range(scrolls):
        pyautogui.scroll(-random.randint(200, 400))
        human_pause(0.2, 0.4)

def human_mouse_to_element(driver, element):
    """
    Moves mouse smoothly to the center of a Selenium element
    """
    location = element.location_once_scrolled_into_view
    size = element.size

    x = location['x'] + size['width'] / 2
    y = location['y'] + size['height'] / 2

    screen_x, screen_y = driver.execute_script("""
        const rect = arguments[0].getBoundingClientRect();
        return [rect.left + rect.width/2, rect.top + rect.height/2];
    """, element)

    win_x = driver.get_window_position()['x']
    win_y = driver.get_window_position()['y']

    target_x = win_x + screen_x
    target_y = win_y + screen_y + 80  # browser top bar offset

    pyautogui.moveTo(
        target_x + random.randint(-5, 5),
        target_y + random.randint(-5, 5),
        duration=random.uniform(0.4, 0.8),
        tween=pyautogui.easeInOutQuad
    )

# ------------------ SELENIUM ------------------

driver = webdriver.Chrome()
driver.get("https://webscraper.io/test-sites/e-commerce/scroll/computers/laptops")
driver.maximize_window()
time.sleep(3)

names = []
descriptions = []

products = driver.find_elements(By.CSS_SELECTOR, "div.product-wrapper.card-body")

for product in products:
    # Move mouse to product
    human_mouse_to_element(driver, product)
    human_pause()

    name_tag = product.find_element(By.CSS_SELECTOR, "a.title")
    desc_tag = product.find_element(By.CSS_SELECTOR, "p.description")

    # Hover effect (human-like)
    ActionChains(driver).move_to_element(name_tag).perform()
    human_pause()

    names.append(name_tag.text.strip())
    descriptions.append(desc_tag.text.strip())

# Human scroll more content
human_scroll(4)
time.sleep(1)

driver.quit()

# ------------------ DATAFRAME ------------------

df = pd.DataFrame({
    "Name": names,
    "Description": descriptions,
})

print(df)

# ------------------ MONGODB ------------------

client = MongoClient("mongodb://localhost:27017/")
db = client["userData"]
collection = db["products"]

# Unique index
try:
    collection.create_index("Name", unique=True)
except DuplicateKeyError:
    pass

records = df.to_dict(orient="records")

# Add metadata
for record in records:
    record["scraped_at"] = datetime.utcnow()
    record["version"] = 1

try:
    collection.insert_many(records, ordered=False)
    print("Inserted records")
except BulkWriteError:
    print("Duplicate records skipped")

# Verify
print("Sample record:")
print(collection.find_one())
