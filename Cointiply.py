from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException
import time
import cv2
import numpy as np
import pyautogui
import pygetwindow
from datetime import datetime
# from matplotlib import pyplot as plt
from Functions import getUsername, getPassword, showMessage

def runCointiply(directory, driver, run_faucet=True):
    # load webpage 
    driver.implicitly_wait(2)
    driver.get("https://cointiply.com/login")
    driver.maximize_window()

    #Login
    try:
        # enter email
        driver.find_element_by_xpath("//html/body/div/div[2]/section/div[1]/div/div[2]/div/div[3]/form/div[1]/input").send_keys(getUsername(directory, 'Cointiply'))
        # enter password
        driver.find_element_by_xpath("/html/body/div/div[2]/section/div[1]/div/div[2]/div/div[3]/form/div[2]/input").send_keys(getPassword(directory, 'Cointiply'))
        showMessage("CAPTCHA", 'Verify captcha, then click OK')
        #click LOGIN
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/section/div[1]/div/div[2]/div/div[3]/form/div[5]/button").click()
    except NoSuchElementException:
        exception = "already logged in"

    # move window to primary monitor
    Cointiply = pygetwindow.getWindowsWithTitle('Cointiply Bitcoin Rewards - Earn Free Bitcoin - Google Chrome')[0]
    Cointiply.moveTo(10, 10)
    Cointiply.resizeTo(100, 100)
    Cointiply.maximize()
    
    if run_faucet:
        # Roll faucet
        driver.get("https://cointiply.com/home?intent=faucet")
        time.sleep(2)
        # click Roll & Win
        try:
            driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div/button").click()
            showMessage("CAPTCHA", 'Verify captcha, then click OK')
            # click Submit Captcha & Roll
            driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div/button").click()
            time.sleep(2)
        except NoSuchElementException:
            exception = "gotta wait"
    # capture time when faucet is completed (used for Hourly Script)
    faucet_complete = datetime.now().time()

    # PTC Ads
    driver.get("https://cointiply.com/ptc")
    time.sleep(1)

    view_length = ""
    selection = ""
    # driver.implicitly_wait(1)
    main_window = driver.window_handles[0]
    still_ads = True
    while still_ads:
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
            driver.close()
        driver.switch_to.window(main_window)
        # make sure there are coins to be earned
        avail_coins = driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[1]/div[2]").text
        if int(avail_coins[0]) > 0:
            try:
                # click to enable Rain Pool button
                driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[1]/div[4]/div[2]/div/div[2]/span[3]").click()
                time.sleep(1)
                # "Click to qualify for rain pool
                driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[1]/div[4]/div[2]/div/div[2]/div/label[2]").click()
                time.sleep(1)
                # click I UNDERSTAND
                try:
                    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/button[2]").click()
                except NoSuchElementException:
                    driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[3]/button[2]").click()
            except (ElementNotInteractableException, ElementClickInterceptedException):
                exception = "already registered"
            time.sleep(1)
            # click on view highest paying add link
            driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[1]/div[3]/button").click()
            # Obtain how long ad needs to be viewed for
            driver.switch_to.window(main_window)
            try:
                # Capture "X seconds remaining" element text
                view_length = driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/span").text
            except (NoSuchElementException, StaleElementReferenceException):
                continue

            ## register ad viewing
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            # time.sleep(1)
            driver.switch_to.window(main_window)
            current_pos = pyautogui.position()
            # click on screen, move back to current_pos
            pyautogui.leftClick(1150, 250)
            pyautogui.moveTo(current_pos)
            driver.switch_to.window(window_after)
            try:
                view_length = int(view_length[0] + view_length[1]) + 3
                time.sleep(view_length)
            except ValueError:
                print('error')
                driver.close()
                continue

            driver.switch_to.window(main_window)
            time.sleep(1)

            # obtain which image needs to be selected
            try:
                selection = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/span[1]").text.replace("Select: ", "")
            except NoSuchElementException:
                try:
                    # skip ad
                    print('skipped ad')
                    driver.find_element_by_id("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/button").click()
                    continue
                except NoSuchElementException:
                    continue
            time.sleep(1)
            # take screenshot of captcha images
            myScreenshot = pyautogui.screenshot(region=(650, 400, 600, 400))
            myScreenshot.save(directory + r"\Projects\Coding\Python\MRAutomation\Resources\captcha images\captcha_shot.png")
            template = ''
            template = cv2.imread(directory + r"\Projects\Coding\Python\MRAutomation\Resources\captcha images" + '\\' + selection + '.png')
            if not isinstance(template,np.ndarray):
                showMessage("check captcha", f'selection: {selection}  not available')
                continue
            
            img = cv2.imread(directory + r"\Projects\Coding\Python\MRAutomation\Resources\captcha images\captcha_shot.png")
            img2 = img.copy()
            w, h = template.shape[:-1]
            methods = ['cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']
            x_coord = 0
            for i in methods:
                img = img2.copy()
                method = eval(i)
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                top_left = min_loc if method in [cv2.TM_SQDIFF_NORMED] else max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv2.rectangle(img, top_left, bottom_right, 255, 2)
            # removes the code to draw rectangle (keeping for troubleshooting reference)
                # plt.subplot(121), plt.imshow(res, cmap='gray')
                # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                # plt.subplot(122), plt.imshow(img, cmap='gray')
                # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                # plt.suptitle(i)
                x_coord = x_coord + int(top_left[0])
                # plt.show()
            x_coord_avg = x_coord / 2
            # time.sleep(1)
            img_num = 0
            if x_coord_avg < 107:
                img_num = 1
            elif 107 <= x_coord_avg <= 200:
                img_num = 2
            elif 200 <= x_coord_avg <= 300:
                img_num = 3
            elif 300 <= x_coord_avg <= 400:
                img_num = 4
            elif x_coord_avg > 400:
                img_num = 5
            driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/img[" + str(img_num) + "]").click()
            # time.sleep(1)
        else:
            still_ads = False

    # # # PROMO - Candy Chaos
    # # # navigate to address
    # driver.get("https://cointiply.com/itemPromos?utm_source=desktop")
    # time.sleep(1)
    # # get number of spins
    # spins_remaining = driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div[1]/div[2]/div[1]").text
    # while (int(spins_remaining) > 0):
    #     try:
    #         # click spin
    #         driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div[3]/div[3]").click()
    #         # wait 5 seconds
    #         time.sleep(5)
    #         spins_remaining = driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div[1]/div[2]/div[1]").text.replace("\n", " ").strip(" Spins Remaining")
    #     except NoSuchElementException:
    #         exception = "pop-up"
    return faucet_complete