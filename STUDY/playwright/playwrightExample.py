# playwright_scraper.py
from playwright.sync_api import sync_playwright
import pandas as pd

names = []
descriptions = []
prices = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # headless mode
    page = browser.new_page()
    page.goto("https://webscraper.io/test-sites/e-commerce/allinone")
    
    # Auto-waits, no need for sleep
    products = page.locator("div.product-wrapper.card-body")
    for i in range(products.count()):
        product = products.nth(i)
        
        # Name
        names.append(product.locator("a.title").inner_text().strip())
        
        # Description
        descriptions.append(product.locator("p.description").inner_text().strip())
        
        # Price
        prices.append(product.locator("span[itemprop='price']").inner_text().strip())
    
    browser.close()

# Create DataFrame
df = pd.DataFrame({
    "Name": names,
    "Description": descriptions,
    "Price": prices
})

print(df)
