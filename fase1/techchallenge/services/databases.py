import sqlite3
import pandas as pd
import glob
import numpy as np
import io


def conectar_sqlite():
    """ create a database connection to an SQLite database """
    conn = None
    filename = "TechChallenge01.db"
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            return conn
            

def write_table(conn, file, table_name):
    # read file
    df = pd.read_csv(file, sep=';')
    # write the data to a sqlite table
    df.to_sql(table_name, conn, if_exists='replace', index = False)

def get_files():
    extension = 'csv'
    result = glob.glob(f'data/*.{extension}')
    print(result)
    return(result)

def save_tables_in_db():
    conn = conectar_sqlite()
    for i in get_files():
        write_table(conn=conn, file=i, table_name=i.replace("data/data_", "").replace(".csv", ""))
    return "Tabelas salvas"
    
def read_tables_from_db(table, ano_min=2010, ano_max=2020, json_type=True):
    conn = conectar_sqlite()
    df = pd.read_sql(f"Select * from {table}", conn)
    lista_anos = [str(ano) for ano in range(ano_min, ano_max + 1)]
    cols = [col for col in df.columns if col[:4] in lista_anos]
    colunas_nao_anos = [col for col in df.columns if not col.replace('.', '').isdigit()]
    df = df[colunas_nao_anos + cols].copy()
    if json_type:
        print(  table)
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True)

        return df.to_dict()
    return df

def select_tables(table_prefix, ano_min, ano_max, sub_pages=False):
    if sub_pages == 'Yes':
        subpage_list = [name for name in get_files() if table_prefix in name]
        dict_return = {}
        for i in subpage_list:
            print(i)
            table_return = read_tables_from_db(i.replace("data/data_", "").replace(".csv", ""), ano_min=ano_min, ano_max=ano_max)
            dict_return[i.replace("data/data_", "").replace(".csv", "")] = table_return
        return dict_return
    return read_tables_from_db(table_prefix, ano_min=ano_min, ano_max=ano_max)


def return_all_tables(ano_min, ano_max):
    dict_return = {}
    for file in get_files():
        table_return = read_tables_from_db(file.replace("data/data_", "").replace(".csv", ""), ano_min=ano_min, ano_max=ano_max)
        dict_return[file.replace("data/data_", "").replace(".csv", "")] = table_return
    return dict_return
