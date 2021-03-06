import ctypes
import os
import time
from datetime import datetime

import piecash
import psutil
import pyautogui
import pygetwindow
from piecash import GnucashException
from pykeepass import PyKeePass
from selenium import webdriver
from selenium.common.exceptions import (ElementNotInteractableException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def showMessage(header, body): 
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, body, header, 0)

def checkIfProcessRunning(processName):
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def startExpressVPN():
    os.startfile(r'C:\Program Files (x86)\ExpressVPN\expressvpn-ui\ExpressVPN.exe')
    time.sleep(5)
    EVPN = pygetwindow.getWindowsWithTitle('ExpressVPN')[0]
    EVPN.close()  # stays open in system tray

def closeExpressVPN():
    if checkIfProcessRunning('ExpressVPN.exe'):
        os.startfile(r'C:\Program Files (x86)\ExpressVPN\expressvpn-ui\ExpressVPN.exe')
        time.sleep(3)
        EVPN = pygetwindow.getWindowsWithTitle('ExpressVPN')[0]
        EVPN.restore()
        EVPN.move(0, 0)
        EVPN.activate()
        pyautogui.leftClick(40, 50)
        time.sleep(1)
        pyautogui.leftClick(40, 280)
        time.sleep(4)

def setDirectory():
    return os.environ.get('StorageDirectory')

def chromeDriverAsUser(directory=setDirectory()): # Beta version to obtain v104 (bug exists with <104). Once 104 is standard version, edit/remove beta lines
    chromedriver = Service(directory + r"\Projects\Coding\webdrivers\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=C:\Users\dmagn\AppData\Local\Google\Chrome Beta\User Data") # remove beta here
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    options.binary_location = "C:/Program Files/Google/Chrome Beta/Application/chrome.exe" # remove this line to revert from "Beta" version
    return webdriver.Chrome(service=chromedriver, options=options)

def chromeDriverBlank(directory):
    chromedriver = directory + r"\Projects\Coding\webdrivers\chromedriver.exe"
    return webdriver.Chrome(executable_path=chromedriver)

def braveBrowserAsUser(directory):
    bravedriver = directory + r"\Projects\Coding\webdrivers\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=C:\Users\dmagn\AppData\Local\BraveSoftware\Brave-Browser\User Data1")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.binary_location = "C:\Program Files\BraveSoftware\Brave-Browser\Application\chrome.exe"
    return webdriver.Chrome(executable_path=bravedriver, options=options)

def getUsername(directory, name):
    keepass_file = directory + r"\Other\KeePass.kdbx"
    KeePass = PyKeePass(keepass_file, password=os.environ.get('KeePass'))
    return KeePass.find_entries(title=name, first=True).username

def getPassword(directory, name):
    keepass_file = directory + r"\Other\KeePass.kdbx"
    KeePass = PyKeePass(keepass_file, password=os.environ.get('KeePass'))
    return KeePass.find_entries(title=name, first=True).password

def loginPiHole(directory, driver):
    driver.implicitly_wait(2)
    driver.get("http://192.168.1.144/admin/")
    driver.maximize_window()
    try:
        #click Login
        driver.find_element(By.XPATH, "/html/body/div[2]/aside/section/ul/li[3]/a").click()
        # Enter Password
        driver.find_element(By.ID, "loginpw").send_keys(getPassword(directory, 'Pi hole'))
        #click Login again
        driver.find_element(By.XPATH, "//*[@id='loginform']/div[2]/div/button").click()
        time.sleep(1)
    except NoSuchElementException:
        exception = "already logged in"

def disablePiHole(directory, driver):
    driver.maximize_window()
    pihole_window = driver.window_handles[0]
    driver.switch_to.window(pihole_window)
    loginPiHole(directory, driver)
    try:
        driver.find_element(By.XPATH, "//*[@id='pihole-disable']/a/span[2]").click()
        # Click Indefinitely
        driver.find_element(By.XPATH, "//*[@id='pihole-disable-indefinitely']").click()
    except ElementNotInteractableException:
        exception = "already disabled"

def enablePiHole(directory, driver):
    pihole_window = driver.window_handles[0]
    driver.switch_to.window(pihole_window)
    loginPiHole(directory, driver)
    try:
        driver.find_element(By.ID, "enableLabel").click()
    except NoSuchElementException:
        exception = "already enabled"
    except ElementNotInteractableException:
        exception = "already enabled"

def openGnuCashBook(directory, type, readOnly, openIfLocked):
    if type == 'Finance':
        book = directory + r"\Finances\Personal Finances\Finance.gnucash"
    elif type == 'Home':
        book = directory + r"\Stuff\Home\Finances\Home.gnucash"
    try:
        mybook = piecash.open_book(book, readonly=readOnly, open_if_lock=openIfLocked)
    except GnucashException:
        showMessage("Gnucash file open", 'Close Gnucash file then click OK \n')
        mybook = piecash.open_book(book, readonly=readOnly, open_if_lock=openIfLocked)
    return mybook

def timeOfNextRun(minsLeftForFaucet):
    now = datetime.now().time().replace(second=0, microsecond=0)
    if now.hour == 23:
        nextRunMinute = 0
        nextRunHour = 0
    else:
        nextRunMinute = now.minute + minsLeftForFaucet
        nextRunHour = now.hour
        # adjust for minutes going over 60
        if (nextRunMinute > 60):
            nextRunMinute = abs(nextRunMinute - 60)
            nextRunHour += 1 if nextRunHour < 23 else 0
    if nextRunMinute < 0 or nextRunMinute > 59:
        showMessage('Next Run Minute is off', 'Nextrunminute = ' + str(nextRunMinute))
    nextRun = now.replace(hour=nextRunHour, minute=nextRunMinute)
    print('next run at ', str(nextRun.hour) + ":" + "{:02d}".format(nextRun.minute))
    return nextRun
