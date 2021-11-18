import piecash
from piecash import GnucashException
import ctypes
from Functions import openGnuCashBook

def confirmAmazonGCBalance(directory, driver):
    # Amazon GC balance
    driver.get("https://www.amazon.com/gift-cards")
    balance = driver.find_element_by_xpath("//*[@id='asv-gclp-balance-widget-desktop']/ul/li[1]/span/a").text
    mybook = openGnuCashBook(directory, 'Finance', True, True)

    # Get Balances
    with mybook as book:
        Amazon_GC = mybook.accounts(fullname="Assets:Liquid Assets:Amazon GC")
        amazon_balance = float(Amazon_GC.get_balance())
        book.close()
    if str(amazon_balance) not in balance:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, f'{balance} \n'
                        f'Gnu Cash balance {amazon_balance} \n', "Amazon mismatch", 0)