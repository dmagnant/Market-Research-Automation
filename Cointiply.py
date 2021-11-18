from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException
import time
import ctypes
import cv2
import pyautogui
import pygetwindow
import win32gui
from Functions import getKeePassUsername, getKeePassPassword, enumHandler

def runCointiply(directory, driver):
    # load webpage 
    driver.implicitly_wait(1)
    driver.get("https://cointiply.com/login")
    driver.maximize_window()

    #Login
    try:
        # enter email
        driver.find_element_by_xpath("//html/body/div/div[2]/section/div[1]/div/div[2]/div/div[3]/form/div[1]/input").send_keys(getKeePassUsername(directory, 'Cointiply'))
        # enter password
        driver.find_element_by_xpath("/html/body/div/div[2]/section/div[1]/div/div[2]/div/div[3]/form/div[2]/input").send_keys(getKeePassPassword(directory, 'Cointiply'))
        # handle captcha
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, "Verify captcha, then click OK", 'CAPTCHA', 0)
        #click LOGIN
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/section/div[1]/div/div[2]/div/div[3]/form/div[5]/button").click()
    except NoSuchElementException:
        exception = "already logged in"

    # move window to primary monitor
    Cointiply = pygetwindow.getWindowsWithTitle('Cointiply Bitcoin Rewards - Earn Free Bitcoin - Google Chrome')[0]
    Cointiply.resizeTo(100, 100)
    win32gui.EnumWindows(enumHandler, 'Cointiply')
    Cointiply.maximize()

    # Roll faucet
    driver.get("https://cointiply.com/home?intent=faucet")
    time.sleep(2)
    # click Roll & Win
    try:
        driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div/button").click()
        # handle captcha
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, "Verify captcha, then click OK", 'CAPTCHA', 0)
        # click Submit Captcha & Roll
        driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div/button").click()
        time.sleep(1)
    except NoSuchElementException:
        exception = "gotta wait"

    # PTC Ads
    driver.get("https://cointiply.com/ptc")
    time.sleep(1)

    view_length = ""
    selection = ""
    # driver.implicitly_wait(1)
    main_window = driver.window_handles[0]

    still_ads = True
    while still_ads:
        driver.switch_to.window(main_window)
        # make sure there are coins to be earned
        avail_coins = driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[1]/div[2]").text
        num_avail_coins = int(avail_coins[0])
        if num_avail_coins > 0:
            time.sleep(1)
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
            except ElementNotInteractableException:
                exception = "already registered"
            except ElementClickInterceptedException:
                exception = "already registered"
            # click on view highest paying add link
            driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[1]/div[3]/button").click()
            # Obtain how long ad needs to be viewed for
            driver.switch_to.window(main_window)
            try:
                # Capture "X seconds remaining" element text
                view_length = driver.find_element_by_xpath("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/span").text
            except NoSuchElementException:
                exception = "already viewed"
                driver.switch_to.window(window_after)
                driver.close()
                continue
            except StaleElementReferenceException:
                exception = "already viewed"
                driver.switch_to.window(window_after)
                driver.close()
                continue

            ## register ad viewing
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            time.sleep(1)
            driver.switch_to.window(main_window)
            # click on screen
            pyautogui.leftClick(1150, 250)
            time.sleep(1)
            driver.switch_to.window(window_after)
            view_length = view_length[0] + view_length[1]
            if view_length == "Oo":
                driver.switch_to.window(window_after)
                driver.close()
                continue
            view_length = int(view_length) + 3
            time.sleep(float(view_length))
            driver.switch_to.window(main_window)
            time.sleep(1)
            ##

            # obtain which image needs to be selected
            try:
                selection = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/span[1]").text.replace("Select: ", "")
            except NoSuchElementException:
                try:
                    # skip ad
                    driver.find_element_by_id("//*[@id='app']/div[4]/div/div/div[2]/div[1]/div/div[2]/div/div/div[2]/button").click()
                    continue
                except NoSuchElementException:
                    continue

            time.sleep(1)
            # take screenshot of captcha images
            myScreenshot = pyautogui.screenshot(region=(650, 400, 600, 400))
            myScreenshot.save(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\captcha_shot.png")
            
            # select proper template based on selection
            if selection == "Anchovies":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\anchovies.png")
            elif selection == "Apple":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\apple.png")
            elif selection == "Beaker":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\beaker.png")
            elif selection == "Bolts of Cloth":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\bolts of cloth.png")
            elif selection == "Bones":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\bones.png")
            elif selection == "Bucket":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\bucket.png")
            elif selection == "Carrot":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\carrot.png")
            elif selection == "Cheese":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\cheese.png")
            elif selection == "Chocolate":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\chocolate.png")
            elif selection == "First Aid Kit":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\first aid kit.png")
            elif selection == "Fish":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\fish.png")
            elif selection == "Jerry Can":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\jerry can.png")
            elif selection == "Keys":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\keys.png")
            elif selection == "Lock Box":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\lock box.png")
            elif selection == "Medecine":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\medicine.png")
            elif selection == "Mushroom":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\mushroom.png")
            elif selection == "Ointment":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\ointment.png")
            elif selection == "Paint":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\paint.png")
            elif selection == "Peanut":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\peanut.png")
            elif selection == "Pen":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\pen.png")
            elif selection == "Pencil":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\pencil.png")
            elif selection == "Pills":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\pills.png")
            elif selection == "Sack":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\sack.png")
            elif selection == "Small Lollipop":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\small lollipop.png")
            elif selection == "Steak":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\steak.png")
            elif selection == "Syringe":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\syringe.png")
            elif selection == "Tire":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\tire.png")
            elif selection == "Turkey Leg":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\turkey leg.png")
            elif selection == "Wallet":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\wallet.png")
            elif selection == "Wooden Logs":
                template = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\wooden logs.png")
            else:
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, f'selection not available \n'
                        , "check captcha", 0)
                driver.switch_to.window(window_after)
                driver.close()
                continue

            img = cv2.imread(directory + r"\Projects\Coding\Python\Market Research\Resources\captcha images\captcha_shot.png")
            img2 = img.copy()
            w, h = template.shape[:-1]
            # Condensed methods from 6 to 2
            methods = ['cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']
            x_coord = 0
            for meth in methods:
                img = img2.copy()
                method = eval(meth)
                # Apply template Matching
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
                if method in [cv2.TM_SQDIFF_NORMED]:
                    top_left = min_loc
                else:
                    top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv2.rectangle(img, top_left, bottom_right, 255, 2)
                # removes the code to draw rectangle (keeping for troubleshooting reference)
                #plt.subplot(121), plt.imshow(res, cmap='gray')
                #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                #plt.subplot(122), plt.imshow(img, cmap='gray')
                #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                #plt.suptitle(meth)
                x_coord = x_coord + int(top_left[0])
                #plt.show()
            x_coord_avg = x_coord / 2
            time.sleep(1)
            if x_coord_avg < 107:
                driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/img[1]").click()
            elif 107 <= x_coord_avg <= 200:
                driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/img[2]").click()
            elif 200 <= x_coord_avg <= 300:
                driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/img[3]").click()
            elif 300 <= x_coord_avg <= 400:
                driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/img[4]").click()
            elif x_coord_avg > 400:
                driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[1]/img[5]").click()
            else:
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, f'X Coordinate: {x_coord_avg} \n'
                                f'not meeting criteria'
                        , "check captcha", 0)
            driver.switch_to.window(window_after)
            driver.close()
            driver.switch_to.window(main_window)
        else:
            still_ads = False

    # PROMO - November Monster Mania
    # navigate to address
    driver.get("https://cointiply.com/itemPromos?utm_source=desktop")
    # get number of spins
    spins_remaining = driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div/div[2]/div[4]").text.replace("\n", " ").replace(" Spins Remaining", '')

    while (spins_remaining.isnumeric()):
        try:
            # click spin
            driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div/div[2]/div[6]").click()
            # wait 5 seconds
            time.sleep(4)
            # check if spins remain
            spins_remaining = driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div/div[2]/div[4]").text.replace("\n", " ").replace(" Spins Remaining", '')
        except NoSuchElementException:
            exception = "pop-up"