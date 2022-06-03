import time

from random_word import RandomWords

from Functions import chromeDriverAsUser


def runPresearch(driver):
    search_prefix = "https://testnet-engine.presearch.org/search?q="
    search_term = None
    while search_term is None:
        search_term = RandomWords().get_random_word()
    time.sleep(1)
    search_path = search_prefix + search_term
    driver.get(search_path)
    time.sleep(1)

if __name__ == '__main__':
    driver = chromeDriverAsUser()
    runPresearch(driver)
