##############################################################################################
# ADCBaseClass.py
#
# Description: Add S2 DSK to ADC backend for Smart Start T3000 thermostat
#
# Usage: Using Chrome as the browser run this script using Python 3.10. Also verified this works
# on Edge, just change the webdriver to point at Edge, Should also work on Firfox but not verified.
#
# Nortek Control, 2022, Kris Juarez
#############################################################################################
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

######################################################################################################################
#
#         This file contains the unit tests for adding a S2 Smart Start Device to the backend
#         Verified that this works correctly using the T300 ADC Thermostat on Edge Panel.
#
######################################################################################################################


account = {
    "user_login_id": "kristoffer.juarez",
    "user_pass": "Inadaze123!@#",
    "panel_id": "13196217",
    "thermostat_device_name": "T3000",
    "thermostat_DSK": ["09134", "08770", "57129", "33165", "04152", "33972", "09108", "15612"],
}

#Add a S2 smart start device
class AlarmAdminAddS2():

#Open ADC Alarm Admin Page
    def logintoadc(self):
        baseUrl = "https://alarmadmin.alarm.com"
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        #driver = webdriver.Edge(EdgeChromiumDriverManager().install())

        driver.maximize_window()
        driver.get(baseUrl)
        driver.implicitly_wait(10)

#Load and read JSON info
        userlogin = account["user_login_id"]
        userpass = account["user_pass"]
        panelID = account["panel_id"]
        devicename = account["thermostat_device_name"]
        dsk = []
        dsk.extend(account["thermostat_DSK"])
        s2keycnt = 8


#Search for the login input field element
        ul = driver.find_element(By.ID, "txtUsername")
        ul.send_keys(userlogin)

#Search for the password input field element
        up = driver.find_element(By.ID, "txtPassword")
        up.send_keys(userpass)

#Click the login button
        login = driver.find_element(By.ID, "butLogin").click()
        time.sleep(10)

#Click the tab "Customers
        driver.find_element(By.XPATH, "//span[contains(@class,'tabTitle') and contains(text(),'Customers')]")


#Click Search Customer/Device
        driver.find_element(By.XPATH, "//a[@href='/Support/FindCustomer.aspx']").click()

#Scroll and then click on the customer ID and then click "Search"
        cusID = driver.find_element(By.ID, "ctl00_responsiveBody_txtCustomerId")
        cusID.send_keys(panelID)
        login = driver.find_element(By.ID, "ctl00_responsiveBody_btnSearch").click()


#Scroll and find the customer link at the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element(By.XPATH, "//tr[@class='dataRow']//a[contains(text(),'')]").click()


#Find equipment link on the customer page
        driver.find_element(By.XPATH, "//a[@title='See equipment list for a customer']").click()

#Find and click on the zwave tab
        driver.find_element(By.XPATH, "//a[@title='See emPower devices for a customer']").click()


#find manage S2 and Smart Start Keys
        driver.find_element(By.XPATH, "//a[@id='ctl00_phBody_UcsZWaveDevices_btnManageDeviceKeys']").click()

#Use a if/then block to see if there are not any keys loaded on the page
        if driver.find_element(By.XPATH, "//*[text()='No device security keys found.']"):
            print("Pagesource found!!")
            # Choose Add key
            driver.find_element(By.XPATH, "//div[@id='content_container']" and
                                "//input[@name='ctl00$phBody$btnAddKey']").click()
            #Choose Enter Manually button and click it
            driver.find_element(By.XPATH, "//form[@id='aspnetForm']" and
                                "//input[@name='ctl00$phBody$ucsScanDsk$btnEnterManually']").click()
            # Enter the Device Name from the json file and enter the 15 digit  id for the Device
            driver.find_element(By.XPATH, "//form[@id='aspnetForm']" and
                                "//input[@name='ctl00$phBody$ucsDsk$txtDeviceName']").send_keys(str(devicename))

            #Send device keys
            count = 0
            for itr in dsk:
                temp = count
                driver.find_element(By.XPATH, "//*[contains(@name,'ctl00$phBody$ucsDsk$txtDskWord%s')]"%str(temp)).send_keys(itr)
                count += 1

            #add device button
            driver.find_element(By.XPATH, "//form[@id='aspnetForm']" and "//input[@name='ctl00$phBody$ucsDsk$btnSave']").click()
            time.sleep(3)

        #Should be an else here to deactivate a key if the key has already been added in. Could be expanded to remove device first.
        driver.quit()

S2 = AlarmAdminAddS2()
S2.logintoadc()

