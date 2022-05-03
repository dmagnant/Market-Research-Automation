import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
from Functions import showMessage

def runTellwut(driver):
    # LOAD PAGE
    driver.implicitly_wait(3)
    driver.get("https://www.tellwut.com/signin")
    # Login
    try:
        driver.find_element(By.XPATH, "//*[@id='signinForm']/div[4]/div/button").click()
    except NoSuchElementException:
        showMessage('Captcha', "complete captcha, then click OK")
    try:
        driver.find_element(By.XPATH, "//*[@id='signinForm']/div[5]/div/button").click()
    except NoSuchElementException:
        exception = "already logged in"
    time.sleep(1)
    # Click Home
    driver.find_element(By.XPATH, "//*[@id='header']/nav[1]/div/ul/li[1]/a").click()
    while True:
        try:
            # look for "Start Survey" button
            driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[2]/div[1]/form/div[1]/div/button").click()
        except NoSuchElementException:
            try:
                # look for submit button
                driver.find_element(By.XPATH, "//input[@id='survey_form_submit']")
                # if no submit button, stop
            except NoSuchElementException:
                break
        # click on all radio buttons
        for i in driver.find_elements(By.XPATH, "//input[@type='radio']"):
            try:
                i.click()
            except ElementNotInteractableException:
                exception = "caught"
        # click on all checkboxes
        for i in driver.find_elements(By.XPATH,"//input[@type='checkbox']"):
            try:
                i.click()
            except (ElementNotInteractableException, ElementClickInterceptedException):
                exception = "caught"
        # Click Submit
        driver.find_element(By.XPATH, "//input[@id='survey_form_submit']").click()
        time.sleep(3)
        # re-load the webpage to load new survey
        driver.get("https://www.tellwut.com/")
    # Check balance and Redeem
    tellwut_balance = driver.find_element(By.XPATH, "/html/body/div/header/div/div/div/div[4]/div/div/div[2]/div[1]/div[1]").text
    if int(tellwut_balance) >= 4000:
        driver.find_element(By.XPATH, "//*[@id='header']/nav[1]/div/ul/li[2]/a").click()
        time.sleep(1)
        driver.find_element(By.PARTIAL_LINK_TEXT, "$10 Amazon.com Gift Card").click()
        driver.find_element(By.ID, "checkout_form_submit").click()
        driver.find_element(By.ID, "form_button").click()
        time.sleep(3)
