import os
import sys
import time
from instagram_upload import main as instagram_upload
from snapchat_upload import main as snapchat_upload
from tiktok_upload import main as tiktok_upload
from youtube_upload import main as youtube_upload
from x_upload import main as x_upload
from linkedin_upload import main as linkedin_upload
from config import Config

def upload_with_retry(upload_func, *args, max_retries=3):
    for attempt in range(max_retries):
        try:
            upload_func(*args)
            print(f"{upload_func.__name__} succeeded on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"{upload_func.__name__} failed on attempt {attempt + 1}: {e}")
            time.sleep(5)  
    print(f"{upload_func.__name__} failed after {max_retries} attempts")
    return False

def get_user_choices():
    platforms = {
        "1": ("Instagram", instagram_upload, Config.instagram_cookies_file),
        "2": ("TikTok", tiktok_upload, Config.tiktok_cookies_file),
        "3": ("YouTube", youtube_upload, Config.youtube_cookies_file),
        "4": ("Snapchat", snapchat_upload, None),
        "5": ("X", x_upload, Config.x_cookies_file),
        "6": ("Linkedin", linkedin_upload, Config.linkedin_cookies_file)
    }
    
    print("Which platforms do you want to upload to? Enter the corresponding number(s):")
    print("ENTER: All")
    print("1: Instagram")
    print("2: TikTok")
    print("3: YouTube")
    print("4: Snapchat")
    print("5: X")
    print("6: Linkedin")
    print("Example: '12' to select Instagram and TikTok")
    
    choices = input("Enter your choices: ")
    
    selected_platforms = [platforms[choice] for choice in choices if choice in platforms]
    
    if not selected_platforms:
        return list(platforms.values())  
    
    return selected_platforms

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    video_path = Config.video_path
    description_file_path = Config.description_file_path

    selected_platforms = get_user_choices()
    failed_uploads = []

    for platform_name, upload_func, cookies_file in selected_platforms:
        if not upload_with_retry(upload_func, video_path, description_file_path, cookies_file):
            failed_uploads.append((platform_name, upload_func, video_path, description_file_path, cookies_file))

    while failed_uploads:
        platform_name, func, *args = failed_uploads.pop(0)
        print(f"Retrying {platform_name} upload...")
        if not upload_with_retry(func, *args):
            failed_uploads.append((platform_name, func, *args))

if __name__ == "__main__":
    main()
