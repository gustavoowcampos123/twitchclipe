import streamlit as st
import streamlit as st

def check_ffmpeg_installation():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        st.success("FFmpeg is installed and accessible.")
    except FileNotFoundError:
        st.error("FFmpeg is not installed on the system. Please ensure it's available.")

check_ffmpeg_installation()
import os

def cut_video(input_file, output_file, start_time, duration):
    """Cut a video using FFmpeg."""
    try:
        ffmpeg.input(input_file, ss=start_time, t=duration).output(output_file).run()
        st.success(f"Clip created: {output_file}")
    except ffmpeg.Error as e:
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

def process_video(twitch_url, output_dir, clip_duration):
    video_path = download_twitch_video(twitch_url, output_dir)
    if video_path:
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}_clip.mp4")
        cut_video(video_path, output_file, start_time=0, duration=clip_duration)
        return output_file
    return None
# Streamlit app
st.title("Twitch to TikTok Cutter and Uploader")

# User input for Twitch live URL
twitch_url = st.text_input("Enter Twitch live URL:")

# User input for clip duration
clip_duration = st.number_input("Clip duration (in seconds):", min_value=1, value=60)

# Directory for output
output_dir = "clips"
os.makedirs(output_dir, exist_ok=True)

if st.button("Download and Process Video"):
    if not twitch_url:
        st.error("Please provide the Twitch URL.")
    else:
        output_file = process_video(twitch_url, output_dir, clip_duration)
        if output_file:
            st.success(f"Video processed successfully: {output_file}")
