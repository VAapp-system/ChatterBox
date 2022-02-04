# Actions on Google Simulator Reset Tool
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

driver.get('https://console.actions.google.com/u/0/')
driver.find_element(By.XPATH, '//*[@id="Email"]').send_keys('your_gmail' + Keys.ENTER)
time.sleep(2)
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('your_gmail_password' + Keys.ENTER)
time.sleep(5)
driver.set_window_size(2000,1000)
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' your_project_name ')]")))
driver.find_element(By.XPATH, "//*[contains(text(), ' your_project_name ')]").click()
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/a7t-topnav/div/div[4]/div[2]')))
driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/a7t-topnav/div/div[4]/div[2]').click()
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/a7t-interactive-sidenav/div/div[1]/a7t-interactive-sidenav-group[4]/button/div[1]/span')))
driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/a7t-interactive-sidenav/div/div[1]/a7t-interactive-sidenav-group[4]/button/div[1]/span').click()
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/a7t-featurebar/div/div/div[2]/div[1]/button')))
driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/a7t-featurebar/div/div/div[2]/div[1]/button').click()
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[2]/div/div[2]/div/fb-chip/div')))

driver.quit()