import os
import aiofiles
import uuid


from fastapi import FastAPI, UploadFile, Form, File, BackgroundTasks, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, Response, status
from fastapi.security import HTTPBearer

from model.api import summary_response, document_id
from data_source.pdf import extract_text_from_pdf
from data_source.docx import extract_text_from_docx 
from data_source.pptx import extract_text_from_pptx 
from data_source.web import extract_text_from_web 
from data_source.audio import extract_text_from_audio 
from data_source.youtube import extract_text_from_youtube
from summary_model.cohere import cohere_summarize

app = FastAPI()
DEFAULT_CHUNK_SIZE = 1*1024 * 1024   # 1 megabytes


uploads_dir = os.path.dirname(os.path.realpath(__file__))

origins = [
  "https://app.mindpal.io/",
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

@app.get("/api/id", response_model = document_id)
def get_id():
    
    if not os.path.exists("instance"):
        os.makedirs("instance")

    id = str(uuid.uuid4())
    while id in os.listdir("instance"):
        id = str(uuid.uuid4())
    
    return document_id(id = id)


@app.post("/api/upload-pdf", response_model = summary_response)
async def upload_pdf(background_tasks: BackgroundTasks, id: str, pdf_file: UploadFile = File()):

    if id in os.listdir("instance"):
        return {"error": True, "msg": "the id is already exist"}
    
    os.mkdir("instance/" + id)
    file_name = "instance/" + id + "/" + pdf_file.filename

    async with aiofiles.open(file_name, 'wb') as out_file:
            while chunk := await pdf_file.read(DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)

    pdf_text = extract_text_from_pdf(file_name)

    summary = cohere_summarize(pdf_text)
    background_tasks.add_task(remove_file, file_name)
    return summary_response(bullet_points = summary.split("\n"))


@app.post("/api/upload-pptx", response_model = summary_response)
async def upload_pptx(background_tasks: BackgroundTasks, id: str, pptx_file: UploadFile = File()):

    if id in os.listdir("instance"):
        return {"error": True, "msg": "the id is already exist"}
    
    os.mkdir("instance/" + id)
    file_name = "instance/" + id + "/" + pptx_file.filename

    async with aiofiles.open(file_name, 'wb') as out_file:
            while chunk := await pptx_file.read(DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)

    pptx_text = extract_text_from_pptx(file_name)

    summary = cohere_summarize(pptx_text)
    background_tasks.add_task(remove_file, file_name)
    return summary_response(bullet_points = summary.split("\n"))


@app.post("/api/upload-docx", response_model = summary_response)
async def upload_docx(background_tasks: BackgroundTasks, id: str, dox_file: UploadFile = File()):
        
    if id in os.listdir("instance"):
        return {"error": True, "msg": "the id is already exist"}
        
    os.mkdir("instance/" + id)
    file_name = "instance/" + id + "/" + dox_file.filename
    
    async with aiofiles.open(file_name, 'wb') as out_file:
            while chunk := await dox_file.read(DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    
    docx_text = extract_text_from_docx(file_name)
    
    summary = cohere_summarize(docx_text)
    background_tasks.add_task(remove_file, file_name)
    return summary_response(bullet_points = summary.split("\n"))

@app.post("/api/upload-web", response_model = summary_response)
async def upload_web(url: str = Form(...)):
          
    web_text = extract_text_from_web(url)        
    summary = cohere_summarize(web_text)
    return summary_response(bullet_points = summary.split("\n"))

@app.post("/api/upload-youtube", response_model = summary_response)
async def upload_web(url: str = Form(...)):
          
    web_text = extract_text_from_youtube(url)        
    summary = cohere_summarize(web_text)
    if type(summary) == str:
        return summary_response(bullet_points = summary.split("\n"))
    elif type(summary) == list:
        buller_points = []
        for s in summary:
            buller_points += s.split("\n")
        return summary_response(bullet_points = buller_points)

@app.post("/api/upload-audio", response_model = summary_response)
async def upload_audio(background_tasks: BackgroundTasks, id: str, audio_file: UploadFile = File()):
        
    if id in os.listdir("instance"):
        return {"error": True, "msg": "the id is already exist"}
        
    os.mkdir("instance/" + id)
    file_name = "instance/" + id + "/" + audio_file.filename
    
    async with aiofiles.open(file_name, 'wb') as out_file:
            while chunk := await audio_file.read(DEFAULT_CHUNK_SIZE):
                await out_file.write(chunk)
    
    audio_text = extract_text_from_audio(file_name)
    
    summary = cohere_summarize(audio_text)
    background_tasks.add_task(remove_file, file_name)
    return summary_response(bullet_points = summary.split("\n"))