from utils.vector_db import ChromaDB
from utils.caption_video import query_model, client, MAX_CAPTION_TOKEN_LEN as MAX_QUERY_LENGTH, CAPTION_MODEL as QUERY_MODEL
import argparse

SYSTEM_PROMPT = """
You are an intelligent video analyzer tasked with describing a video scene and identifying any key moments and important events that occur.

Based on the input query, you also have access to metadata for the top k chunks of key moments that might relate to what the user is asking.
These chunks of key moments smaller sections of video taken from the longer video the user wants to ask questions about. The chunk metadata may help you
answer the question, but they aren't perfect so you may have to look beyond the metadata provided by the chunks. The metadata is ordered by how relevant the
chunk is to the query. The metadata provided by each chunk will include the following:

1. A text description of what is going on in the chunk of video
2. The start and end times in the video where the chunk takes place

The medata will be provided in the following format:
Chunk \{Rank\}: ...
Description: ...
Start Time: MM:SS.MS
End Time: MM:SS.MS

Using this metadata, answer any questions the user has on where and when an event in the video occurs.

Here is the metadata:

"""
NUM_CHUNKS_FOR_CONTEXT = 5

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This queries the video and rag pipeline to check to see if an event occured")
    parser.add_argument('query', help='Path to input mp4 file')
    parser.add_argument('video_name', help='Title of the video')
    args = parser.parse_args()

    query, video_name = args.query, args.video_name
    db = ChromaDB()
    db.initialize_chroma_db_collection("videos")

    query_results = db.query_k_clips(video_name, query, NUM_CHUNKS_FOR_CONTEXT)
    
    ids=query_results["ids"][0]
    documents=query_results["documents"][0]
    metadatas=query_results["metadatas"][0]


    system_prompt = SYSTEM_PROMPT
    for i, (doc, metadata) in enumerate(zip(documents, metadatas), start=1):
        system_prompt += f""" Chunk {i}
        Description: {doc}
        Start Time: {metadata['start-time']}
        End Time: {metadata['end-time']}\n\n\n"""
        print(doc)
    
    messages = [
            {"role": "system", "content": [
                {"type": "text", "text": system_prompt}
            ]},
            {"role": "user", "content": [
                {"type": "text", "text": query},
                ]}
            ]
    result = query_model(client, QUERY_MODEL, MAX_QUERY_LENGTH, messages)
    if result:
        print(result)
    else:
        print(f"Failed to get caption for {video_name}")