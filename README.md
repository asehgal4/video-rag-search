# video-rag-search

## Motivation
Current advancements in vision-language models (VLMs) have shown remarkable capabilities in understanding and reasoning about visual content. However, a significant challenge remains when dealing with long-duration videos. The sheer volume of information contained within these videos often exceeds the context window limitations of even the most sophisticated models. This constraint prevents the models from processing the entire video stream at once, hindering their ability to identify and recall crucial details or events that occur over extended periods. We created a pipeline to split longer videos into chunks, convert the chunks into a text embedding using GPT-4o, and store these chunks on device in ChromaDB. From here, you can query for events in the video and with our RAG pipeline, recieve responses faster in an order of magnitude.

## How to use
### Initial Setup
1. Use uv to create your own virtual python environment with the necessary packages
2. Create a `.env` file with environment variables for `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_KEY`

### Initialize ChromaDB With Relevant Videos
1. Run the `initialize_db.py` script as follows: `python initalize_db.py filepath-to-video video_name -t optional-size-of-each-chunk`

### Query Your Videos
1. Run the `query_model.py` script as follows: `python query_model.py query video_name`

## Example Videos

Building a log cabin (15min): https://drive.google.com/file/d/1dqVTdJBdy0mIe0NOzb9mebdXU4BhSEoj/view?usp=sharing
