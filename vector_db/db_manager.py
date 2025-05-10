import chromadb
from chromadb.utils import embedding_functions

class VectorDBManager:
    def __init__(self, collection_name="documents"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sergeyzh/rubert-tiny-turbo")
        self.collection = self.client.get_or_create_collection(name=collection_name, embedding_function=self.embedding_function)

    def add_document(self, filename, chunks):
        ids = [f"{filename}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename} for _ in chunks]
        self.collection.add(documents=chunks, metadatas=metadatas, ids=ids)

    def search(self, query, n_results=3):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results['documents'][0]  # Возвращаем совпадения
    
    def delete_document(self, source_name):
        self.collection.delete(where={"source": source_name})