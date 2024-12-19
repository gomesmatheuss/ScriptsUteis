import subprocess
import os

def compress_video(input_path, output_path, bitrate="2M", preset="medium"):
    """
    Compress a video file using FFmpeg while keeping the original resolution.

    Parameters:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the compressed video.
        bitrate (str): Target video bitrate (e.g., '500k', '1M', '2M'). Default is '2M'.
        preset (str): Compression speed preset ('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'). Default is 'medium'.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' does not exist.")

    if not input_path.endswith('.mp4'):
        raise ValueError("The input file must be in .mp4 format.")

    try:
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vcodec", "libx264",
            "-b:v", bitrate,
            "-preset", preset,
            "-acodec", "aac",
            "-b:a", "97k",
            "-map_metadata", "0",
            output_path
        ]
        subprocess.run(command, check=True)
        print(f"Video compressed successfully and saved to '{output_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error compressing video: {e}")

if __name__ == "__main__":
    input_video = "path.mp4"
    output_video = "path.mp4"
    bitrate = "5000k"

    compress_video(input_video, output_video, bitrate)
