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

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    video_path = Config.video_path
    description_file_path = Config.description_file_path

    failed_uploads = []

    if not upload_with_retry(instagram_upload, video_path, description_file_path, Config.instagram_cookies_file):
        failed_uploads.append(("Instagram", instagram_upload, video_path, description_file_path, Config.instagram_cookies_file))

    if not upload_with_retry(snapchat_upload, video_path, description_file_path):
        failed_uploads.append(("Snapchat", snapchat_upload, video_path, description_file_path))

    if not upload_with_retry(tiktok_upload, video_path, description_file_path, Config.tiktok_cookies_file):
        failed_uploads.append(("TikTok", tiktok_upload, video_path, description_file_path, Config.tiktok_cookies_file))

    if not upload_with_retry(youtube_upload, video_path, description_file_path, Config.youtube_cookies_file):
        failed_uploads.append(("YouTube", youtube_upload, video_path, description_file_path, Config.youtube_cookies_file))

    if not upload_with_retry(x_upload, video_path, description_file_path, Config.x_cookies_file):
        failed_uploads.append(("X", x_upload, video_path, description_file_path, Config.x_cookies_file))

    if not upload_with_retry(linkedin_upload, video_path, description_file_path, Config.linkedin_cookies_file):
        failed_uploads.append(("Linkedin", linkedin_upload, video_path, description_file_path, Config.linkedin_cookies_file))

    while failed_uploads:
        platform, func, *args = failed_uploads.pop(0)
        print(f"Retrying {platform} upload...")
        if not upload_with_retry(func, *args):
            failed_uploads.append((platform, func, *args))  

if __name__ == "__main__":
    main()