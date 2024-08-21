import os
import pickle
import random
import time
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pywinauto import Application, timings
from pywinauto.keyboard import send_keys
from pywinauto.timings import wait_until_passes
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
    driver.get("https://www.linkedin.com/feed/")
    spoof_navigator(driver)

    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            if 'domain' in cookie:
                del cookie['domain']
            driver.add_cookie(cookie)

    driver.refresh()
    random_sleep(3, 5)

def upload_video(driver, video_path, description):
    spoof_navigator(driver)
    driver.get("https://www.linkedin.com/feed/")

    try:
        media_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add media']"))
        )
        media_button.click()
    except Exception as e:
        print("no media button appeared or click failed:", e)

    time.sleep(3)

    try:
        app = Application(backend='win32').connect(title_re="Open", visible_only=True)
        dlg = app.window(title_re="Open")
        dlg.wait('visible')

        wait_until_passes(5, 0.5, lambda: dlg.Edit1.exists())
        dlg.Edit1.set_edit_text(video_path)

        send_keys('{ENTER}')
        print("File path set and 'Open' button clicked.")
    except Exception as e:
        print("File input send keys failed:", e)
        

    try:
        media_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Next']"))
        )
        media_button.click()
    except Exception as e:
        print("no next button appeared or click failed:", e)

    time.sleep(3)

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@contenteditable="true"]'))
        )
        actions = ActionChains(driver)
        for i in description:
            actions.send_keys(i)
            actions.perform()
            random_sleep(0.01, 0.03)
        time.sleep(1)
    except Exception as e:
        print("Description input failed:", e)

    time.sleep(3)

    try:
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button') and .//span[text()='Post']]"))
        )
        post_button.click()
    except Exception as e:
        print("Post sharing failed:", e)
    
    time.sleep(30)

    try:
        time.sleep(5)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'published')]"))
        )
        print("Upload success message detected. Closing the browser.")
    except Exception as e:
        print("Failed to detect published stage message:", e)

def main(video_path, description_file_path, cookies_file):
    description = read_description(description_file_path)
    options = uc.ChromeOptions()
    ua = UserAgent()
    options.add_argument(str(ua.random))
    driver = uc.Chrome(options=options)

    try:
        load_cookies(driver, cookies_file)
        upload_video(driver, video_path, description)
    finally:
        driver.quit()

if __name__ == "__main__":
    main(Config.video_path, Config.description_file_path, Config.linkedin_cookies_file)
