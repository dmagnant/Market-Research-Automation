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

def timeOfNextRun(faucet_complete):
        hour = faucet_complete.hour
        hourfromcomplete = hour + 1 if hour <= 22 else 0
        minutefromcomplete = faucet_complete.minute if hour > 0 else 0
        return faucet_complete.replace(minute=minutefromcomplete, hour=hourfromcomplete)

time9am = datetime.now().time().replace(hour=9, minute=0, second=0, microsecond=0)
time8pm = datetime.now().time().replace(hour=20, minute=0, second=0, microsecond=0)
time11pm = datetime.now().time().replace(hour=23, minute=0, second=0, microsecond=0)

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
faucet_complete = runCointiply(directory, driver, True)
driver.quit()
nextRun = timeOfNextRun(faucet_complete)
print('next run at ', nextRun)
while True:
    now = datetime.now().time()
    if now > nextRun and now < time11pm:
        driver = clearChromeWindows(directory)
        run_faucet = True if now > time9am and now < time8pm else False
        # run_faucet = False          # activate this line to run passively indefinitely
        runPresearch(driver)
        faucet_complete = runCointiply(directory, driver, run_faucet)
        nextRun = timeOfNextRun(faucet_complete)
        runPresearch(driver)
        driver.quit()
        print('next run at ', nextRun)
    # else:
    #     brave.refresh()
    time.sleep(600)