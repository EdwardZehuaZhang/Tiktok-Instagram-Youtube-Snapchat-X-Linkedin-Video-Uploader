import os
import pickle
import random
import time
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pywinauto import Application, timings
from pywinauto.keyboard import send_keys
from config import Config

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_cookies(driver, cookies_file):
    driver.get("https://www.tiktok.com/login")
    spoof_navigator(driver)
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def upload_video(driver, video_path, description):    
    driver.get("https://www.tiktok.com/tiktokstudio/upload?from=creator_center")
    spoof_navigator(driver)

    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[data-tt="Upload_index_iframe"]'))
        )
        driver.switch_to.frame(iframe)

        upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Select video']"))
        )
        upload_button.click()
        time.sleep(3)
    except Exception as e:
        print("Cant find ifrmae or create button click failed:", e)
        
        try:
            upload_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Select video']"))
            )
            upload_button.click()
            time.sleep(3)
        except Exception as e:
            print("Create button click failed:", e)
        
        try:
            app = Application(backend='win32').connect(title_re="Open")
            dlg = app.Open
            dlg.wait('visible')
            dlg.Edit1.set_edit_text(video_path)
            
            open_button = dlg.Open
            open_button.wait('enabled', timeout=10)
            open_button.click()
            time.sleep(1)  
            send_keys('{ENTER}')
            print("File path set and 'Open' button clicked.")
        except Exception as e:
            print("File input send keys failed:", e)
            return
        
        try:
            driver.switch_to.default_content()

            editable_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true']"))
            )
            actions = ActionChains(driver)
            actions.move_to_element(editable_div).click().perform()
            
            actions.key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.DELETE)
            actions.send_keys(description)
            actions.perform()
        except Exception as e:
            print("Interaction with contenteditable div failed:", e)
        
        try:
            uploaded_text = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Uploaded']"))
            )
        except Exception as e:
            print("Failed to find 'Uploaded' text:", e)
            

        try:
            post_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'TUXButton') and .//div[text()='Post']]"))
            )
            post_button.click()
        except Exception as e:
            print("Post sharing failed:", e)
            

        try:
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Your video has been uploaded']"))
            )
        except Exception as e:
            print("Failed to detect upload success message:", e)

def main(video_path, description_file_path, cookies_file):
    description = read_description(description_file_path)
    options = uc.ChromeOptions()
    #note that you should replace this string with ur own useragent caz tiktok have good detection
    options.add_argument("Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
    driver = uc.Chrome(options=options)

    try:
        load_cookies(driver, cookies_file)
        upload_video(driver, video_path, description)
    finally:
        driver.quit()

if __name__ == "__main__":
    main(Config.video_path, Config.description_file_path, Config.tiktok_cookies_file)
