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

def remove_non_bmp_characters(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n\n')
        title = content[0]  
        description = content[1] if len(content) > 1 else ""  
        tags = '# ' + ' '.join(content[2].split()) if len(content) > 2 else ""  
        return title, description, tags

def load_cookies(driver, cookies_file):
    driver.get("https://www.instagram.com/")
    spoof_navigator(driver)
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def dismiss_notifications_popup(driver):
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, '_a9--') and contains(@class, '_ap36') and contains(@class, '_a9_1') and text()='Not Now']"))
        )
        not_now_button.click()
    except Exception as e:
        print("No 'Turn on Notifications' popup appeared or click failed:", e)

def upload_video(driver, video_path, description, title, tags):
    dismiss_notifications_popup(driver)
    try:
        create_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Create']"))
        )
        create_button.click()
    except Exception as e:
        print("Create button click failed:", e)
        return
    
    try:
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(video_path)
    except Exception as e:
        print("File input send keys failed:", e)
        return
    
    try:
        OK_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        )
        OK_button.click()
    except Exception as e:
        print("OK button click failed:", e)

    try:
        crop_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Select crop']"))
        )
        crop_button.click()

        portrait_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='svg' and @aria-label='Crop portrait icon']"))
        )
        portrait_button.click()
    except Exception as e:
        print("Crop selection failed:", e)

    try:
        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and text()='Next']"))
        )
        next_button.click()

        time.sleep(1)

        next_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and text()='Next']"))
        )
        next_button.click()

        description_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and @aria-label='Write a caption...']"))
        )
        description_input.send_keys(title + "\n\n" + description + "\n\n" + tags)

        share_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[name()='div' and text()='Share']"))
        )
        share_button.click()
    except Exception as e:
        print("Post sharing failed:", e)
        return
    
    try:
        WebDriverWait(driver, 120).until(
            lambda driver: driver.execute_script("""
                var spans = document.querySelectorAll('span');
                for (var i = 0; i < spans.length; i++) {
                    if (spans[i].innerText.includes('Your reel has been shared.')) {
                        return true;
                    }
                }
                return false;
            """)
        )
        print("Upload success message detected. Closing the browser.")
    except Exception as e:
        print("Failed to detect upload success message:", e)

def main(video_path, description_file_path, cookies_file):
    title, description, tags = read_description(description_file_path)
    options = uc.ChromeOptions()
    ua = UserAgent()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    driver = uc.Chrome(options=options)

    try:
        load_cookies(driver, cookies_file)
        upload_video(driver, video_path, description, title, tags)
    finally:
        driver.quit()

if __name__ == "__main__":
    main(Config.video_path, Config.description_file_path, Config.instagram_cookies_file)
