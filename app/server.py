import os
import aiofiles
import openai
import re

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from model.api import upload_document_response, chat_response
from data_source.pdf import extract_text_from_pdf
from data_source.docx import extract_text_from_docx 
from data_source.pptx import extract_text_from_pptx 
from data_source.web import extract_text_from_web 
from data_source.audio import extract_text_from_audio 
from data_source.youtube import extract_text_from_youtube
from utils.unique_id import generate_uuid 
from utils.text_splitter import split_text
from vector_database.pinecone import upload_document, init_pinecone_index, get_context
from embedding.cohere import init_cohere_embedding

app = FastAPI()
DEFAULT_CHUNK_SIZE = 2*1024 * 1024   # 1 megabytes


uploads_dir = os.path.dirname(os.path.realpath(__file__))

origins = [
  "https://chat.mindpal.space/",
  "http://localhost:3000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

def remove_file(file_path: str):
    os.remove(file_path)

@app.on_event("startup")
async def startup():
    load_dotenv()
    global vector_database
    vector_database =  init_pinecone_index(PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY"),
                                           environment = "us-central1-gcp",
                                           index_name= "docify",
                                           dimension= 1024,
                                           metric="cosine")
    global embedding 
    embedding = init_cohere_embedding(COHERE_API_KEY = os.environ.get("COHERE_API_KEY"))
    openai.api_key = os.environ.get("OPENAI_API_KEY")



@app.post("/api/upload-file", response_model = upload_document_response)
async def upload_file(background_tasks: BackgroundTasks, doc_file: UploadFile = File()):

    document_id = generate_uuid()
    if not os.path.exists("instance"):
            os.makedirs("instance")

    file_name =  "instance/" + document_id + "/" + doc_file.filename

    os.mkdir("instance/" + document_id)

    async with aiofiles.open(file_name, 'wb') as out_file:
            while chunk := await doc_file.read(DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)

    extracted_text = extract_text_from_file(file_name)
    chunks = split_text(extracted_text)
    print(len(chunks))
    upload_document(embedding, vector_database, chunks, document_id, batch_size = 64)

    background_tasks.add_task(remove_file, file_name)
    return upload_document_response(document_id = document_id)

def extract_text_from_file(file_name: str):
    file_type = file_name.split(".")[-1]
    if file_type == "pdf":
        return extract_text_from_pdf(file_name)
    elif file_type == "docx":
        return extract_text_from_docx(file_name)
    elif file_type == "pptx":
        return extract_text_from_pptx(file_name)
    elif file_type == "mp3":
        return extract_text_from_audio(file_name)
    elif file_type == "wav":
        return extract_text_from_audio(file_name)
    elif file_type == "webm":
        return extract_text_from_audio(file_name)
    elif file_type == "mp4":
        return extract_text_from_audio(file_name)

@app.post("/api/upload-url", response_model = upload_document_response)
async def upload_url(url: str = Form()):

    document_id = generate_uuid()

    if is_youtube_url(url):
        extracted_text = extract_text_from_youtube(url)
    else:
        extracted_text = extract_text_from_web(url)
    chunks = split_text(extracted_text)
    print(len(chunks))
    upload_document(embedding, vector_database, chunks, document_id, batch_size = 64)

    return upload_document_response(document_id = document_id)

def is_youtube_url(url):
    youtube_regex = r"(http(s)?:\/\/)?(w{3}\.)?youtu(be\.com|\.be)\/.+"
    return bool(re.match(youtube_regex, url))


@app.get("/api/chat", response_model = chat_response)
async def chat(document_id: str ,
                user_message: str ):
    context = get_context(embedding, document_id, vector_database, user_message)
    messages=[{"role": "system", "content": "you are a helpful assistant"}]
    user_message = f"given the context: {context}, answer the follwing question: {user_message}"
    bot_message = chatbot_response(user_message, messages)
    return chat_response(context = context, bot_message = bot_message)

def chatbot_response(msg, messages):
    item =  {"role": "user", "content": msg}
    messages.append(item)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, temperature = 0, max_tokens = 100)
    return str(response['choices'][0]['message']['content'])
