from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from Functions import setDirectory, chromeDriverAsUser, closeExpressVPN, startExpressVPN, showMessage
from Sites.Cointiply import runCointiply
from Sites.Presearch_MR import runPresearch
from Sites.Swagbucks import runSwagbucks
from Sites.Bing import runBing
from Sites.Tellwut import runTellwut
from Sites.Pinecone import runPinecone
from Sites.AmazonGC import confirmAmazonGCBalance

directory = setDirectory()
closeExpressVPN()
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