from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from Functions import setDirectory, chromeDriverAsUser, closeExpressVPN, timeOfNextRun
from Sites.Cointiply import runCointiply
from Sites.Presearch_MR import runPresearch
from Sites.Swagbucks import runSwagbucks
from Sites.Bing import runBing
from Sites.Tellwut import runTellwut

directory = setDirectory()
closeExpressVPN()
driver1 = webdriver.Edge(service = Service(directory + r"\Projects\Coding\webdrivers\msedgedriver.exe"))
# disablePiHole(directory, driver1)
runBing(directory, driver1)
driver1.quit()
driver = chromeDriverAsUser(directory)
runTellwut(driver)
runSwagbucks(driver, True, "office")
driver.quit()
while True:
    driver = chromeDriverAsUser(directory)
    runCointiply(directory, driver, False)
    runPresearch(driver)
    driver.quit()
    timeOfNextRun(60)

    time.sleep(3600)