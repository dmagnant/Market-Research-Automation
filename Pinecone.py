import ctypes
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from Functions import chromeDriverAsUser


def runPinecone(driver):
    # Pinecone Research
    driver.get("https://members.pineconeresearch.com/#/Login")
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    # click login
    driver.find_element(By.XPATH, "//*[@id='mainContainer']/div/div/div[1]/div/form/button").click()
    time.sleep(3)
    balance = ''
    while balance == '':
        balance = driver.find_element(By.XPATH, "//*[@id='basic-navbar-nav']/div/form/button/div").text
    if float(balance) >= 300:
        try:
            # Click Redeem
            driver.get('https://rewards.pineconeresearch.com/')
            # Click Shop
            driver.find_element(By.XPATH, "//*[@id='navbarContent']/ul/li[5]/a").click()
            # click WishList
            driver.find_element(By.XPATH, "//*[@id='navbarContent']/ul/li[3]/div/a[4]").click()
            # click link for product
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/span[1]/a").click()
            # Click add to cart
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/form/div/div[2]/input").click()
            if float(balance) > 300:
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, 'code redemption of Pinecone > 300pts'
                        , "balance higher than 300", 0)
            # click checkout
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[1]/div/div[2]/div/div/table/tbody/tr[5]/td/a").click()
            # click Review Order
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[2]/div/form/div[2]/div/button").click()
            # click Place Order
            driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div[3]/div/table/tbody/tr[5]/td/form/button").click()
        except NoSuchElementException:
            # skip if prompted for security question
            exception = "caught"

if __name__ == '__main__':
    driver = chromeDriverAsUser()
    runPinecone(driver)
