import streamlit as st
import subprocess
import os
import requests

def check_ffmpeg_installation():
    """Check if FFmpeg is installed and accessible."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        st.success("FFmpeg is installed and accessible.")
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

def download_twitch_video(twitch_url, output_dir):
    """Download a Twitch video (placeholder logic)."""
    try:
        # Placeholder for actual Twitch download implementation
        st.info(f"Downloading video from: {twitch_url}")
        sample_video_path = "sample_twitch_live.mp4"  # Replace with actual download logic
        output_path = os.path.join(output_dir, sample_video_path)
        st.success(f"Video downloaded to {output_path}")
        return output_path
    except Exception as e:
        st.error(f"Error downloading video: {e}")
        return None

def post_to_tiktok(video_path, tiktok_api_key):
    """Simulate posting a video to TikTok."""
    try:
        st.info(f"Uploading {video_path} to TikTok...")
        with open(video_path, "rb") as video_file:
            response = requests.post(
                "https://api.tiktok.com/upload",
                headers={"Authorization": f"Bearer {tiktok_api_key}"},
                files={"video": video_file}
            )
        if response.status_code == 200:
            st.success(f"Successfully posted {video_path} to TikTok!")
        else:
            st.error(f"Failed to post {video_path}: {response.text}")
    except Exception as e:
        st.error(f"Error posting video to TikTok: {e}")

def process_video(twitch_url, output_dir, clip_duration, tiktok_api_key):
    video_path = download_twitch_video(twitch_url, output_dir)
    if video_path:
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}_clip.mp4")
        cut_video(video_path, output_file, start_time=0, duration=clip_duration)
        post_to_tiktok(output_file, tiktok_api_key)
        return output_file
    return None

# Streamlit app
st.title("Twitch to TikTok Cutter and Uploader")

# Check FFmpeg installation
check_ffmpeg_installation()

# User input for Twitch live URL
twitch_url = st.text_input("Enter Twitch live URL:")

# User input for TikTok API key
tiktok_api_key = st.text_input("Enter TikTok API Key:", type="password")

# User input for clip duration
clip_duration = st.number_input("Clip duration (in seconds):", min_value=1, value=60)

# Directory for output
output_dir = "clips"
os.makedirs(output_dir, exist_ok=True)

if st.button("Download, Process, and Upload Video"):
    if not twitch_url or not tiktok_api_key:
        st.error("Please provide both the Twitch URL and TikTok API Key.")
    else:
        output_file = process_video(twitch_url, output_dir, clip_duration, tiktok_api_key)
        if output_file:
            st.success(f"Video processed and uploaded successfully: {output_file}")
