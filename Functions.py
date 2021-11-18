from selenium import webdriver
import socket
from pykeepass import PyKeePass
import os
import win32gui
import psutil
import time
import pygetwindow
import pyautogui

def enumHandler(hwnd, title):
    if win32gui.IsWindowVisible(hwnd):
        if title in win32gui.GetWindowText(hwnd):
            win32gui.MoveWindow(hwnd, 0, 0, 100, 100, True)

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

def closeExpressVPN():
    if checkIfProcessRunning('ExpressVPN.exe'):
        os.startfile(r'C:\Program Files (x86)\ExpressVPN\expressvpn-ui\ExpressVPN.exe')
        time.sleep(1)
        EVPN = pygetwindow.getWindowsWithTitle('ExpressVPN')[0]
        EVPN.restore()
        EVPN.move(0, 0)
        EVPN.activate()
        pyautogui.leftClick(40, 50)
        time.sleep(1)
        pyautogui.leftClick(40, 280)
        time.sleep(1)

def setDirectory():
    #get computer name
    computer = socket.gethostname()
    # computer-specific file paths
    if computer == "Big-Bertha":
        return r"C:\Users\dmagn\Google Drive"
    elif computer == "Black-Betty":
        return r"D:\Google Drive"

def chromeDriverAsUser(directory):
    chromedriver = directory + r"\Projects\Coding\webdrivers\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir=C:\Users\dmagn\AppData\Local\Google\Chrome\User Data")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return webdriver.Chrome(executable_path=chromedriver, options=options)

def chromeDriverBlank(directory):
    chromedriver = directory + r"\Projects\Coding\webdrivers\chromedriver.exe"
    return webdriver.Chrome(executable_path=chromedriver)

def getKeePassUsername(directory, name):
    keepass_file = directory + r"\Other\KeePass.kdbx"
    KeePass = PyKeePass(keepass_file, password=os.environ.get('KeePass'))
    return KeePass.find_entries(title=name, first=True).username

def getKeePassPassword(directory, name):
    keepass_file = directory + r"\Other\KeePass.kdbx"
    KeePass = PyKeePass(keepass_file, password=os.environ.get('KeePass'))
    return KeePass.find_entries(title=name, first=True).password