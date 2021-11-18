from Cointiply import runCointiply
from Presearch import runPresearch
from Functions import setDirectory, chromeDriverAsUser

# set directory
directory = setDirectory()
# load webdriver
driver = chromeDriverAsUser(directory)

runCointiply(directory, driver)
runPresearch(driver)
driver.quit()