import ctypes
from Functions import openGnuCashBook, showMessage

def confirmAmazonGCBalance(directory, driver):
    driver.get("https://www.amazon.com/gift-cards")
    balance = driver.find_element_by_xpath("//*[@id='asv-gclp-balance-widget-desktop']/ul/li[1]/span/a").text
    mybook = openGnuCashBook(directory, 'Finance', True, True)
    with mybook as book:
        amazon_balance = mybook.accounts(fullname="Assets:Liquid Assets:Amazon GC").get_balance()
        book.close()
    if str(amazon_balance) not in balance:
        showMessage("Amazon GC Mismatch", f'{balance} \n' f'Gnu Cash balance {amazon_balance} \n')
