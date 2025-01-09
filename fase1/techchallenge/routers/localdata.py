from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from utils import webscrapping
from utils import databases

router = APIRouter()

class WineRequest(BaseModel):
    page: str
    subpage: str
    api_key: str


@router.post("/localdata/")
def get_dataframe(WineRequest):
    webscrapping.get_all()
    
