import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://webscraper.io/test-sites/e-commerce/allinone"

web_response = requests.get(url)
print(web_response)

soup = BeautifulSoup(web_response.content, "html.parser")
name = []
description = []
price = []

product_divs = soup.find_all("div", class_="product-wrapper card-body")
# print(product_divs)

for product in product_divs:
    name_tag = product.find("a", class_="title").text.strip()
    name.append(name_tag)

    desc_tag = product.find("p", class_="description card-text").text.strip()
    description.append(desc_tag)

    price_tag = product.find("span", itemprop="price").text.strip()
    price.append(price_tag)

df = pd.DataFrame({
    "Name": name,
    "Description": description,
    "Price": price
})

print(df)

df.to_excel("SAMPLE.xlsx", index=False)