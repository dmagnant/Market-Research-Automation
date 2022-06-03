from selenium.webdriver.common.by import By

from Functions import (chromeDriverAsUser, openGnuCashBook, setDirectory,
                       showMessage)


def confirmAmazonGCBalance(directory, driver):
    driver.get("https://www.amazon.com/gc/balance")
    balance = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/h2/span").text.strip('$')
    mybook = openGnuCashBook(directory, 'Finance', True, True)
    with mybook as book:
        amazonBalance = mybook.accounts(fullname="Assets:Liquid Assets:Amazon GC").get_balance()
        book.close()
    if str(amazonBalance) != balance:
        showMessage("Amazon GC Mismatch", f'Amazon balance: {balance} \n' f'Gnu Cash balance: {amazonBalance} \n')

if __name__ == '__main__':
    directory = setDirectory()
    driver = chromeDriverAsUser(directory)
    confirmAmazonGCBalance(directory, driver)
