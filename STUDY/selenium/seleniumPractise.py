from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
import pandas as pd


# chrome_options = Options()
# chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-popup-blocking")
# driver = webdriver.Chrome(options=chrome_options)

# driver = webdriver.Chrome()

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install())
)

# time.sleep(5)
wait = WebDriverWait(driver,3)

# driver.get("file:///c:/Users/RohitS.ARB/WORK/seleniumPractise.py")
driver.get("http://127.0.0.1:5500/selenium_practice_site.html")
driver.maximize_window()

wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("user")
wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("1234567890")
wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

status = wait.until(EC.visibility_of_element_located((By.ID, "loginStatus")))
print(status.text)

# dropdown = Select(driver.find_element(By.ID, "category"))
dropdown = wait.until(EC.presence_of_element_located((By.ID, "category")))
# dropdown = wait.until(EC.element_to_be_clickable((By.ID, "category")))
select = Select(dropdown)
select.select_by_visible_text("Clothing")
# select.select_by_value("Clothing")
# select.select_by_index(1)

products = driver.find_elements(By.CLASS_NAME, "product")
title=[]
price=[]
link=[]
for product in products:
    title.append(product.find_element(By.CLASS_NAME, "title").text)
    price.append(product.find_element(By.CLASS_NAME, "price").text)
    link.append(product.find_element(By.TAG_NAME, "a").get_attribute("href"))

df = pd.DataFrame({
    "title" : title,
    "price" : price,
    "link" : link
})
print(df)



# Method	                        Description
# move_to_element(element)	        Moves the mouse to the middle of the element.
# click(element)	                Clicks on the element.
# double_click(element)	            Double-clicks on the element.
# context_click(element)	        Right-clicks on the element.
# drag_and_drop(source, target)	    Drags an element to another element.
# send_keys(keys)	                Sends keyboard keys to the active element.
# perform()	                        Executes all queued actions in sequence.

# click(on_element): Performs a left-click on the specified element.
# actions.click(element).perform()

# double_click(on_element): Executes a double-click on an element.
# actions.double_click(element).perform()

# context_click(on_element): Performs a right-click on the target element.
# actions.context_click(element).perform()

# drag_and_drop(source, target): Drags an element and drops it on another.
# actions.drag_and_drop(source_element, target_element).perform()

# move_to_element(on_element): Moves the mouse pointer to the middle of the specified element.
# actions.move_to_element(element).perform()

# send_keys(keys_to_send): Sends keyboard input to the active element.
# actions.send_keys("Hello").perform()

link_element = driver.find_element(By.TAG_NAME, "a")
ActionChains(driver)\
.key_down(Keys.CONTROL)\
.click(link_element)\
.key_up(Keys.CONTROL)\
.perform()




# Dealing with multiple tabs
link_elements = driver.find_elements(By.TAG_NAME, "a")
for element in link_elements:
    ActionChains(driver)\
    .key_down(Keys.CONTROL)\
    .click(element)\
    .key_up(Keys.CONTROL)\
    .perform()
# 2-nd way
# for element in link_elements:
#     driver.execute_script(
#         "window.open(arguments[0].href, '_blank');", element
#     )
main_tab = driver.current_window_handle
for tab in driver.window_handles:
    if tab != main_tab:
        driver.switch_to.window(tab)
        print("New tab title: ", driver.title)
        time.sleep(3)
        driver.close()
driver.switch_to.window(main_tab)



# handling alerts
driver.find_element(By.XPATH, "/html/body/button[2]").click()
alert = wait.until(EC.alert_is_present())
print(alert.text)


# handling iframes
driver.switch_to.frame(0)
frame_content = driver.find_element(By.ID, "frameText").text
print("Content inside frame: ", frame_content)
driver.switch_to.default_content()


# scroll using javascript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# smooth scrolling
        # driver.execute_script(
        #     "window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
# scroll to specific element
        # element = driver.find_element(By.ID, "product")
        # driver.execute_script("window.scrollIntoView(true);", element)
# scroll by fixed amount
        # driver.execute_script("window.scrollBy(0, 100);")
# Scrolling Horizontally
        # In some cases, you might need to scroll horizontally, for example, to interact with elements in a wide table. Use the following script to scroll horizontally:
        # driver.execute_script("window.scrollBy(1000, 0);")





# now additional selenium functionalities apart from which we have used in the project


# Identifying Honeypots
# Honeypots are elements deliberately hidden from regular users but visible to bots. They are designed to detect and block automated activities like web scraping. Selenium allows you to detect and avoid interacting with these elements effectively.
# You can use CSS selectors to identify elements hidden from view using styles like display: none; or visibility: hidden;. Selenium’s find_elements method with By.CSS_SELECTOR is handy for this purpose:
        # elements = driver.find_elements(By.CSS_SELECTOR, '[style*="display:none"], [style*="visibility:hidden"]')
        # for element in elements:
        #     if not element.is_displayed():
        #         continue  # Skip interacting with honeypot elements
# A common form of honeypot is a disguised button element. These buttons are visually hidden from users but exist within the HTML structure of the page:
#         <button id="fakeButton" style="display: none;">Click Me</button>
# In this scenario, the button is intentionally hidden. An automated bot programmed to click all buttons on a page might interact with this hidden button, triggering security measures on the website. Legitimate users, however, would never encounter or engage with such hidden elements.



# Dynamic tables often use pagination to show only a subset of rows at a time. We click the “Next” button to scrape all rows until we reach the last page.
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        
        # while True:
        #     # Extract rows from the current page
        #     rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        #     for row in rows:
        #         cells = row.find_elements(By.TAG_NAME, "td")
        #         if cells:
        #             table_data.append([cell.text for cell in cells])
        
        #     # Check if the "Next" button is disabled
        #     try:
        #         next_button = driver.find_element(By.CSS_SELECTOR, ".dt-paging-button.next")
        #         if "disabled" in next_button.get_attribute("class"):
        #             print("Reached the last page.")
        #             break
        
        #         # Click the "Next" button
        #         next_button.click()
        
        #         # Wait for the new page to load
        #         WebDriverWait(driver, 10).until(
        #             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
        #         )
        #     except Exception as e:
        #         print(f"Error while navigating: {e}")
        #         break
        
        # print(f"Total rows scraped: {len(table_data)}")





time.sleep(3)
driver.quit()