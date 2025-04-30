import ffmpeg
import argparse
import os
from datetime import datetime

# Uses ffmpeg to split video into chunks
def split_into_chunks(input_video_path: str, output_video_name: str, chunk_time_length: int = 10):
    (
        ffmpeg.input(input_video_path)
            .output(
                output_video_name,
                codec='copy',
                f='segment',
                segment_time=chunk_time_length,
                reset_timestamps=True
            )
            .run()
    )

def chunk_video(input_file_name: str, output_file_name: str, time_period: int) -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"run_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    split_into_chunks(input_file_name, f"{folder_name}/{output_file_name}_%03d.mp4", time_period)
    return folder_name

if __name__ == "__main__":
    # Parser to get arguments (file name, chunk size, optional output file chunk name)
    parser = argparse.ArgumentParser(description="This tool splits an input mp4 file into multiple chunks of a given time period")
    parser.add_argument('filename', help='Path to input mp4 file')
    parser.add_argument('time_period', help='Length of each output mp4 chunk')
    parser.add_argument('--output', '-o', help='Optional file name for mp4 chunks', default='out')
    args = parser.parse_args()

    input_file_name, time_period, output_file_name = args.filename, args.time_period, args.output

    # Creates a run folder to store chunked video based on current date+time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"run_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    split_into_chunks(input_file_name, f"{folder_name}/{output_file_name}_%03d.mp4", int(time_period))