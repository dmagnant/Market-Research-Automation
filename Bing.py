from selenium.common.exceptions import NoSuchElementException
import time
import os
from Functions import getKeePassUsername, getKeePassPassword

def runBing(directory, driver):
    driver.execute_script("window.open('https://account.microsoft.com/rewards/');")
    bing_window = driver.window_handles[1]
    driver.switch_to.window(bing_window)
    # click Sign in
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/main/section/div[1]/div[2]/section/div[1]/a[2]").click()
    # login
    try:
        # enter username
        driver.find_element_by_id("i0116").send_keys(getKeePassUsername(directory, 'Bing Rewards'))
        time.sleep(1)
        # click Next
        driver.find_element_by_id("idSIButton9").click()
        time.sleep(1)
        # enter password
        driver.find_element_by_id("i0118").send_keys(getKeePassPassword(directory, 'Bing Rewards'))
        time.sleep(1)
        # click Sign in
        driver.find_element_by_xpath("/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div/div/input").click()
        time.sleep(1)
        # click to stay signed in
        driver.find_element_by_xpath("/html/body/div/form/div/div/div[2]/div[1]/div/div/div/div/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div/div[2]/input").click()
        # click sign in link
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/main/section/div[1]/div[2]/section/div[1]/a[2]").click()
    except NoSuchElementException:
        exception = "already logged in"
    # click on "points" links
    links = driver.find_elements_by_partial_link_text("points")
    links[0].click()
    time.sleep(1)
    window_after = driver.window_handles[2]
    driver.switch_to.window(window_after)
    driver.close()
    driver.switch_to.window(bing_window)
    # capture balance
    time.sleep(3)
    mr_balance = driver.find_element_by_xpath("//*[@id='userBanner']/mee-banner/div/div/div/div[2]/div[1]/mee-banner-slot-2/mee-rewards-user-status-item/mee-rewards-user-status-balance/div/div/div/div/div/p[1]/mee-rewards-counter-animation/span").text.replace(",", "")
    if int(mr_balance) >= 5250:
        # go to $5 Amazon gift card link
        driver.get("https://rewards.microsoft.com/redeem/000800000000")
        time.sleep(3)
        # click Redeem Reward
        driver.find_element_by_xpath("//*[@id='redeem-pdp_000800000000']/span[1]").click()
        # click Confirm Reward
        driver.find_element_by_xpath("//*[@id='redeem-checkout-review-confirm']/span[1]").click()
        try:
            # enter Phone number
            driver.find_element_by_id("redeem-checkout-challenge-fullnumber").send_keys(os.environ.get('Phone'))
            # click Send
            driver.find_element_by_xpath("//*[@id='redeem-checkout-challenge-validate']/span").click()
        except NoSuchElementException:
            exception = "caught"