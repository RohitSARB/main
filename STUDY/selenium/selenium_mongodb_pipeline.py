"""
End-to-end Selenium → MongoDB pipeline
Author: Rohit
"""

# =========================
# Imports
# =========================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import pandas as pd
import time
from datetime import datetime, UTC
from pymongo import MongoClient, errors, UpdateOne # type: ignore
import logging


# =========================
# Logging Setup
# =========================
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# =========================
# MongoDB Configuration
# =========================
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "userData"
COLLECTION_NAME = "products"


def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    indexes = collection.index_information()

    if "name_1" not in indexes:
        collection.create_index(
            [("name", 1)],
            unique=True,
            partialFilterExpression={"name": {"$type": "string"}}
        )

    return collection


# =========================
# Selenium Scraper
# =========================
def scrape_laptops():
    logger.info("Starting Selenium scraper")

    driver = webdriver.Chrome()
    url = "https://webscraper.io/test-sites/e-commerce/scroll/computers/laptops"

    try:
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)

        # infinite scrolling
        last_height = driver.execute_script("return document.body.scrollHeight")
        print(last_height)

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behvior: 'smooth'});")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            # print(new_height)

        products = driver.find_elements(By.CSS_SELECTOR, "div.product-wrapper.card-body")

        rows = []
        for product in products:
            name = product.find_element(By.CSS_SELECTOR, "a.title").text.strip()
            desc = product.find_element(By.CSS_SELECTOR, "p.description").text.strip()

            rows.append({
                "name": name,
                "description": desc
            })

        df = pd.DataFrame(rows)
        
        logger.info(f"Scraped {len(df)} products")
        return df

    except WebDriverException:
        logger.exception("Selenium error occurred")
        raise

    finally:
        driver.quit()
        logger.info("Browser closed")


# =========================
# MongoDB Ingestion
# =========================
def ingest_to_mongodb(df: pd.DataFrame):
    logger.info("Starting MongoDB ingestion")

    collection = get_mongo_collection()
    now = datetime.now(UTC)

    operations = []

    for record in df.to_dict(orient="records"):
        operations.append(
            UpdateOne(
                {"name": record["name"]},
                {
                    "$set": {
                        "description": record["description"],
                        "scraped_at": now
                    },
                    "$setOnInsert": {
                        "created_at": now
                    },
                    "$inc": {
                        "version": 1
                    }
                },
                upsert=True
            )
        )

    result = collection.bulk_write(operations, ordered=False)

    print(
        f"Inserted: {result.upserted_count}, "
        f"Updated: {result.modified_count}"
    )


# =========================
# Main
# =========================
if __name__ == "__main__":
    logger.info("Pipeline started")

    try:
        df = scrape_laptops()
        ingest_to_mongodb(df)
        logger.info("Pipeline completed successfully")

    except Exception:
        logger.exception("Pipeline failed")
        print("Pipeline failed. Check scraper.log for details.")
