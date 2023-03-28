from pydantic import BaseModel
from typing import List

class summary_response(BaseModel):
    bullet_points: List[str]

class document_id(BaseModel):
    id: str
