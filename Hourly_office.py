import time
from Sites.Cointiply import runCointiply
from Sites.Presearch_MR import runPresearch
from Functions import setDirectory, chromeDriverAsUser, timeOfNextRun

def runHourlyOffice(directory=setDirectory()):
    while True:
        driver = chromeDriverAsUser(directory)
        runCointiply(directory, driver, False)
        runPresearch(driver)
        driver.quit()
        timeOfNextRun(60)
        time.sleep(3600)
runHourlyOffice()
