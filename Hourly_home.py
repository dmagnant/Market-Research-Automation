from selenium.common.exceptions import InvalidArgumentException
import os
from datetime import datetime
import time
import pyautogui
from Cointiply import runCointiply
from Presearch_MR import runPresearch
from Functions import setDirectory, chromeDriverAsUser, braveBrowserAsUser, showMessage, timeOfNextRun

def clearChromeWindows(directory):
    try:
    
        driver = chromeDriverAsUser(directory)
    except InvalidArgumentException:
        os.system("taskkill /im chrome.exe /f")
        driver = chromeDriverAsUser(directory)
    return driver

directory = setDirectory()

# brave = braveBrowserAsUser(directory)
# with pyautogui.hold('ctrl'):
#     pyautogui.press('t')
# brave.switch_to.window(brave.window_handles[0])
# while len(brave.window_handles) > 1:
#     brave.close()
#     brave.switch_to.window(brave.window_handles[0])
# brave.minimize_window()

driver = clearChromeWindows(directory)
driver.implicitly_wait(3)
time.sleep(3)
minsLeftForFaucet = runCointiply(directory, driver, True)
driver.quit()
# calculate next run time
nextRun = timeOfNextRun(minsLeftForFaucet)
if nextRun.hour == 0:
    minsLeftForFaucet -= datetime.now().time().minute
time.sleep(minsLeftForFaucet * 60)
while True:
    now = datetime.now().time().replace(second=0,microsecond=0)
    driver = clearChromeWindows(directory)
    runFaucet = True if now.hour >= 9 and now.hour < 20 else False
    # runFaucet = False          # activate this line to run passively indefinitely
    runPresearch(driver)
    minsLeftForFaucet = runCointiply(directory, driver, runFaucet)
    runPresearch(driver)
    driver.quit()
    nextRun = timeOfNextRun(minsLeftForFaucet)
    # else:
    #     brave.refresh()
    time.sleep(minsLeftForFaucet * 60)
    