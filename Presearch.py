import time
import random
from random_word import RandomWords
from Functions import setDirectory, chromeDriverAsUser, getKeePassUsername, getKeePassPassword, enumHandler

# set directory
directory = setDirectory()

# load driver and webpage
driver = chromeDriverAsUser(directory)

def Presearch(driver):
    # Presearch
    search_prefix = "https://testnet-engine.presearch.org/search?q="
    delay = [1, 2, 3]
    num = 0
    while num < 2:
        search_term = RandomWords().get_random_word()
        search_path = search_prefix + search_term
        driver.get(search_path)
        num += 1
        time.sleep(random.choice(delay))
Presearch(driver)
driver.quit()