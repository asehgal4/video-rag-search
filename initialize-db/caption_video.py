import os
import cv2
import base64
from openai import AzureOpenAI
from collections import deque

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_VERSION = "2024-08-01-preview"
client = AzureOpenAI(
            azure_endpoint=  os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=API_VERSION)

CAPTION_MODEL = "gpt-4o"
MAX_CAPTION_TOKEN_LEN = 512
SYSTEM_PROMPT = """
You are an intelligent video analyzer tasked with describing a video scene and identifying any key moments and important events that occur.

Your main goals are:
1. Provide a concise but complete description of what is happening in the video.
2. If you see evidence of any hazards, mention them explicitly. 
3. Make sure to mention any other events you deem unique, important, or otherwise relevant to understanding the context of the video.

"""

def caption_chunk(client, video, user_prompt):
    messages = [
        {"role": "system", "content": [
            {"type": "text", "text": SYSTEM_PROMPT}
        ]},
        {"role": "user", "content": [
            {"type": "text", "text": user_prompt},
            *map(lambda x: {"image": x, "resize": 768}, video),
        ]}
    ]

    try:
        response = client.chat.completions.create(
            #   deployment_id="YOUR_DEPLOYMENT_NAME",
            model=CAPTION_MODEL,
            messages=messages,
            max_tokens=MAX_CAPTION_TOKEN_LEN,
        )
        if response:
            return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return None

def format_mm_ss_ms(total_seconds: float) -> str:
    minutes = int(total_seconds) // 60
    seconds = int(total_seconds) % 60
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)

    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def get_video_duration(cap: cv2.VideoCapture) -> float:
    fps         = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    if fps == 0:
        raise ValueError("FPS is zero, can't compute duration")
    return frame_count / fps

def caption_video(video_chunks: str) -> list:
    captions = []
    start_end_times = [0]
    for video in sorted(os.listdir(video_chunks)):
        if video.endswith(".mp4"):
            video_path = os.path.join(video_chunks, video)
            print(f"Processing {video_path}")
            captions.append("")
            
            # send the video to gpt
            video_frames = []
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"Total frames: {total_frames}")
            max_frames = 50

            start_end_times.append(start_end_times[-1] + get_video_duration(cap))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                _, frame = cv2.imencode(".jpg", frame)
                frame = base64.b64encode(frame).decode("utf-8")
                video_frames.append(frame)
                if len(video_frames) >= max_frames:
                    caption = caption_chunk(client, video_frames, "Please describe the video and identify any hazards.")
                    if caption:
                        captions[-1] += caption + "\n"
                    else:
                        print(f"Failed to get caption for {video}")
                    video_frames = []
            cap.release()
    
    start_end_times = list(map(lambda x: format_mm_ss_ms(x), start_end_times))
    start_end_times = zip(start_end_times, start_end_times[1:])
    return captions, list(start_end_times)


            


