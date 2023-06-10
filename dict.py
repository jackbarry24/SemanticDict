import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os
import uuid


class SemanticDict():
    def __init__(self, threshold: float=0.1):
        self.threshold = threshold
        self.dict = {}
        self.empty = True
        self.collection_name = "semantic_dict"
        self.client = None
        self.collection = None
        self.init_chroma()
        

    def init_chroma(self):
        try:
            api_key = os.environ['OPENAI_API_KEY']
        except KeyError:
            raise Exception('OPENAI_API_KEY not found in environment variables')
        
        ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-ada-002"
        )

        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=".chromadb/"
        ))

        collection = client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=ef
        )

        self.client = client
        self.collection = collection

    def embed(self, val: str):
        self.collection.add(
            documents=[val],
            ids=[str(uuid.uuid4())]
        )

    def __getitem__(self, key: str):
        #check to see if the embedding space is empty
        if self.empty:
            raise KeyError(f"{key}")
        
        #check to see if there is an exact match in the dict
        try:
            return self.dict[key]
        except KeyError:
            pass

        context = self.collection.query(
            query_texts=[key],
            n_results=1
        )

        new_key = context.get('documents')[0][0]
        distance = context.get('distances')[0][0]

        if distance > self.threshold:
            raise KeyError(f"{key}")
        
        return self.dict[new_key]
        
    def __setitem__(self, key: str, val: str):
        self.dict[key] = val
        self.embed(key)
        self.empty = False

    def __delitem__(self, key: str):
        if self.empty:
            raise KeyError(f"{key}")
        
        context = self.collection.query(
            query_texts=[key],
            n_results=1
        )

        id = context.get('ids')[0][0]
        distance = context.get('distances')[0][0]

        if distance > self.threshold:
            raise KeyError(f"{key}")
        
        del self.dict[key]
        self.collection.delete(ids=[id])

    def __del__(self):
        self.client.delete_collection(
            name=self.collection_name
        )

    def __len__(self):
        return len(self.dict)
    
    def __str__(self):
        return str(self.dict)
    
    def peek(self):
        return self.collection.peek().get('documents')

    
