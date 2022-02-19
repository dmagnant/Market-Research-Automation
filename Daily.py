from selenium import webdriver
from Functions import setDirectory, chromeDriverAsUser, closeExpressVPN, startExpressVPN, disablePiHole, enablePiHole, showMessage
from Cointiply import runCointiply
from Presearch_MR import runPresearch
from Swagbucks import runSwagbucks
from Bing import runBing
from Tellwut import runTellwut
from Pinecone import runPinecone
from AmazonGC import confirmAmazonGCBalance

directory = setDirectory()
closeExpressVPN()
driver1 = webdriver.Edge(executable_path=(directory + r"\Projects\Coding\webdrivers\msedgedriver.exe"))
# disablePiHole(directory, driver1)
runBing(directory, driver1)
driver1.minimize_window()
driver = chromeDriverAsUser(directory)
runTellwut(driver)
confirmAmazonGCBalance(directory, driver)
runPinecone(driver)
runCointiply(directory, driver)
runPresearch(driver)
runSwagbucks(driver, True)
showMessage("Scripts Complete", 'Click OK to: \n''Enable Pihole \n' 'Close Chrome webdriver \n')
driver.quit()
driver1.maximize_window()
# enablePiHole(directory, driver1)
driver1.quit()
startExpressVPN()