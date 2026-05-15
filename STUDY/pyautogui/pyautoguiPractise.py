import pyautogui # type: ignore

def cursorLocFinder():
    print(pyautogui.position())


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2

print(pyautogui.size())
print(pyautogui.position())

pyautogui.moveTo(100,30, duration=2)
pyautogui.rightClick()
# other functionalities
# pyautogui.click()
# pyautogui.doubleClick()

pyautogui.moveTo(500,300, duration=1)
pyautogui.click()

pyautogui.scroll(500)
pyautogui.scroll(-500)

# cursorLocFinder()

pyautogui.moveTo(500,960, duration=1)
pyautogui.click()
pyautogui.write("got it", interval=1)
# pyautogui.press("enter")
pyautogui.hotkey("ctrl","shift","t")