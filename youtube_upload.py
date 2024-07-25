import os
import pickle
import random
import time
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import Config

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

def read_video_details(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n\n')
        title = content[0]
        description = '\n\n'.join(content[1:3])
        tags = ','.join(content[3].split('#')[1:]) if len(content) > 3 else ""
        return title, description, tags

def load_cookies(driver, cookies_file):
    driver.get("https://www.youtube.com/")
    spoof_navigator(driver)
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def upload_video(driver, video_path, title, description, tags):
    driver.get("https://www.youtube.com/upload")
    spoof_navigator(driver)

    try:
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(video_path)
        time.sleep(10)
    except Exception as e:
        print("File input send keys failed:", e)
        return
    
    try:
        title_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="textbox"]'))
        )
        title_box.clear()
        title_box.send_keys(title)
    except Exception as e:
        print("Title input failed:", e)

    try:
        description_box = driver.find_elements(By.XPATH, '//*[@id="textbox"]')[1]
        description_box.send_keys(description)
    except Exception as e:
        print("Description input failed:", e)
    
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//ytcp-button[@id="toggle-button"]'))
        )
        show_more_button.click()
    except Exception as e:
        print("Show more button click failed:", e)

    try:
        tags_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Tags"]'))
        )
        tags_box.send_keys(tags)
    except Exception as e:
        print("Tags input failed:", e)

    try:
        for _ in range(3):
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//ytcp-button[@id="next-button"]'))
            )
            next_button.click()
    except Exception as e:
        print("Next button click failed:", e)
        return

    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Checks complete')]"))
        )
    except Exception as e:
        print("Failed to detect checking stage message:", e)

    try:
        publish_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ytcp-button[@id="done-button"]//div[text()="Publish"]'))
        )
        driver.execute_script("arguments[0].click();", publish_button)
    except Exception as e:
        print("publish sharing failed:", e)
        return
    
    try:
        time.sleep(5)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'published')]"))
        )
    except Exception as e:
        print("Failed to detect published stage message:", e)

def main(video_path, description_file_path, cookies_file):
    title, description, tags = read_video_details(description_file_path)
    options = uc.ChromeOptions()
    ua = UserAgent()
    options.add_argument(str(ua.random))
    driver = uc.Chrome(options=options)

    try:
        load_cookies(driver, cookies_file)
        upload_video(driver, video_path, title, description, tags)
    finally:
        driver.quit()

if __name__ == "__main__":
    main(Config.video_path, Config.description_file_path, Config.tiktok_cookies_file)
