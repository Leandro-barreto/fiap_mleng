from fastapi import APIRouter
from pydantic import BaseModel
from services import webscrapping
from services import databases
import json

router = APIRouter()

class WineRequest(BaseModel):
    page: str = "Comercializacao"
    ano_min: int = 2010
    ano_max: int = 2023
    api_key: str = ""

def read_pages():
    file_path = 'config/pages.json'

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

def get_tables(request: WineRequest):
    ano_min = request.ano_min
    ano_max = request.ano_max
    pages_dict = read_pages()
    dict_return = {}
    dict_return['msg'] = "Retornando todos os dados salvos na Base Local"
    if request.page == "All":
        dict_return['dado'] = databases.return_all_tables(ano_min=ano_min, ano_max=ano_max)
    elif request.page in pages_dict.keys():
        table_prefix = pages_dict[request.page]["prefix"]
        has_subpages = pages_dict[request.page]["has_subpages"]
        dict_return['msg'] = f"Retorando tabela {request.page}"
        dict_return['dado'] = {
            request.page: databases.select_tables(table_prefix, ano_min=ano_min, ano_max=ano_max, sub_pages=has_subpages)
            }
    else:
        dict_return['msg'] = "Retorando tabela default: Comercio"
        dict_return['dado'] = databases.read_tables_from_db("Comercio", json_type=True, ano_min=ano_min, ano_max=ano_max)
        
    return dict_return


@router.post("/webdata/")
def get_dataframe(request: WineRequest):
    dict_return = {}
    web_message = webscrapping.get_all()
    if isinstance(web_message, int):
        dict_return['msg_conexao']  = f"Falha da conexão com o site, retornando dados salvos na DB"
    else:
        databases.save_tables_in_db()
    dict_return['web_msg'] = web_message
    dict_return['dados_locais'] = get_tables(request)
    return dict_return

