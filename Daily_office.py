import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from Bing import runBing
from Cointiply import runCointiply
from Functions import (chromeDriverAsUser, closeExpressVPN, setDirectory,
                       timeOfNextRun)
from Presearch_MR import runPresearch
from Swagbucks import runSwagbucks
from Tellwut import runTellwut

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
