from sentence_transformers import SentenceTransformer

# Загружаем русскоязычную модель
model = SentenceTransformer('sergeyzh/rubert-tiny-turbo')

def get_embeddings(texts):
    return model.encode(texts, convert_to_tensor=False).tolist()