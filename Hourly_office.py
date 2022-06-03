import time

from Cointiply import runCointiply
from Functions import chromeDriverAsUser, setDirectory, timeOfNextRun
from Presearch_MR import runPresearch


def runHourlyOffice(directory=setDirectory()):
    while True:
        driver = chromeDriverAsUser(directory)
        driver.implicitly_wait(3)
        runCointiply(directory, driver, False)
        runPresearch(driver)
        driver.quit()
        timeOfNextRun(60)
        time.sleep(3600)
runHourlyOffice()
