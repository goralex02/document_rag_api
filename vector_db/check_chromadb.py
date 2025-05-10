import chromadb
from chromadb.utils import embedding_functions

# Укажи ту же модель, что используется в приложении
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="sergeyzh/rubert-tiny-turbo")

# Подключаемся к существующей базе
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="documents", embedding_function=sentence_transformer_ef)

# Получаем все записи из коллекции
data = collection.get(include=["metadatas", "documents", "embeddings"])

# Выводим информацию
print("Количество документов в базе:", len(data["ids"]))
for i in range(len(data["ids"])):
    print(f"\nID: {data['ids'][i]}")
    print(f"Метаданные: {data['metadatas'][i]}")
    print(f"Фрагмент текста: {data['documents'][i][:200]}...")  # Первые 200 символов
    print(f"Эмбеддинг (первые 5 значений): {data['embeddings'][i][:5]}...")