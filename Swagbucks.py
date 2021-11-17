from __future__ import print_function

import ctypes
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, NoSuchWindowException, WebDriverException
from selenium import webdriver
import time
import csv
import random
from ahk import AHK
from selenium.webdriver.common.keys import Keys
import socket
import pyautogui

#get computer name
computer = socket.gethostname()

# computer-specific file paths
if computer == "Big-Bertha":
    google_drive = r"C:\Users\dmagn\Google Drive"
elif computer == "Black-Betty":
    google_drive = r"D:\Google Drive"

ahk = AHK()

# load webdriver
chromedriver = google_drive + r"\Projects\Coding\webdrivers\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=C:\Users\dmagn\AppData\Local\Google\Chrome\User Data")
driver = webdriver.Chrome(executable_path=chromedriver, options=options)
driver.implicitly_wait(2)
driver.get("https://www.swagbucks.com/")
driver.maximize_window()
try:
    driver.find_element_by_id("lightboxExit").click()
except ElementNotInteractableException:
    exception = "caught"
except NoSuchElementException:
    exception = "caught"

# NO ALUS REVENGE

#Daily Poll
driver.implicitly_wait(5)
driver.execute_script("window.open('https://www.swagbucks.com/polls');")
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
time.sleep(1)
try:
    # click on first answer
    driver.find_element_by_css_selector("td.pollMainAnswerText").click()
    # click Vote & Earn
    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[5]/div[2]/div[2]/div[1]/div[1]").click()
except NoSuchElementException:
    exception = "already answered"

#Coupons
driver.get("https://www.swagbucks.com/shop/allcoupons/grocery")
time.sleep(2)
#scroll down
pyautogui.scroll(-1500)
time.sleep(2)
ahk.click(1400, 780)

#AdGate Media
driver.execute_script("window.open('https://www.swagbucks.com/discover/offer-walls/151/adgate-media');")
window_after = driver.window_handles[2]
driver.switch_to.window(window_after)

#Inbox
driver.execute_script("window.open('https://www.swagbucks.com/g/inbox');")
window_after = driver.window_handles[3]
driver.switch_to.window(window_after)


#Answer
driver.execute_script("window.open('https://www.swagbucks.com/surveys');")
window_after = driver.window_handles[4]
driver.switch_to.window(window_after)

# To Do List
main = driver.window_handles[4]
list_item_num = 1
button_num = 1
button_not_clicked = True
while list_item_num <= 8:
    try:
        # look for Daily Bonus header 
        driver.find_element_by_xpath("/html/body/div[2]/div[1]/header/nav/div[3]/div/div/div/div[1]/h4")
    except NoSuchElementException:
        try:
            # if not visible, click to show To Do List
            driver.find_element_by_xpath("/html/body/div[2]/div[1]/header/nav/div[3]/button/span/span[1]").click()
        except NoSuchElementException:
            break
    time.sleep(1)
    # get title of List Item
    list_item = driver.find_element_by_xpath("/html/body/div[2]/div[1]/header/nav/div[3]/div/div/div/div[2]/div/section[1]/div/ul/li[" + str(list_item_num) + "]/a")
    if list_item.text == "Add In-Store Deal":
        list_item.click()
        time.sleep(1)
        # window_after = driver.window_handles[5]
        # driver.switch_to.window(window_after)
        while button_not_clicked:
            try:
                driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/main/div/div[2]/div[2]/div[2]/div/div/a[" + str(button_num) +"]/div[2]/button[1]").click()
                button_not_clicked = False
            except ElementNotInteractableException:
                exception = "already clicked"
                button_num += 1
        # driver.close()
        # driver.switch_to.window(main)
    elif list_item.text == "Deal of the Day":
        list_item.click()
        time.sleep(6)
        # window_after = driver.window_handles[5]
        # driver.switch_to.window(window_after)
        # driver.close()
        # driver.switch_to.window(main)
    elif list_item.text == "Daily Watch":
        list_item.click()
        # window_after = driver.window_handles[5]
        # driver.switch_to.window(window_after)
        driver.implicitly_wait(20)
        try:
            driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div/button").click()
            time.sleep(2)
        except NoSuchElementException:
            exception = "caught"
        # click Discover Content
        driver.find_element_by_xpath("/html/body/div/div/div/div/div[5]/a").click()
        time.sleep(3)
        driver.switch_to.window(main)
    list_item_num += 1

#Daily Search
words = google_drive + r"\Projects\Coding\Python\Market Research\Resources\words.csv"
search_window = driver.window_handles[0]
driver.switch_to.window(search_window)
driver.implicitly_wait(5)
delay = [1, 2, 3]
searches = 0
num = 0
while num < 2:
    try:
        driver.find_element_by_xpath("//*[@id='tblAwardBannerAA']/div[2]/div/div[1]/form/input[2]")
        num += 1
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, f'Total searches: {searches} \n'
                         f'redemptions: {num} \n'
                   , "Redeem Swagbucks", 0)
    except NoSuchElementException:
        try:
            driver.find_element_by_id("lightboxExit").click()
        except NoSuchElementException:
            try:
                driver.find_element_by_id("daily-goal-celebration__exitCta--2VEiu").click()
            except NoSuchElementException:
                exception = "no award box"
        except ElementNotInteractableException:
            exception = "caught"
        driver.find_element_by_id("sbLogoLink").click()
        time.sleep(1)
        searches += 1
        with open(words, 'r') as t1:
            csv_reader = csv.reader(t1, delimiter=',')
            for row in csv_reader:
                driver.find_element_by_id("sbGlobalNavSearchInputWeb").send_keys(random.choice(row) + " " + random.choice(row))
        time.sleep(random.choice(delay))
        driver.find_element_by_id("sbGlobalNavSearchInputWeb").send_keys(Keys.ENTER)
    except NoSuchWindowException:
        num = 3
    except WebDriverException:
        num = 3