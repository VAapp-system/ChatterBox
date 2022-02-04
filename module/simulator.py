import chromedriver_binary
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

class Crawler:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--mute-audio')
        self.driver = webdriver.Chrome(options=self.options)

    def quit(self):
        self.driver.close()
        self.driver.quit()

    def setting(self, mail_address, pass_word):
        self.mail_address = mail_address
        self.pass_word = pass_word
        driver = self.driver
        driver.get('https://console.actions.google.com/u/0/')
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Email"]')))
        driver.find_element(By.XPATH, '//*[@id="Email"]').send_keys(mail_address + Keys.ENTER)
        time.sleep(2)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pass_word + Keys.ENTER)
        time.sleep(5)
        driver.set_window_size(2000,1000)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' test1 ')]")))
        driver.find_element(By.XPATH, "//*[contains(text(), ' test1 ')]").click()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/a7t-topnav/div/div[4]/div[3]')))
        driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/a7t-topnav/div/div[4]/div[3]').click()

    def next(self, locale):
        driver = self.driver
        r_start = time.time()
        flag = False
        while(True):
            if time.time() - r_start > 30:
                break
            try:
                n = driver.find_element_by_xpath('/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[2]/div/div[2]/div/fb-chip/div')
                if (locale == 'JA' and n.text == 'テスト用アプリにつないで') or (locale == 'EN' and n.text == 'Talk to my test app'):
                    n.click()
                    flag = True
                    break
            except:
                pass
            time.sleep(2)
        if flag:
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[2]/div/div[2]/div/fb-chip/div')))
            driver.find_element_by_xpath('/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[2]/div/div[2]/div/fb-chip/div').click()
            time.sleep(2)
            return True
        else:
            return False

    def other_next(self):
        driver = self.driver
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s7r-query-input"]')))
        driver.find_element(By.XPATH, '//*[@id="s7r-query-input"]').send_keys(Keys.ENTER)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[2]/div/div[2]/div/fb-chip/div')))
        c = driver.find_element_by_xpath('/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[2]/div/div[2]/div/fb-chip/div')
        if c.text == 'cancel':
            c.click()
            time.sleep(2)
            return True
        else:
            return False
        
    def japanese(self):
        driver = self.driver
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-options/div/md-single-grid/div/md-card/div[2]/div')))
        driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-options/div/md-single-grid/div/md-card/div[2]/div').click()
        time.sleep(2)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' Japanese (Japan) ')]")))
        japan = driver.find_elements(By.XPATH, "//*[contains(text(), ' Japanese (Japan) ')]")
        if len(japan) == 1:
            japan[0].click()
        elif len(japan) == 2:
            japan[1].click()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s7r-options-location-input"]')))
        target = driver.find_element(By.XPATH, '//*[@id="s7r-options-location-input"]')
        target.clear()
        target.send_keys('Japan')
        actions = ActionChains(driver)
        actions.move_by_offset(1600,130)
        actions.click()
        actions.perform()
        time.sleep(3)

    def english(self):
        driver = self.driver
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-options/div/md-single-grid/div/md-card/div[2]/div')))
        driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-options/div/md-single-grid/div/md-card/div[2]/div').click()
        time.sleep(2)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), ' English (United States) ')]")))
        english = driver.find_elements(By.XPATH, "//*[contains(text(), ' English (United States) ')]")
        if len(english) == 1:
            english[0].click()
        elif len(english) == 2:
            english[1].click()
            
    def input_req(self, req):
        driver = self.driver
        time.sleep(2)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s7r-query-input"]')))
        driver.find_element(By.XPATH, '//*[@id="s7r-query-input"]').send_keys(req + Keys.ENTER)

    def output_res(self):
        driver = self.driver
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[1]/md-input-container')))
        class_value = driver.find_element(By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[1]/s7r-query-input/div/div[1]/md-input-container').get_attribute("class")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, 'tab-content-')]/div/div/fb-code-editor/div/div[6]/div[1]/div/div/div/div[5]/pre/span")))
        responses = driver.find_elements_by_xpath("//*[starts-with(@id, 'tab-content-')]/div/div/fb-code-editor/div/div[6]/div[1]/div/div/div/div[5]/pre/span")
        return class_value, responses

    def end(self):
        driver = self.driver
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-message-history/div/div[1]/div[2]/button')))
        driver.find_element_by_xpath('/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-message-history/div/div[1]/div[2]/button').click()
        time.sleep(2)

    def warning(self):
        driver = self.driver
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-message-history/div/div[2]/div/div[1]/div[2]/div/div')))
        text = driver.find_element_by_xpath('/html/body/await-bootstrap-ng2/ng-transclude/div/md-content/div[1]/div/div/div/ng-transclude/div/div/div/div[2]/s7r-message-history/div/div[2]/div/div[1]/div[2]/div/div').text
        return text

    def exit_check(self, page_url, locale):
        driver = self.driver
        for i in range(10):
            try:
                driver.execute_script("window.open()")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(page_url)
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@class="YtWsM RfR9R"]')))
                driver.find_element(By.XPATH, '//*[@class="YtWsM RfR9R"]').text
            except:
                break
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'VWIzNe')))
            reset = driver.find_elements(By.CLASS_NAME, 'VWIzNe')
            flag = True
            for r in reset:
                t = r.text
                if locale == 'JA':
                    if t == 'リセット':
                        reset = r
                        flag = False
                        break
                if locale == 'EN':
                    if t == 'Reset':
                        reset = r
                        flag = False
                        break
            if flag:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return 'Non-resettable'
            
            reset.click()
            time.sleep(1)
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[2]/span/span')))
            driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[2]/span/span').click()
            time.sleep(2)

            driver.get(page_url)

            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'VWIzNe')))
            show = driver.find_elements(By.CLASS_NAME, 'VWIzNe')
            flag = True
            for s in show:
                t = s.text
                if locale == 'JA':
                    if t == '[保存済みデータを表示]':
                        show = s
                        flag = False
                        break
                if locale == 'EN':
                    if t == '[View stored data]':
                        show = s
                        flag = False
                        break
            if flag:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return 'Storage not displayed'

            show.click()
            time.sleep(1)
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd1"]/div')))
                data = driver.find_element(By.XPATH, '//*[@id="dwrFZd1"]/div').text
            except:
                try:
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd3"]/div')))
                    data = driver.find_element(By.XPATH, '//*[@id="dwrFZd3"]/div').text
                except:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    return 'Storage not available'
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return data
        return False

    def get_storage(self, page_url, locale):
        driver = self.driver
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(page_url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'VWIzNe')))
        show = driver.find_elements(By.CLASS_NAME, 'VWIzNe')
        flag = True
        for s in show:
            t = s.text
            if locale == 'JA':
                if t == '[保存済みデータを表示]':
                    show = s
                    flag = False
                    break
            if locale == 'EN':
                if t == '[View stored data]':
                    show = s
                    flag = False
                    break
        if flag:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return 'Storage not displayed'

        show.click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd1"]/div')))
            data = driver.find_element(By.XPATH, '//*[@id="dwrFZd1"]/div').text
        except:
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd3"]/div')))
                data = driver.find_element(By.XPATH, '//*[@id="dwrFZd3"]/div').text
            except:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return 'Storage not available'

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return data

    def reset_storage(self, page_url, locale):
        driver = self.driver
        driver.execute_script("window.open()")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(page_url)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'VWIzNe')))
        reset = driver.find_elements(By.CLASS_NAME, 'VWIzNe')
        flag = True
        for r in reset:
            t = r.text
            if locale == 'JA':
                if t == 'リセット':
                    reset = r
                    flag = False
                    break
            if locale == 'EN':
                if t == 'Reset':
                    reset = r
                    flag = False
                    break
        if flag:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return 'Non-resettable'
        
        reset.click()
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[2]/span/span')))
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div/div[2]/div[3]/div[2]/span/span').click()
        time.sleep(2)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.execute_script("window.open()")

        driver.switch_to.window(driver.window_handles[1])
        driver.get(page_url)
        
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'VWIzNe')))
        show = driver.find_elements(By.CLASS_NAME, 'VWIzNe')
        flag = True
        for s in show:
            t = s.text
            if locale == 'JA':
                if t == '[保存済みデータを表示]':
                    show = s
                    flag = False
                    break
            if locale == 'EN':
                if t == '[View stored data]':
                    show = s
                    flag = False
                    break
        if flag:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return 'Storage not displayed'

        show.click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd1"]/div')))
            data = driver.find_element(By.XPATH, '//*[@id="dwrFZd1"]/div').text
        except:
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd3"]/div')))
                data = driver.find_element(By.XPATH, '//*[@id="dwrFZd3"]/div').text
            except:
                try:
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dwrFZd5"]/div')))
                    data = driver.find_element(By.XPATH, '//*[@id="dwrFZd5"]/div').text
                except:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    return 'Storage not available'
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        return data

    def screenshot(self, path):
        driver = self.driver
        driver.save_screenshot(path)

    def canvas(self):
        driver = self.driver
        time.sleep(10)
        canvas = driver.find_element(By.CLASS_NAME, 's7r-canvas-iframe')
        driver.switch_to.frame(canvas)
        canvas_html = driver.page_source
        text_elements = driver.find_elements(By.XPATH, '//*[text()][count(*)=0]')
        canvas_texts = []
        for element in text_elements:
            if element.text != '':
                canvas_texts.append(element.text)
        driver.switch_to.default_content()
        simu_html = driver.page_source
        return canvas_texts, canvas_html, simu_html
        
    def cancel(self):
        driver = self.driver
        time.sleep(2)
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="s7r-query-input"]')))
        driver.find_element(By.XPATH, '//*[@id="s7r-query-input"]').send_keys('cancel' + Keys.ENTER)
        time.sleep(3)
