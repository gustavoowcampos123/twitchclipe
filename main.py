import streamlit as st
import subprocess
import os
import time

def check_ffmpeg_installation():
    """Check if FFmpeg is installed and accessible."""
    try:
        result = subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        st.success("FFmpeg is installed and accessible.")
        st.text(result.stdout.decode())  # Display FFmpeg version
    except FileNotFoundError:
        st.error("FFmpeg is not installed or not accessible in the system PATH.")
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

def generate_clips(video_path, output_dir, clip_duration):
    """Generate clips from a video in intervals."""
    try:
        # Get video duration
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        total_duration = float(result.stdout.strip())

        clip_count = 0
        for start_time in range(0, int(total_duration), clip_duration):
            output_file = os.path.join(output_dir, f"clip_{clip_count}.mp4")
            cut_video(video_path, output_file, start_time, clip_duration)
            clip_count += 1

        st.success(f"Generated {clip_count} clips.")
    except Exception as e:
        st.error(f"Error generating clips: {e}")

# Streamlit app
st.title("Twitch to TikTok Clip Generator")

# Check FFmpeg installation
check_ffmpeg_installation()

# User input for video processing
video_path = st.text_input("Enter the path to your video:")
clip_duration = st.number_input("Clip duration (in seconds):", min_value=1, value=300)  # Default: 5 minutes
output_dir = "clips"
os.makedirs(output_dir, exist_ok=True)

if st.button("Generate Clips"):
    if not video_path:
        st.error("Please provide the path to the video.")
    else:
        generate_clips(video_path, output_dir, clip_duration)
