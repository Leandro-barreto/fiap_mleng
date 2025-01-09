from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..utils import webscrapping
from ..utils import database

router = APIRouter()

class WineRequest(BaseModel):
    page: str
    subpage: str
    api_key: str


@router.post("/web_data/")
def get_dataframe(WineRequest):
    webscrapping.get_all()
    
