import time
import random
from fake_useragent import UserAgent
import undetected_chromedriver as uc

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def main():
    ua = UserAgent()
    user_agent_string = ua.random

    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    print(user_agent_string)

    print(f"Using UserAgent: {user_agent_string}")  

    try:
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent_string})
        
        driver.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
        random_sleep(5, 8)
        
        user_agent_from_browser = driver.execute_script("return navigator.userAgent;")
        print(f"UserAgent from browser: {user_agent_from_browser}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
