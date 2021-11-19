import ctypes
import time
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

def runTellwut(driver):
    # LOAD PAGE
    driver.implicitly_wait(3)
    driver.get("https://www.tellwut.com/signin")
    # Login
    try:
        driver.find_element_by_xpath("//*[@id='signinForm']/div[4]/div/button").click()
    except NoSuchElementException:
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, "complete captcha, then click OK", 'Captcha', 0)
    try:
        driver.find_element_by_xpath("//*[@id='signinForm']/div[5]/div/button").click()
    except NoSuchElementException:
        exception = "already logged in"
    driver.maximize_window()
    time.sleep(1)
    # Click Home
    driver.find_element_by_xpath("//*[@id='header']/nav[1]/div/ul/li[1]/a").click()
    while True:
        try:
            # look for "Start Survey" button
            driver.find_element_by_xpath("/html/body/div/main/div[2]/div[2]/div[1]/form/div[1]/div/button").click()
        except NoSuchElementException:
            try:
                # look for submit button
                driver.find_element_by_xpath("//input[@id='survey_form_submit']")
                # if no submit button, stop
            except NoSuchElementException:
                break
        # click on all radio buttons
        for i in driver.find_elements_by_xpath("//input[@type='radio']"):
            try:
                i.click()
            except ElementNotInteractableException:
                exception = "caught"
        # click on all checkboxes
        for i in driver.find_elements_by_xpath("//input[@class='answerListOption']"):
            try:
                i.click()
            except ElementNotInteractableException:
                exception = "caught"
        # Click Submit
        driver.find_element_by_xpath("//input[@id='survey_form_submit']").click()
        time.sleep(3)
        # re-load the webpage to load new survey
        driver.get("https://www.tellwut.com/")
    # Check balance and Redeem
    tellwut_balance = driver.find_element_by_xpath("/html/body/div/header/div/div/div/div[4]/div/div/div[2]/div[1]/span").text
    if int(tellwut_balance) >= 4000:
        driver.find_element_by_xpath("//*[@id='header']/nav[1]/div/ul/li[2]/a").click()
        time.sleep(1)
        driver.find_element_by_partial_link_text("$10 Amazon.com Gift Card").click()
        driver.find_element_by_id("checkout_form_submit").click()
        driver.find_element_by_id("form_button").click()