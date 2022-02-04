# Google Sign-In Reset Tool
import chromedriver_binary
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--mute-audio')
driver = webdriver.Chrome(options=options)

driver.get('https://console.actions.google.com/')
driver.find_element(By.XPATH, '//*[@id="Email"]').send_keys('your_gmail' + Keys.ENTER)
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('your_password' + Keys.ENTER)

time.sleep(2)

driver.get("https://myaccount.google.com/permissions?continue=https%3A%2F%2Fmyaccount.google.com%2Fsecurity")
login_list = driver.find_elements(By.CLASS_NAME, 'ulZjrf')
n = len(login_list) - 1
print(n)
for i in range(n):
    login = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/c-wiz/div/div[2]/div[1]/div[2]/div[3]')
    login.click()
    button = login.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/c-wiz/div/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/div[2]/div[2]/div')
    button.click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/div/div/div[2]/div[3]/div[2]/span/span')))
    driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div/div/div[2]/div[3]/div[2]/span/span').click()
    print('OK')
    time.sleep(3)

driver.quit()
