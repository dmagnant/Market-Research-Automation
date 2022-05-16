import time
from Cointiply import runCointiply
from Presearch_MR import runPresearch
from Functions import setDirectory, chromeDriverAsUser, timeOfNextRun

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
