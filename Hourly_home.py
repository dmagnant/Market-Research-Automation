import os
import time
from datetime import datetime

import pyautogui
from selenium.common.exceptions import InvalidArgumentException

from Cointiply import runCointiply
from Functions import (braveBrowserAsUser, chromeDriverAsUser, setDirectory,
                       showMessage, timeOfNextRun)
from Presearch_MR import runPresearch


def clearChromeWindows(directory):
    try:
    
        driver = chromeDriverAsUser(directory)
    except InvalidArgumentException:
        os.system("taskkill /im chrome.exe /f")
        driver = chromeDriverAsUser(directory)
    return driver

directory = setDirectory()
driver = clearChromeWindows(directory)
driver.implicitly_wait(3)
time.sleep(3)
minsLeftForFaucet = runCointiply(directory, driver, True)
runPresearch(driver)
driver.quit()
nextRun = timeOfNextRun(minsLeftForFaucet)
if nextRun.hour == 0:
    minsLeftForFaucet -= datetime.now().time().minute
time.sleep(minsLeftForFaucet * 60)
while True:
    now = datetime.now().time().replace(second=0,microsecond=0)
    driver = clearChromeWindows(directory)
    runFaucet = True if now.hour >= 9 and now.hour < 20 else False
    runPresearch(driver)
    minsLeftForFaucet = runCointiply(directory, driver, runFaucet)
    runPresearch(driver)
    driver.quit()
    nextRun = timeOfNextRun(minsLeftForFaucet)
    time.sleep(minsLeftForFaucet * 60)
    