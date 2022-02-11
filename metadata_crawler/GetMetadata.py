import os
import sys
import json
import http
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

args = sys.argv
locale = args[1]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

if locale == 'EN':
    driver.get('https://assistant.google.com/explore?hl=en')
    path1 = './appurl_en.txt'
    path2 = '../page_info_en.json'
    if not(os.path.exists('./page_source_en')):
        os.mkdir('./page_source_en')
    if not(os.path.exists('./metadata_en')):
        os.mkdir('./metadata_en')
elif locale == 'JA':
    driver.get('https://assistant.google.com/explore?hl=ja_jp')
    path1 = './appurl_ja.txt'
    path2 = '../page_info_ja.json'
    if not(os.path.exists('./page_source_ja')):
        os.mkdir('./page_source_ja')
    if not(os.path.exists('./metadata_ja')):
        os.mkdir('./metadata_ja')

with open(path1, 'r', encoding='utf-8') as f1:
    urls = f1.readlines()
    urls = [url.strip() for url in urls]

metadata = {}
count = 1
for url in urls:
    if locale == 'EN':
        url += '?hl=en'
        path3 = './page_source_en/source' + str(count) + '.html'
        path4 = './metadata_en/data' + str(count) + '.json'
    elif locale == 'JA':
        url += '?hl=ja_jp'
        path3 = './page_source_ja/source' + str(count) + '.html'
        path4 = './metadata_ja/data' + str(count) + '.json'
    jf = {
        "Name": None,
        "Developer": None,
        "Category": None,
        "Devices": None,
        "Description": None,
        "Commands": None,
        "Rating": None,
        "5_star": None,
        "4_star": None,
        "3_star": None,
        "2_star": None,
        "1_star": None,
        "NumberOfUsers": None,
        "PageUrl": url,
        "PolicyUrl": None
    }
    driver.get(url)

    try:
        jf["Name"] = driver.find_element(By.XPATH, '//*[@class="YtWsM RfR9R"]').text
    except:
        html = driver.page_source
        with open(path3, 'w', encoding='utf-8') as f3:
            f3.write(html)
        with open(path4, 'w', encoding='utf-8') as f4:
            json.dump(jf, f4, indent=4, ensure_ascii=False)
        
        metadata[count] = jf
        count += 1
        continue
        
    jf["Developer"] = driver.find_element(By.XPATH, '//*[@class="lUcxUb CbqDob"]').text

    categories = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/span/div/div[2]/div/c-wiz/div/div[3]/div[2]/div[1]/div/div')
    devices = driver.find_elements(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/span/div/div[2]/div/c-wiz/div/div[3]/div[2]/div[2]/div/div')
    
    category_list = []
    for category in categories:
        category_list.append(category.text)
    device_list = []
    for device in devices:
        device_list.append(device.text)
    jf["Category"] = category_list
    jf["Devices"] = device_list
    
    jf["Description"] = driver.find_element(By.XPATH, '//*[@class="IB9ccf"]').text.replace('\n', '')
    
    commands = driver.find_elements(By.XPATH, '//*[@class="bCHKrf"]')
    command_list = []
    for command in commands:
        command_list.append(command.text)
    jf["Commands"] = command_list

    try:
        star = driver.find_element(By.XPATH, '//*[@class="NRNQAb FTlnHb"]').text
        user = driver.find_element(By.XPATH, '//*[@class="rriIab CdFZQ"]').text
        jf["Rating"] = star
        jf["NumberOfUsers"] = user
    except:
        pass
        
    try:
        stars = driver.find_elements(By.XPATH, '//*[@class="CdFZQ  E6Tcbd"]')
        star_list = []
        for st in stars:
            star_list.append(st.text)
        jf["5_star"] = star_list[0]
        jf["4_star"] = star_list[1]
        jf["3_star"] = star_list[2]
        jf["2_star"] = star_list[3]
        jf["1_star"] = star_list[4]
    except:
        pass

    try:
        privacy = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[4]/span/div/div[2]/div/c-wiz/div/div[5]/a').get_attribute("href")
        jf["PolicyUrl"] = privacy
    except:
        pass

    html = driver.page_source
    with open(path3, 'w', encoding='utf-8') as f3:
        f3.write(html)
    with open(path4, 'w', encoding='utf-8') as f4:
        json.dump(jf, f4, indent=4, ensure_ascii=False)
        
    metadata[count] = jf
    count += 1

with open(path2, 'w', encoding='utf-8') as f2:
    json.dump(metadata, f2, indent=4, ensure_ascii=False)

try:
    driver.quit()
except http.client.RemoteDisconnected:
    pass