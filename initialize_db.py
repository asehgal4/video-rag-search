from utils.caption_video import caption_video
from utils.vector_db import ChromaDB
from utils.video_slicer import chunk_video
import argparse
import os

# Function to take lists of video names and paths and chunk times for each video to upload to vector db
def initialize_db(video_paths: list, video_names: list, chunk_times: list):
    db = ChromaDB()
    db.initialize_chroma_db_collection("videos")

    for video_path, video_name, chunk_time in zip(video_paths, video_names, chunk_times):
        chunk_folder = chunk_video(video_path, video_name, chunk_time)
        video_descriptions, start_end_times = caption_video(chunk_folder)

        video_chunk_names = sorted(os.listdir(chunk_folder))
        db.upload_chunks_to_collection(video_name, video_chunk_names, video_descriptions, start_end_times)
    
    return db


# Main function/entry point for uplading individual videos to vector db for rag pipeline
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This initializes the vector database with videos and their chunks for the rag pipeline")
    parser.add_argument('filepath', help='Path to input mp4 file')
    parser.add_argument('video_name', help='Title of the video')
    parser.add_argument('--chunk_time', '-t', help='Optional specified time span of each chunk', default=10)
    args = parser.parse_args()

    video_paths, video_names, chunk_times = [args.filepath], [args.video_name], [int(args.chunk_time)]
    initialize_db(video_paths, video_names, chunk_times)
