from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchWindowException, WebDriverException, ElementClickInterceptedException
import time
import random
from selenium.webdriver.common.keys import Keys
import pyautogui
import win32gui
import pygetwindow
from random_word import RandomWords
from Functions import enumHandler, closeExpressVPN, showMessage

def runAlusRevenge(driver, run_Alu):
    if run_Alu:
        closeExpressVPN()
        #Play Alus Revenge
        driver.get('https://www.swagbucks.com/games/play/319/alu-s-revenge-2?tid=113')
        time.sleep(2)

        # move window to primary monitor
        Alu = pygetwindow.getWindowsWithTitle("Alu's Revenge 2 - Free Online Games | Swagbucks - Google Chrome")[0]
        Alu.resizeTo(100, 100)
        win32gui.EnumWindows(enumHandler, "Alu's Revenge")
        Alu.maximize()

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
        driver.get("https://www.swagbucks.com/")

def runSwagbucks(driver, run_Alu):
    closeExpressVPN()
    driver.implicitly_wait(2)
    driver.get("https://www.swagbucks.com/")
    driver.maximize_window()
    try:
        driver.find_element_by_id("lightboxExit").click()
    except ElementNotInteractableException:
        exception = "caught"
    except NoSuchElementException:
        exception = "caught"

    runAlusRevenge(driver, run_Alu)

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
            while button_not_clicked:
                try:
                    driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/main/div/div[2]/div[2]/div[2]/div/div/a[" + str(button_num) +"]/div[2]/button[1]").click()
                    button_not_clicked = False
                except ElementNotInteractableException:
                    exception = "already clicked"
                    button_num += 1
        elif list_item.text == "Deal of the Day":
            list_item.click()
            time.sleep(6)
        elif list_item.text == "Daily Watch":
            list_item.click()
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
    driver.implicitly_wait(3)
    delay = [1, 2, 3]
    searches = 0
    num = 0
    while num < 2:
        search_term1, search_term2 = None
        search_term = None
        try:
            # accept reward
            driver.find_element_by_xpath("//*[@id='tblAwardBannerAA']/div[2]/div/div[1]/form/input[2]")
            num += 1
            showMessage("Redeem Swagbucks", f'Total searches: {searches} \n' f'redemptions: {num} \n')
        # if no reward, continue searching
        except NoSuchElementException:
            time.sleep(1)
            try:
                driver.find_element_by_id("sbLogoLink").click()
            # light-box pop-up in the way
            except ElementClickInterceptedException:
                try: 
                    driver.find_element_by_id("lightboxExit").click()
                except NoSuchElementException:
                    try: 
                        driver.find_element_by_id("daily-goal-celebration__exitCta--2VEiu").click()
                    except ElementNotInteractableException:
                        exception = "caught"
                driver.find_element_by_id("sbLogoLink").click()
            time.sleep(1)
            searches += 1
            while search_term1 is None:
                search_term1 = RandomWords().get_random_word()
            while search_term2 is None:
                search_term2 = RandomWords().get_random_word()
            search_term = search_term1 + " " + search_term2
            driver.find_element_by_id("sbGlobalNavSearchInputWeb").send_keys(search_term)
            driver.find_element_by_id("sbGlobalNavSearchInputWeb").send_keys(Keys.ENTER)
            time.sleep(random.choice(delay))
        except NoSuchWindowException:
            num = 3
        except WebDriverException:
            num = 3