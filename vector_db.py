import chromadb
import uuid

class ChromaDB:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./chromadb")
        self.collection = None
        self.embedding_model = None

    def initialize_chroma_db_collection(self, collection_name: str) -> None:
        if self.embedding_model != None:
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name, embedding_function=self.embedding_model)
        else:
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)

    def upload_video_to_collection(self, video_name: str, video_transcript: str, start_time: str, end_time: str, id=str(uuid.uuid4()), embedding_vector=None) -> None:
        try:
            if embedding_vector != None:
                self.collection.add(
                    ids=[id],
                    embeddings= [embedding_vector],
                    documents=[video_transcript],
                    metadatas=[{"video-source":video_name, "start-time":start_time, "end-time":end_time}]
                )
            else:
                 self.collection.add(
                    ids=[id],
                    documents=[video_transcript],
                    metadatas=[{"video-source":video_name, "start-time":start_time, "end-time":end_time}]
                )
        except Exception as e:
            print("Error uploading video to collection:", e)
        else:
            print("Successfully added video to collection!")
    
    def upload_chunks_to_collection(self, video_name: str, video_chunk_names=[], video_transcripts=[], times = []):
        if len(times) != len(video_transcripts) or len(video_chunk_names) != len(video_transcripts):
            print("Each video chunk must have a transcript/description and start/end times!")
            return
        
        for i in range(len(video_transcripts)):
            video_chunk_name = video_chunk_names[i]
            video_transcript = video_transcripts[i]
            start_time, end_time = times[i]
            self.upload_video_to_collection(video_name, video_transcript, start_time, end_time, video_chunk_name)
    
    def query_k_clips(self, video_id: str, query: str, k: int):
        return self.collection.query(
            query_texts=[query],
            n_results=k,
            where={"video_id":video_id}
        )

        


            
    
    
