import sys
import os
from time import sleep
from selenium.webdriver.remote.command import Command
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



# DEBUG: Creates a Chrome session
def getArgv():
    if len(sys.argv) < 6:
        print("Usage: python ./" + sys.argv[0] + " spare2@ccc o31453 wifiname wifipass adsl")
        exit(0)

def getBrowser():
    try:
        return webdriver.Chrome()
    except Exception as e:
        print("Could not create a Chrome session.")

# DEBUG: Opens the url for the router
def setSite(browser):
    try:
        browser.get("https://emulator.tp-link.com/W9970V2_Emulator/index.htm")
        #browser.get("http://192.168.1.1")
    except Exception as e:
        print("Could not resolve http://192.168.1: " + e)
        return setSite(browser)
    # TODO:
def getActionChain(browser):
    return ActionChains(browser)

def waitUntilVisibleID(browser, id):
    return WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.ID, id)))

def waitUntilVisibleValue(browser, value):
    return WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.VALUE, value)))

# NOTE: Go to Quick Setup
def login(browser):

    login = browser.find_element_by_xpath('//div/div/div/ul/li/input[@id="userName"]')
    password = browser.find_element_by_xpath('//div/div/div/ul/li/input[@id="pcPassword"]')
    loginBtn = browser.find_element_by_xpath('//div/div/div/button[@id="loginBtn"]')

    getActionChain(browser).move_to_element(login).send_keys("admin").click(password).send_keys("Cadmin").click(loginBtn).perform()
    waitUntilVisibleID(browser, 'menu_qs').click()
    waitUntilVisibleID(browser, 't_note2')
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()


def setRegion(browser):

    waitUntilVisibleID(browser, 'region')

    region = browser.find_element_by_xpath('//div/div/p/select[@name="region"]')
    timezone = browser.find_element_by_xpath('//div/div/p/select[@name="timezone"]')

    for option in region.find_elements_by_tag_name('option'):
        if option.text == 'Israel':
            option.click() # select() in earlier versions of webdriver
            break
    for option in timezone.find_elements_by_tag_name('option'):
        if option.text == '(GMT+02:00) Cairo, Athens, Istanbul, Minsk, Jerusalem, Kiev, Chisinau':
            option.click() # select() in earlier versions of webdriver
            break

    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def setDSL(browser):
    waitUntilVisibleID(browser, "vid_en")
    isp = browser.find_element_by_xpath('//div/div/p/select[@name="isp"]')
    if (sys.argv[5] == "vdsl"):
        for option in isp.find_elements_by_tag_name('option'):
            if option.text == 'VDSL_Triple C':
                option.click()
                break
            elif option.text == 'Other':
                option.click()
                break
        browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()
    else:
        for option in isp.find_elements_by_tag_name('option'):
            if option.text == 'ADSL_Triple C':
                option.click()
                break
            elif option.text == 'Other':
                option.click()
                l2type = browser.find_element_by_xpath('//div/div/p/select[@id="intf_type"]')
                for option in l2type.find_elements_by_tag_name('option'):
                    if option.text == 'ADSL':
                        option.click()
                        break
                vpi = browser.find_element_by_xpath('//div/div/p/input[@id="vpi_isp"]')
                vci = browser.find_element_by_xpath('//div/div/p/input[@id="vci_isp"]')
                vci.clear()
                vpi.clear()

                vci.send_keys("8")
                vpi.send_keys("48")

                break
        browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def setPPPoE(browser):
    waitUntilVisibleID(browser, 'usr')
    usr = browser.find_element_by_xpath('//div/div/p/input[@id="usr"]')
    pwd = browser.find_element_by_xpath('//div/div/p/input[@id="pwd"]')
    cfm = browser.find_element_by_xpath('//div/div/p/input[@id="cfm"]')

    usr.clear()
    pwd.clear()
    cfm.clear()

    getActionChain(browser).click(usr).send_keys(sys.argv[1]).click(pwd).send_keys(sys.argv[2]).click(cfm).send_keys(sys.argv[2]).perform()
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def set3G4G(browser):
    waitUntilVisibleID(browser, "usb3g_backup_en")
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def setAutoDetect(browser):
    waitUntilVisibleID(browser, "en_auto")
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def setWifi(browser):
    waitUntilVisibleID(browser, 'ssid')
    ssid = browser.find_element_by_xpath('//div/div/p/input[@id="ssid"]')
    pwd = browser.find_element_by_xpath('//div/div/p/input[@id="pwd"]')

    ssid.clear()
    pwd.clear()

    getActionChain(browser).click(ssid).send_keys(sys.argv[3]).click(pwd).send_keys(sys.argv[4]).perform()
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def confirmFinish(browser):
    waitUntilVisibleID(browser, "wlpwd")
    browser.find_element_by_xpath('//div/p/input[@value="Save"]').click()
    waitUntilVisibleID(browser, "doEnd")
    browser.find_element_by_xpath('//div/p/input[@value="Finish"]').click()

def quickSetup(browser):
    waitUntilVisibleID(browser, 'menu_qs').click()
    waitUntilVisibleID(browser, 'et')
    sleep(2)
    browser.find_element_by_xpath('//div/p/input[@value="Next"]').click()

def tplink9970():
    setSite(browser)
    # DEBUG:
    quickSetup(browser)
    # DEBUG:
    #login(browser)
    setRegion(browser)
    setAutoDetect(browser)
    setDSL(browser)
    setPPPoE(browser)
    set3G4G(browser)
    setWifi(browser)
    confirmFinish(browser)

getArgv()
browser = getBrowser()
tplink9970()

# DEBUG: Quick Setup - Region and Time Zone

# DEBUG: Quick Setup - Auto Detection

# DEBUG: Quick Setup - DSL

# DEBUG: Quick Setup - PPPoE

# DEBUG: Quick Setup - Wireless

# DEBUG: Quick Setup - Confirm

# DEBUG: Quick Setup - Complete
