# Tiktok Instagram Youtube Snapchat Python Video Uploader

This project automates the process of uploading videos to Instagram, TikTok, YouTube, and Snapchat using Python and Selenium. 

## Prerequisites

1. **Python**: Make sure you have Python installed. You can download it from [here](https://www.python.org/downloads/).
2. **AutoIt**: For interacting with certain elements on Windows, AutoIt is required. You can download it from [here](https://www.autoitscript.com/site/autoit/downloads/).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/video-uploader.git
    cd video-uploader
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
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
        snapchat_username = "ur snap username"
        snapchat_password = "ur snap password"
        instagram_username = "ur insta username"
        instagram_password = "ur insta password"
        tiktok_username = "ur tiktok username"
        tiktok_password = "ur tiktok password"
        youtube_email = "ur yt email"
        youtube_password = "ur yt password"
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

- Ensure that the cookies are properly saved in the `.pkl` files for seamless login.
- The script uses the `fake_useragent` library to generate random user agents to avoid detection.
- However it is recommended that one uses their own user agent in (`tiktok_upload.py`) as for anti-automation
- The `undetected_chromedriver` library is used to bypass anti-bot mechanisms.
- For Snapchat, the AutoIt script is used to handle the file upload dialog. Ensure AutoIt is installed and configured.

## AutoIt Script

AutoIt script (`upload_video.au3`) is required for Snapchat file uploads. The script will be automatically executed when needed.

```autoit
; Wait for the Open dialog to become active
WinWaitActive("Open")

; Focus the edit control where the file path is to be entered
ControlFocus("Open", "", "Edit1")

; Set the file path in the edit control
ControlSetText("Open", "", "Edit1", "D:\\Your Path\\Your Path\\Your Path.mp4")

; Click the Open button to confirm the selection
ControlClick("Open", "", "Button1")
```

With this, you should be able to use the script to upload videos to multiple platforms efficiently.
