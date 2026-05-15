import random, time, pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.03


def pause():
    time.sleep(random.uniform(0.2,0.6))


def move_mouse(x,y):
    pyautogui.moveTo(
        x + random.randint(-5,5),
        y + random.randint(-5,5),
        duration=random.uniform(0.5,0.9),
        tween=pyautogui.easeInOutQuad
    )

def click():
    pyautogui.mouseDown()
    pause()
    pyautogui.mouseUp()

def type_text(text):
    pyautogui.write(text, interval=random.uniform(0.1,0.3))

def human_scroll(amount=400):
    pyautogui.scroll(-amount)
    pause()


def element_to_screen(driver, element):
    rect = driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return { x: r.left + r.width/2, y: r.top + r.height/2 };
    """, element)

    win = driver.get_window_position()

    chrome_offset = driver.execute_script("""
        return window.outerHeight - window.innerHeight;
    """)

    return (
        win['x'] + rect['x'],
        win['y'] + rect['y'] + chrome_offset
    )

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# from human_actions import *
# from utils import element_to_screen  # if separated

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5500/pyautogui/pyautoGUISample.html")
driver.maximize_window()
time.sleep(2)

# TYPE NAME (HUMAN)
name_input = driver.find_element(By.ID, "name")
x, y = element_to_screen(driver, name_input)
move_mouse(x, y)
click()
pause()
type_text("Rohit Sharma")

# CLICK SUBMIT (HUMAN)
submit = driver.find_element(By.TAG_NAME, "button")
x, y = element_to_screen(driver, submit)
move_mouse(x, y)
pause()
click()

# WAIT LIKE HUMAN
pause()

# CLOSE POPUP
close_btn = driver.find_element(By.XPATH, "//button[text()='Close']")
x, y = element_to_screen(driver, close_btn)
move_mouse(x, y)
click()

# SCROLL USING PYAUTOGUI
for _ in range(5):
    human_scroll(random.randint(200, 400))

pause()
driver.quit()
