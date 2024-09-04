# Tiktok Instagram Youtube Snapchat X Linkedin Video Uploader (Douyin Kuaishou Bilbili Comming Soon)

This project automates the process of uploading videos to Instagram, TikTok, YouTube, Snapchat, X and Linkedin using Python and Selenium. 

## Prerequisites

**Python**: Make sure you have Python installed. You can download it from [here](https://www.python.org/downloads/).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/EdwardZehuaZhang/Tiktok-Instagram-Youtube-Snapchat-X-Linkedin-Video-Uploader.git
    ```

2. Install the required Python packages:
    ```bash
    pip install fake_useragent undetected_chromedriver selenium pywinauto
    ```

## Configuration

1. **Config Class**: Replace the placeholders in the `Config` class with your own usernames, passwords, and file paths.
    ```python
    class Config:
        video_path = "Your video path"
        description_file_path = "Your file descript path, txt btw"
        instagram_cookies_file = "instagram_cookies.pkl"
        tiktok_cookies_file = "tiktok_cookies.pkl"
        youtube_cookies_file = "youtube_cookies.pkl"
        x_cookies_file = "x_cookies.pkl"
        linkedin_cookies_file = "linkedin_cookies.pkl"
        snapchat_username = "ur_snap_username"
        snapchat_password = "ur_snap_password"
        instagram_username = "ur_insta_username"
        instagram_password = "ur_insta_username"
        ......
    ```

2. **Cookie Extraction**: Run the script to login and save cookies for each platform. This will generate the required cookie files (`.pkl`):
    ```bash
    python extract_cookies.py
    ```

## Description File Structure

Create a description file for your video with the following structure:

1. Title on the first line
2. An empty line
3. Description paragraph
4. An empty line
5. Tags, separated by commas

Example:
```
My Video Title

This is a description of the video.

#tag1, #tag2, #tag3
```

## Usage

Run the main script to upload your video to all platforms:
```bash
python main.py
```

## Important Points

- The script uses the `fake_useragent` library to generate random user agents to avoid detection. However it is recommended that one uses their own user agent in (`tiktok_upload.py`) as for anti-automation
- Ensure that the cookies are properly saved in the `.pkl` files for seamless login.
- The `undetected_chromedriver` library is used to bypass anti-bot mechanisms.
