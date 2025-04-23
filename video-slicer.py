import ffmpeg
import argparse
import os
from datetime import datetime


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
    parser = argparse.ArgumentParser(description="This tool splits an input mp3 file into multiple chunks of a given time period")
    parser.add_argument('filename', help='Path to input mp3 file')
    parser.add_argument('time_period', help='Length of each output mp3 chunk')
    parser.add_argument('--output', '-o', help='Optional file name for mp3 chunks', default='out')
    args = parser.parse_args()

    inputFileName, timePeriod, outputFileName = args.filename, args.time_period, args.output

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"run_{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    splitIntoChunks(inputFileName, f"{folder_name}/{outputFileName}_%03d.mp3", int(timePeriod))