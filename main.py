from instagram_upload import main as instagram_upload
from snapchat_upload import upload_video as snapchat_upload
from tiktok_upload import main as tiktok_upload
from youtube_upload import main as youtube_upload
from config import Config

def main():
    video_path = Config.video_path
    description_file_path = Config.description_file_path

    instagram_upload(video_path, description_file_path, Config.instagram_cookies_file)

    snapchat_upload(video_path, description_file_path)

    tiktok_upload(video_path, description_file_path, Config.tiktok_cookies_file)

    youtube_upload(video_path, description_file_path, Config.youtube_cookies_file)

if __name__ == "__main__":
    main()
