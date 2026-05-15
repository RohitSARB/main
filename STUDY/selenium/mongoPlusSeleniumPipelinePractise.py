# selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up Chrome driver (make sure chromedriver is in PATH)
driver = webdriver.Chrome()

# url = "https://webscraper.io/test-sites/e-commerce/allinone"
url = "https://webscraper.io/test-sites/e-commerce/scroll/computers/laptops"
driver.get(url)
time.sleep(3)  # simple wait for page to load dynamic content
# driver.maximize_window()

# Lists to store scraped data
names = []
descriptions = []
prices = []

# Find all product cards
products = driver.find_elements(By.CSS_SELECTOR, "div.product-wrapper.card-body")

for product in products:
    # Name
    name_tag = product.find_element(By.CSS_SELECTOR, "a.title")
    names.append(name_tag.text.strip())
    
    # Description
    desc_tag = product.find_element(By.CSS_SELECTOR, "p.description")
    descriptions.append(desc_tag.text.strip())
    
    # #Price
    # price_tag = product.find_element(By.CSS_SELECTOR, "span[itemprop='price']")
    # prices.append(price_tag.text.strip())


# one time scroll
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(2)


# # infinite scrolling
# last_height = driver.execute_script("return document.body.scrollHeight")
# print(last_height)

# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behvior: 'smooth'});")
#     time.sleep(3)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height
#     print(new_height)


# products = driver.find_elements(By.CSS_SELECTOR, "div.product-wrapper.card-body")

# for product in products:
#     # Name
#     name_tag = product.find_element(By.CSS_SELECTOR, "a.title")
#     names.append(name_tag.text.strip())
    
#     # Description
#     desc_tag = product.find_element(By.CSS_SELECTOR, "p.description")
#     descriptions.append(desc_tag.text.strip())


# Close driver
driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Name": names,
    "Description": descriptions,
    # "Price": prices
})
print(df)










'''

PYMONGO SIMULATION

'''



from pymongo import MongoClient # type: ignore
client = MongoClient("mongodb://localhost:27017/")

print(client.list_database_names())

db = client['userData']
collection = db['products']

# collection.create_index("Name", unique=True) # handles duplicate product insertion
# collection.create_index("Description", unique=True)

records = df.to_dict(orient='records')

# | Orient    | Shape               | Best use        |
# | --------- | ------------------- | --------------- |
# | `records` | list of dicts       | MongoDB, APIs   |
# | `dict`    | col → index → value | Pandas internal |
# | `list`    | col → list          | Simple export   |
# | `series`  | col → Series        | Pandas only     |
# | `split`   | index/cols/data     | ML & caching    |
# | `tight`   | full metadata       | Perfect restore |



# PHASE 1 — DUPLICATE PREVENTION (CRITICAL)
# 🧠 Problem
# If you run the scraper twice → same products get inserted again


# collection.insert_many(records)
## rather do this
# from pymongo.error import BulkWriteError
from pymongo.errors import BulkWriteError, DuplicateKeyError # type: ignore
# try:
#     collection.insert_many(records, ordered = False)
# except (BulkWriteError, DuplicateKeyError) as e:
#     print("Duplicate was found and skipped")

try:
    collection.create_index("Name", unique=True)
except DuplicateKeyError:
    print("Index already exists with duplicates")

try:
    collection.insert_many(records, ordered=False)
except BulkWriteError:
    print("Duplicate records skipped during insert")

idx=0
for doc in collection.find():
    print(doc)
    idx = idx+1
    if (idx == 1): 
        break


# PHASE 2 — TIMESTAMPS & VERSIONING (EXPERT LEVEL)
# 🧠 Why this matters

# Know when data was scraped

# Track changes over time

# Enable analytics & audits

# Step 1: Add metadata before insert
# from datetime import datetime

# for record in records:
#     record["scraped_at"] = datetime.utcnow()
#     record["version"] = 1

# Step 2: Version Update Strategy

# If product exists → increment version

# for record in records:
#     collection.update_one(
#         {"name": record["name"]},
#         {
#             "$set": {
#                 "description": record["description"],
#                 "scraped_at": datetime.utcnow()
#             },
#             "$inc": {"version": 1}
#         },
#         upsert=True
#     )
# 📌 upsert=True = insert if not exists, update if exists



# PHASE 3 — SCRAPING PIPELINE (PROFESSIONAL DESIGN)
# ❌ Beginner way

# Everything in one file

# ✅ Expert way

# Separation of concerns

# project/
# │
# ├── scraper/
# │   ├── selenium_scraper.py
# │
# ├── db/
# │   ├── mongo.py
# │
# ├── pipeline/
# │   ├── ingest.py
# │
# ├── utils/
# │   ├── logger.py
# │
# ├── api/
# │   ├── main.py




# PHASE 4 — LOGGING & ERROR HANDLING (MANDATORY)
# 🧠 Rule

# If it’s not logged → it didn’t happen.


# PHASE 5 — MOVE TO MONGODB ATLAS (CLOUD)
# 🧠 Why Atlas
# Cloud hosted
# Scalable
# Free tier
# Production ready


# PHASE 6 — FASTAPI ON TOP OF MONGODB (BACKEND LEVEL)
# Now your scraped data becomes an API.


