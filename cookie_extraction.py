import pickle
import random
import time
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

def login_to_instagram_and_save_cookies(driver, username, password, cookies_file):
    driver.get("https://www.instagram.com/")
    random_sleep(3, 6)
    
    spoof_navigator(driver)

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')
    
    username_input.send_keys(username)
    random_sleep(1, 2)
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)
    
    random_sleep(5, 8)

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_tiktok_and_save_cookies(driver, username, password, cookies_file):
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    random_sleep(3, 6)
    
    spoof_navigator(driver)

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    
    username_input.send_keys(username)
    random_sleep(1, 2)
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)
    
    random_sleep(5, 8)

    driver.get("https://www.tiktok.com/login")

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_youtube_and_save_cookies(driver, email, password, cookies_file):
    driver.get("https://www.youtube.com/")

    spoof_navigator(driver)

    random_sleep(3, 6)
    
    sign_in_button = driver.find_element(By.XPATH, '//*[@aria-label="Sign in"]')
    sign_in_button.click()
    
    random_sleep(3, 6)
    
    email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_input.send_keys(email)
    random_sleep(1, 2)
    email_input.send_keys(Keys.RETURN)
    
    random_sleep(3, 6)

    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)
    
    random_sleep(5, 8)

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def main():
    options = uc.ChromeOptions()
    ua = UserAgent()
    options.add_argument(str(ua.random))
    driver = uc.Chrome(options=options)

    try:
        login_to_instagram_and_save_cookies(driver, Config.instagram_username, Config.instagram_password, Config.instagram_cookies_file)
        login_to_tiktok_and_save_cookies(driver, Config.tiktok_username, Config.tiktok_password, Config.tiktok_cookies_file)
        login_to_youtube_and_save_cookies(driver, Config.youtube_email, Config.youtube_password, Config.youtube_cookies_file)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
