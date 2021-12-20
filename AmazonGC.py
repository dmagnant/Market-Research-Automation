from Functions import openGnuCashBook, showMessage

def confirmAmazonGCBalance(directory, driver):
    driver.get("https://www.amazon.com/gc/balance")
    balance = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/h2/span").text
    mybook = openGnuCashBook(directory, 'Finance', True, True)
    with mybook as book:
        amazon_balance = mybook.accounts(fullname="Assets:Liquid Assets:Amazon GC").get_balance()
        book.close()
    if str(amazon_balance) not in balance:
        showMessage("Amazon GC Mismatch", f'{balance} \n' f'Gnu Cash balance {amazon_balance} \n')
