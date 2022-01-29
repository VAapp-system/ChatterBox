import sys
import time
import http
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import traceback

args = sys.argv
locale = args[1]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

if locale == 'EN':
    path1 = './article_list_en.txt'
    path2 = './appurl_en.txt'
    driver.get('https://assistant.google.com/explore?hl=en')
elif locale == 'JA':
    path1 = './article_list_ja.txt'
    path2 = './appurl_ja.txt'
    driver.get('https://assistant.google.com/explore?hl=ja_jp')

with open(path1, 'r', encoding='utf-8') as f1:
    words = f1.readlines()

for word in words:
    if locale == 'EN':
        driver.get('https://assistant.google.com/explore/search?q=' + word.strip() + '&hl=en')
    elif locale == 'JA':
        driver.get('https://assistant.google.com/explore/search?q=' + word.strip() + '&hl=ja_jp')
    try:
        app_elements = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/span/div/div/c-wiz/div/div/div/div/div/div/a')
        if len(app_elements) == 0:
            continue

        n1 = len(app_elements) - 1
        actions = ActionChains(driver)
        actions.move_to_element(app_elements[n1])
        actions.perform()
        time.sleep(3)
        app_elements = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/span/div/div/c-wiz/div/div/div/div/div/div/a')
        n2 = len(app_elements) - 1

        while n2 > n1:
            actions = ActionChains(driver)
            actions.move_to_element(app_elements[n2])
            actions.perform()
            time.sleep(3)
            app_elements = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/span/div/div/c-wiz/div/div/div/div/div/div/a')
            n1 = n2
            n2 = len(app_elements) - 1
        for app in app_elements:
            app_url = app.get_attribute("href")
            apps.append(app_url)
        
        apps = list(dict.fromkeys(apps))
    except:
        pass

with open(path2, 'w', encoding='utf-8') as f2:
    f2.write('\n'.join(apps))

try:
    driver.quit()
except http.client.RemoteDisconnected:
    pass