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


@router.post("/webdata/")
def get_dataframe(request: WineRequest):
    web_message = webscrapping.get_all()
    if isinstance(web_message, int):
        return {"message": f"Falhou a conexão com o site"}
    database_msg = databases.save_tables_in_db()
    return databases.read_tables_from_db("ProcessaViniferas")
    return {"web_message": f"{web_message}", "database_msg": f"{database_msg}"}

