from selenium import webdriver
import os
from selenium.webdriver.common.by import By
import time

ADDRESS = "https://api.vk.com/method/"
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "/usr/local/bin/chromedriver")
driver = webdriver.Chrome(executable_path=DRIVER_BIN)
HOST = "http://10.10.3.54:8082/NH-KISA-OTA/ota/pig.jsp"

#Tram
#FinAcno
#balance
def balance(pin):
    driver.get(HOST)
    driver.find_element_by_name("FinAcno").send_keys(pin)
    get_balance=driver.find_element_by_xpath("//input[@value='조회']")
    get_balance.click()
    time.sleep(1)
    balance_ret = driver.find_element_by_id("balance").get_attribute('value')
    return balance_ret


def pay(pin, amount):
    driver.get(HOST)
    
    #add pin account to 
    driver.find_element_by_name("FinAcno").send_keys(pin)
    
    #amount to use from account
    tram = driver.find_element_by_id("Tram")
    tram.clear()
    tram.send_keys(amount)
    
    get_balance=driver.find_element_by_xpath("//input[@value='조회']")
    time.sleep(3)
    get_balance.click()

    get_balance=driver.find_element_by_xpath("//input[@value='결제']")
    time.sleep(3)
    get_balance.click()
    print("Success")


