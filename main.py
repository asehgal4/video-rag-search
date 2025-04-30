from caption_video import caption_video
from vector_db import ChromaDB
from video_slicer import chunk_video
import os

VIDEO_CHUNK_TIME=5

def main():
    chunk_folder = chunk_video("videos/earth.mp4", "earth", VIDEO_CHUNK_TIME)
    video_descriptions, start_end_times = caption_video(chunk_folder)
    
    db = ChromaDB()
    db.initialize_chroma_db_collection("videos")

    video_chunk_names = sorted(os.listdir(chunk_folder))
    db.upload_chunks_to_collection("earth.mp4", video_chunk_names, video_descriptions, start_end_times)



if __name__ == "__main__":
    main()
