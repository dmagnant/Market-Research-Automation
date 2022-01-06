from selenium.common.exceptions import InvalidArgumentException
import os
from datetime import datetime
import time

from Cointiply import runCointiply
from Presearch_MR import runPresearch
from Functions import setDirectory, chromeDriverAsUser

directory = setDirectory()

while True:
    now = datetime.now().time()
    today9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    today8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
    run_faucet = True if now > today9am and now < today8pm else False
    # run_faucet = False          # activate this line to run passively (such as when away for weekend)
    try:
        driver = chromeDriverAsUser(directory)
    except InvalidArgumentException:
        os.system("taskkill /im chrome.exe /f")
        driver = chromeDriverAsUser(directory)
    runPresearch(driver)
    faucet_complete = runCointiply(directory, driver, run_faucet)
    runPresearch(driver)
    driver.quit()
    script_complete = datetime.now().time()

    def findDiff(time_diff):
        return time_diff if (time_diff) >= 0 else time_diff + 60

    def PTCAdTime(faucet_complete, script_complete):
        min_diff = script_complete.minute - faucet_complete.minute
        minutes_ran = findDiff(min_diff)
        sec_diff = script_complete.second - faucet_complete.second
        seconds_ran = findDiff(sec_diff)
        return minutes_ran * 60 + seconds_ran

    time_to_wait = 3600 - PTCAdTime(faucet_complete, script_complete)
    print('next run at ', faucet_complete.replace(hour=now.hour+1))
    time.sleep(time_to_wait)
