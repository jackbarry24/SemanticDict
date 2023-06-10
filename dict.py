import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os
import uuid


class SemanticDict():
    def __init__(self, threshold: float=0.1, overwrite: bool=False):
        self.threshold = threshold
        self.dict = {}
        self.empty = True
        self.collection_name = "semantic_dict"
        self.client = None
        self.collection = None
        self.overwrite = overwrite
        self._init_chroma()
        
    def _init_chroma(self):
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

        #if collection already exists, delete it to remove old keys
        try:
            client.delete_collection(
                name=self.collection_name
            )
        except:
            pass
            
        collection = client.create_collection(
            name=self.collection_name,
            embedding_function=ef
        )

        self.client = client
        self.collection = collection

    def _embed_key(self, key: str):
        self.collection.add(
            documents=[key],
            ids=[str(uuid.uuid4())]
        )

    def _get_key(self, key: str):
        match = self.collection.query(
            query_texts=[key],
            n_results=1
        )
        key_hit = match.get('documents')[0][0]
        distance = match.get('distances')[0][0]
        id = match.get('ids')[0][0]

        return key_hit, distance, id

    def __getitem__(self, key: str):
        #check to see if the embedding space is empty
        if self.empty:
            raise KeyError(f"{key}")
        
        #check to see if there is an exact match in the dict
        try:
            return self.dict[key]
        except KeyError:
            pass

        key_hit, distance, id = self._get_key(key)

        if distance > self.threshold:
            raise KeyError(f"{key}")
        
        return self.dict[key_hit]
        
    def __setitem__(self, key: str, val):
        self.empty = False
        if self.overwrite:
            #see if there is a matching key within threshold
            key_hit, distance, id = self._get_key(key)
            if distance <= self.threshold:
                self.dict[key_hit] = val
                return
            else:
                self.dict[key] = val
                self._embed_key(key)

        #if not overwrite, or no matching key, add new key-val pair
        else:
            self.dict[key] = val
            self._embed_key(key)
        

    def __delitem__(self, key: str):
        if self.empty:
            raise KeyError(f"{key}")
        
        #check to see if there is an exact match in the dict
        try:
            del self.dict[key]
            return
        except KeyError:
            pass
        
        key_hit, distance, id = self._get_key(key)

        if distance > self.threshold:
            raise KeyError(f"{key}")
        
        del self.dict[key]
        self.collection.delete(ids=[id])

    def __len__(self):
        return len(self.dict)
    
    def __str__(self):
        return str(self.dict)
    
    def peek(self):
        return self.collection.peek().get('documents')

    
