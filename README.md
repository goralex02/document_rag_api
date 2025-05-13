# Document RAG API
REST API для извлечения, индексации и семантического поиска текста из документов (PDF, JPG, PNG, DOCX, TXT) 

Это минимально жизнеспособный прототип системы RAG (Retrieval-Augmented Generation), который:

* Принимает файлы: .pdf, .jpg, .png, .txt, .docx
* Извлекает текст
* Разбивает его на фрагменты (чанки)
* Преобразует в эмбеддинги
* Хранит в ChromaDB
* Обеспечивает поиск по запросу пользователя через API

## Функционал
* Загрузка файла (POST /ai-tools/extract-text/)
* Поддержка форматов: PDF, JPG, PNG, TXT, DOCX
* Разбиение текста на чанки
* Сохранение в векторную БД
* Поиск по запросу (GET /ai-tools/search/?q=...)
* Удаление документа (DELETE /ai-tools/delete/?source=...)
* Проверка данных в базе (check_chromadb.py)
* Swagger UI — интерактивная документация API

## Структура
document_rag_api/
│
├── main.py                     # FastAPI сервер
├── extractor.py                # Извлечение текста из PDF/JPG/PNG
│
├── utils/
│   └── chunker.py              # Разделение текста на части
│
├── embeddings/
│   └── embedder.py             # Генерация эмбеддингов
│
├── vector_db/
│   └── db_manager.py           # Работа с ChromaDB
│   └── check_chromadb.py       # Просмотр содержимого ChromaDB
│
├── uploads/                    # Временная папка загрузки
├── chroma_db/                  # Хранилище ChromaDB
│
├── requirements.txt            # Зависимости
├── Dockerfile                  # Для сборки контейнера
└── README.md                   # Этот файл


## Как развернуть через Docker

* git clone https://github.com/goralex02/document-rag-api.git 
* cd document_rag_api
* docker-compose up --build
* Приложение будет доступно по адресу: http://localhost:8000/docs

##  Как использовать API
1. POST /ai-tools/extract-text/ — Загрузка файла
Загружает файл и сохраняет его содержимое в векторную БД.

Поддерживаемые форматы:
.pdf, .jpg, .jpeg, .png, .txt, .docx

2. GET /ai-tools/search/?q=... — Поиск по запросу
Выполняет семантический поиск по запросу пользователя.

3. DELETE /ai-tools/delete/?source=... — Удаление документа
Удаляет все фрагменты, связанные с указанным документом.

## Как проверить данные в ChromaDB

Используй скрипт check_chromadb.py внутри контейнера:
docker exec -it <container_id> python check_chromadb.py
Он покажет:

Сколько всего документов в базе
ID каждого фрагмента
Метаданные (имя файла)
Сам текст (первые 200 символов)
Эмбеддинг (первые 5 значений)
