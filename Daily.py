from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchWindowException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import ctypes
import piecash
from piecash import GnucashException
import random
import pyautogui
from random_word import RandomWords
import pygetwindow
import win32gui
from Functions import setDirectory, chromeDriverAsUser, getKeePassUsername, getKeePassPassword, enumHandler, closeExpressVPN
from Cointiply import runCointiply
from Presearch import runPresearch

directory = setDirectory()
driver = chromeDriverAsUser(directory)
closeExpressVPN()

#Disable Pihole
edgedriver = directory + r"\Projects\Coding\webdrivers\msedgedriver.exe"
driver1 = webdriver.Edge(executable_path=edgedriver)
driver1.implicitly_wait(5)
driver1.get("http://192.168.1.144/admin/")
driver1.maximize_window()
#click Login
driver1.find_element_by_xpath("/html/body/div[2]/aside/section/ul/li[3]/a").click()
# Enter Password
driver1.find_element_by_id("loginpw").send_keys(getKeePassPassword(directory, 'Pi hole'))
#click Login again
driver1.find_element_by_xpath("//*[@id='loginform']/div[2]/div/button").click()
time.sleep(1)
#Click Disable
try:
    driver1.find_element_by_xpath("//*[@id='pihole-disable']/a/span[2]").click()
    # Click Indefinitely
    driver1.find_element_by_xpath("//*[@id='pihole-disable-indefinitely']").click()
except ElementNotInteractableException:
    exception = "already disabled"

# # BING REWARDS
# LOAD PAGE
driver1.execute_script("window.open('https://account.microsoft.com/rewards/');")
bing_window = driver1.window_handles[1]
driver1.switch_to.window(bing_window)
# click Sign in
driver1.find_element_by_xpath("/html/body/div[1]/div[2]/main/section/div[1]/div[2]/section/div[1]/a[2]").click()
# login
try:
    # enter username
    driver1.find_element_by_id("i0116").send_keys(getKeePassUsername(directory, 'Bing Rewards'))
    time.sleep(1)
    # click Next
    driver1.find_element_by_id("idSIButton9").click()
    time.sleep(1)
    # enter password
    driver1.find_element_by_id("i0118").send_keys(getKeePassPassword(directory, 'Bing Rewards'))
    time.sleep(1)
    # click Sign in
    driver1.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div/div/input").click()
    time.sleep(1)
    # click to stay signed in
    driver1.find_element_by_xpath("/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input").click()
    # click sign in link
    driver1.find_element_by_xpath("/html/body/div[1]/div[2]/main/section/div[1]/div[2]/section/div[1]/a[2]").click()
except NoSuchElementException:
    exception = "already logged in"
# click on "points" links
links = driver1.find_elements_by_partial_link_text("points")
links[0].click()
time.sleep(1)
window_after = driver1.window_handles[2]
driver1.switch_to.window(window_after)
driver1.close()
driver1.switch_to.window(bing_window)
# capture balance
time.sleep(3)
mr_balance = driver1.find_element_by_xpath("//*[@id='userBanner']/mee-banner/div/div/div/div[2]/div[1]/mee-banner-slot-2/mee-rewards-user-status-item/mee-rewards-user-status-balance/div/div/div/div/div/p[1]/mee-rewards-counter-animation/span").text.replace(",", "")
if int(mr_balance) >= 5250:
    # go to $5 Amazon gift card link
    driver1.get("https://rewards.microsoft.com/redeem/000800000000")
    time.sleep(3)
    # click Redeem Reward
    driver1.find_element_by_xpath("//*[@id='redeem-pdp_000800000000']/span[1]").click()
    # click Confirm Reward
    driver1.find_element_by_xpath("//*[@id='redeem-checkout-review-confirm']/span[1]").click()
    try:
        # enter Phone number
        driver1.find_element_by_id("redeem-checkout-challenge-fullnumber").send_keys(os.environ.get('Phone'))
        # click Send
        driver1.find_element_by_xpath("//*[@id='redeem-checkout-challenge-validate']/span").click()
    except NoSuchElementException:
        exception = "caught"
driver1.minimize_window()

# # TELLWUT
# LOAD PAGE
driver.implicitly_wait(5)
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

# Amazon GC balance
driver.get("https://www.amazon.com/gift-cards")
balance = driver.find_element_by_xpath("//*[@id='asv-gclp-balance-widget-desktop']/ul/li[1]/span/a").text

# # Open Gnu Cash file
Finance_book = directory + r"\Finances\Personal Finances\Finance.gnucash"
try:
    mybook = piecash.open_book(Finance_book, readonly=False)
except GnucashException:
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, f'Close Gnucash file then click OK \n'
               , "Gnucash file open", 0)
    mybook = piecash.open_book(Finance_book, readonly=False)
# Get Balances
with mybook as book:
    Amazon_GC = mybook.accounts(fullname="Assets:Liquid Assets:Amazon GC")
    amazon_balance = float(Amazon_GC.get_balance())
    book.close()
if str(amazon_balance) not in balance:
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, f'{balance} \n'
                     f'Gnu Cash balance {amazon_balance} \n', "Amazon mismatch", 0)

# Pinecone Research
driver.get("https://members.pineconeresearch.com/#/Login")
time.sleep(2)
driver.refresh()
time.sleep(2)
# click login
driver.find_element_by_xpath("//*[@id='mainContainer']/div/div/div[1]/div/form/button").click()
time.sleep(5)
try:
    # Click Redeem
    driver.find_element_by_id("3").click()
    # Click Shop
    driver.find_element_by_xpath("//*[@id='navbarContent']/ul/li[3]/a").click()
    # click WishList
    driver.find_element_by_xpath("//*[@id='navbarContent']/ul/li[3]/div/a[4]").click()
    # capture Pinecone Balance
    pc_balance = driver.find_element_by_xpath("/html/body/div[2]/header/nav[1]/div/div/div/div[2]/div/div[2]/div[1]/small").text.replace("points", '').replace(",", '')
    # Redeem if there is a balance
    if float(pc_balance) >= 300:
        # click link for product
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/span[1]/a").click()
        # Click add to cart
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/form/div/div[2]/input").click()
        if float(pc_balance) > 300:
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, f'code redemption of Pinecone > 300pts'
                       , "balance higher than 300", 0)
        # click checkout
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[4]/div[1]/div/div[2]/div/div/table/tbody/tr[5]/td/a").click()
        # click Review Order
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div/div[2]/div/form/div[2]/div/button").click()
        # click Place Order
        driver.find_element_by_xpath("/html/body/div[2]/div/div/div[3]/div/div[3]/div/table/tbody/tr[5]/td/form/button").click()
except NoSuchElementException:
    # skip if prompted for security question
    exception = "caught"

runCointiply(directory, driver)
runPresearch(driver)

# Swagbucks
driver.get("https://www.swagbucks.com/")
try:
    driver.find_element_by_id("lightboxExit").click()
except ElementNotInteractableException:
    exception = "caught"
except NoSuchElementException:
    exception = "caught"

#Play Alus Revenge
driver.execute_script("window.open('https://www.swagbucks.com/games/play/319/alu-s-revenge-2?tid=113');")
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
time.sleep(2)

# move window to primary monitor
Alu = pygetwindow.getWindowsWithTitle("Alu's Revenge 2 - Free Online Games | Swagbucks - Google Chrome")[0]
Alu.resizeTo(100, 100)
win32gui.EnumWindows(enumHandler, "Alu's Revenge")
Alu.maximize()
# win = ahk.win_get(title="Alu's Revenge 2 - Free Online Games | Swagbucks - Google Chrome")
# win.move(0, 0)
# win.activate()
# driver.maximize_window()

# click Play for Free
driver.implicitly_wait(20)
driver.find_element_by_id("gamesItemBtn").click()
time.sleep(3)
redeemed = 0
while redeemed < 5:
    game_over_text = ""
    num = 0
    # click Play Now
    pyautogui.leftClick(850, 972)
    time.sleep(1)
    # click Play Now (again)
    pyautogui.leftClick(938, 803)
    time.sleep(1)
    # click to remove "goal screen" and start game
    pyautogui.leftClick(872, 890)
    time.sleep(2)
    # click tiles
    pyautogui.leftClick(680, 1030)
    pyautogui.leftClick(750, 1030)
    pyautogui.leftClick(825, 1030)
    pyautogui.leftClick(900, 1030)
    pyautogui.leftClick(975, 1030)
    pyautogui.leftClick(1025, 1030)
    time.sleep(25)
    while num < 5:
        # if Game over screen up
        if driver.find_element_by_id("closeEmbedContainer"):
            time.sleep(5)
            #read response
            game_over_text = driver.find_element_by_xpath("//*[@id='embedGameOverHdr']/h3").text
            if game_over_text != "":
                if game_over_text != "No SB this time. Keep trying...":
                    redeemed += 1
                # click Play again
                driver.find_element_by_id("gamePlayAgainBtn").click()
                time.sleep(3)
                break
        num += 1

#Daily Poll
driver.implicitly_wait(5)
driver.get("https://www.swagbucks.com/polls")
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
pyautogui.leftClick(1400, 780)

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
        driver.find_element_by_id("sbGlobalNavSearchInputWeb").send_keys(RandomWords().get_random_word())
        time.sleep(random.choice(delay))
        driver.find_element_by_id("sbGlobalNavSearchInputWeb").send_keys(Keys.ENTER)
        searches += 1
    except NoSuchWindowException:
        num = 3
    except WebDriverException:
        num = 3

MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox(None, f'Click OK to: \n'
                 f'Enable Pihole \n'
                 f'Close Chrome webdriver \n'
            , "Script complete", 0)

driver.quit()

# Enable Pihole
driver1.maximize_window()
pihole_window = driver1.window_handles[0]
driver1.switch_to.window(pihole_window)
try:
    # click Login
    driver1.find_element_by_xpath("/html/body/div[2]/aside/section/ul/li[3]/a").click()
    # Enter Password
    driver1.find_element_by_id("loginpw").send_keys(getKeePassPassword(directory, 'Pi hole'))
    # click Login again
    driver1.find_element_by_xpath("//*[@id='loginform']/div[2]/div/button").click()
    time.sleep(1)
except NoSuchElementException:
    exception = "already logged in"
try:
    driver1.find_element_by_id("enableLabel").click()
except NoSuchElementException:
     exception = "already enabled"

driver1.quit()