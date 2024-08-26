import time
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from config import Config

def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readline().strip()
    
def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

def upload_video(driver, video_path, description_file_path, description=None):
    if not description:
        description = read_description(description_file_path)  
    
    try:
        driver.get('https://my.snapchat.com/')
        spoof_navigator(driver)

        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]"))
        )
        sign_in_button.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Use phone number instead']"))
        )

        webdriver.ActionChains(driver).send_keys(Config.snapchat_username).send_keys(Keys.RETURN).perform()

        time.sleep(30)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//p[text()='{Config.snapchat_username}']"))
        )

        webdriver.ActionChains(driver).send_keys(Config.snapchat_password).send_keys(Keys.RETURN).perform()

        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept='video/mp4,video/quicktime,video/webm,image/jpeg,image/png']"))
        )
        file_input.send_keys(video_path)
        time.sleep(10)

        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[5]/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]"))
        )
        post_button.click()

        description_textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Add a description and #topics']"))
        )
        description_textarea.send_keys(description)
        
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agree to Spotlight Terms')]"))
        )
        agree_button.click()

        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button[2]"))
        )
        accept_button.click()

        post_final_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post to Snapchat')]"))
        )
        post_final_button.click()

        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Yay! Your post is now live!']"))
        )
        print("Upload success message detected. Closing the browser.")

        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise  

    finally:
        driver.quit()

def main(video_path=None, description_file_path=None):
    video_path = video_path or Config.video_path
    description_file_path = description_file_path or Config.description_file_path
    
    options = uc.ChromeOptions()
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    driver = uc.Chrome(options=options)

    try:
        upload_video(driver, video_path, description_file_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()