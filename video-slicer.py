import ffmpeg
import argparse
import os
from datetime import datetime

# Uses ffmpeg to split video into chunks
def splitIntoChunks(inputVideoPath: str, outputVideoName: str, chunkTimeLength: int = 10):
    (
        ffmpeg.input(inputVideoPath)
            .output(
                outputVideoName,
                codec='copy',
                f='segment',
                segment_time=chunkTimeLength,
                reset_timestamps=True
            )
            .run()
    )

if __name__ == "__main__":
    # Parser to get arguments (file name, chunk size, optional output file chunk name)
    parser = argparse.ArgumentParser(description="This tool splits an input mp4 file into multiple chunks of a given time period")
    parser.add_argument('filename', help='Path to input mp4 file')
    parser.add_argument('time_period', help='Length of each output mp4 chunk')
    parser.add_argument('--output', '-o', help='Optional file name for mp4 chunks', default='out')
    args = parser.parse_args()

    inputFileName, timePeriod, outputFileName = args.filename, args.time_period, args.output

    # Creates a run folder to store chunked video based on current date+time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"run_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    splitIntoChunks(inputFileName, f"{folder_name}/{outputFileName}_%03d.mp4", int(timePeriod))