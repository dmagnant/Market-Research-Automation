from Cointiply import runCointiply
from Presearch_MR import runPresearch
from Functions import setDirectory, chromeDriverAsUser

directory = setDirectory()
driver = chromeDriverAsUser(directory)
runPresearch(driver)
runCointiply(directory, driver)
runPresearch(driver)
driver.quit()