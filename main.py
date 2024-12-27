import os
import subprocess
import streamlit as st
from tiktok_uploader import upload_video

def check_ffmpeg_installation():
    """Check if FFmpeg is installed and accessible."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        st.success("FFmpeg is installed and accessible.")
        st.text(result.stdout.decode())
    except FileNotFoundError:
        st.error("FFmpeg is not installed or not accessible in the system PATH. Make sure to add 'ffmpeg' to the 'packages.txt' file in your project.")
    except Exception as e:
        st.error(f"Unexpected error while checking FFmpeg: {e}")

def cut_video(input_file, output_file, start_time, duration):
    """Cut a video using FFmpeg."""
    try:
        subprocess.run([
            "ffmpeg", "-i", input_file, "-ss", str(start_time), "-t", str(duration), "-c:v", "libx264", "-c:a", "aac", output_file
        ], check=True)
        st.success(f"Clip created: {output_file}")
    except subprocess.CalledProcessError as e:
        st.error(f"Error while cutting video: {e}")

def upload_to_tiktok(video_path, cookies_path):
    """Upload video to TikTok using tiktok_uploader."""
    try:
        st.info(f"Uploading {video_path} to TikTok...")
        upload_video(video_path, cookies_path)
        st.success(f"Successfully uploaded {video_path} to TikTok!")
    except Exception as e:
        st.error(f"Error uploading video to TikTok: {e}")

# Streamlit app
st.title("Twitch to TikTok Cutter and Uploader")

# Check FFmpeg installation
check_ffmpeg_installation()

# User input for video processing
video_path = st.text_input("Enter the path to your video:")
clip_duration = st.number_input("Clip duration (in seconds):", min_value=1, value=60)
output_dir = "clips"
os.makedirs(output_dir, exist_ok=True)

# Path to TikTok cookies
cookies_path = st.text_input("Enter the path to your TikTok cookies file:")

if st.button("Process and Upload Video"):
    if not video_path or not cookies_path:
        st.error("Please provide both the video path and TikTok cookies path.")
    else:
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}_clip.mp4")
        cut_video(video_path, output_file, start_time=0, duration=clip_duration)
        upload_to_tiktok(output_file, cookies_path)
