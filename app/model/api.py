from pydantic import BaseModel
from typing import List



class upload_document_response(BaseModel):
    document_id: str 


class chat_response(BaseModel):
    context: str 
    bot_message: str 
    