from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from AmazonGC import confirmAmazonGCBalance
from Bing import runBing
from Cointiply import runCointiply
from Functions import (chromeDriverAsUser, closeExpressVPN, setDirectory,
                       showMessage, startExpressVPN)
from Pinecone import runPinecone
from Presearch_MR import runPresearch
from Swagbucks import runSwagbucks
from Tellwut import runTellwut

directory = setDirectory()
# closeExpressVPN()
driver1 = webdriver.Edge(service = Service(directory + r"\Projects\Coding\webdrivers\msedgedriver.exe"))
# disablePiHole(directory, driver1)
runBing(directory, driver1)
driver1.quit()
driver = chromeDriverAsUser(directory)
runTellwut(driver)
confirmAmazonGCBalance(directory, driver)
runPinecone(driver)
runCointiply(directory, driver)
runPresearch(driver)
runSwagbucks(driver, True)
showMessage("Scripts Complete", 'Click OK to: \n''Enable Pihole \n' 'Close Chrome webdriver \n')
driver.quit()
startExpressVPN()
