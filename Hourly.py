from selenium.common.exceptions import InvalidArgumentException
import os
from datetime import datetime
import time
import pyautogui
from Cointiply import runCointiply
from Presearch_MR import runPresearch
from Functions import setDirectory, chromeDriverAsUser, braveBrowserAsUser

def clearChromeWindows(directory):
    try:
        driver = chromeDriverAsUser(directory)
    except InvalidArgumentException:
        os.system("taskkill /im chrome.exe /f")
        driver = chromeDriverAsUser(directory)
    return driver

def timeOfNextRun(minsLeftForFaucet):
    now = datetime.now().time().replace(second=0, microsecond=0)
    nextRunMinute = now.minute + minsLeftForFaucet
    nextRunHour = now.hour
    # adjust for minutes going over 60
    if (nextRunMinute > 60):
        nextRunMinute = abs(nextRunMinute - 60)
        nextRunHour += 1 if nextRunHour < 23 else 0
    nextRun = now.replace(hour=nextRunHour, minute=nextRunMinute)
    print('next run at ', str(nextRun.hour) + ":" + "{:02d}".format(nextRun.minute))
    return nextRun

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
time.sleep(3)
minsLeftForFaucet = runCointiply(directory, driver, True)
driver.quit()
# calculate next run time
nextRun = timeOfNextRun(minsLeftForFaucet)
while True:
    now = datetime.now().time()
    if now > nextRun:
        driver = clearChromeWindows(directory)
        runFaucet = True if now.hour >= 9 and now.hour <= 20 else False
        # runFaucet = False          # activate this line to run passively indefinitely
        runPresearch(driver)
        minsLeftForFaucet = runCointiply(directory, driver, runFaucet)
        nextRun = timeOfNextRun(minsLeftForFaucet)
        runPresearch(driver)
        driver.quit()
    # else:
    #     brave.refresh()
    time.sleep(minsLeftForFaucet * 60)