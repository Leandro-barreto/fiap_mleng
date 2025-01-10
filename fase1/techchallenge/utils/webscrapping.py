import requests
import csv
import io
from bs4 import BeautifulSoup

#embrapa_url = "http://vitibrasil.cnpuv.embrapa.br/index.php"
embrapa_url = "http://vitiasdasbrasil.cnpuv.embrapa.br/index.php"

def check_connection(url):
    try:
        re = requests.get(url)
        re.raise_for_status()
    except requests.RequestException as err:
        print("erro")
        return -100
    if re.status_code != 200:
        print("erro")
        return -100
    return re

def get_pages(page):
    pages = {}
    re = check_connection(embrapa_url)
    if isinstance(re, int):
        return re
    soup = BeautifulSoup(re._content)
    for i in soup.find_all('button'):
        texto = i.text
        value = '' if 'value' not in i.attrs.keys() else i.attrs['value']
        pages[texto] = {
            'link': f'{embrapa_url}?opcao={value}',
            'has_subpages': 'No', 
            'sub_pages': {},
            'download_link': {}
            }
    
    return(pages)

def get_subpages(pages):
    for key, values in pages.items():
        re = requests.get(values['link'])
        soup = BeautifulSoup(re._content)
        subpages_dict = {}
        for i in soup.find_all('button'):
            text = i.text
            btn_value = '' if 'value' not in i.attrs.keys() else i.attrs['value']
            if 'subopt' in btn_value:
                print(f"subopt: {btn_value}")
                values['has_subpages'] = 'yes' 
                subpages_dict[text] = f"{values['link']}&subopcao={btn_value}"
        values['sub_pages'] = subpages_dict
    return pages

def detect_delimiter(sample_line):
    """Detecta o delimitador da linha de amostra."""
    if sample_line.count(';') > sample_line.count('\t'):
        return ';'
    else:
        return '\t'

def get_dataframes(pages):
    for key, values in pages.items():
        if key in ['Apresentação', 'Publicação']: continue
        if values['has_subpages'] == 'No':
            re = requests.get(values['link'])
            soup = BeautifulSoup(re._content)
            for link_element in soup.find_all('a', class_='footer_content'):
                if 'href' in link_element.attrs.keys() and 'DOWNLOAD' in link_element.text:
                    values['download_link'] = [embrapa_url.replace('index.php', link_element['href'])]
                    # Fazendo a requisição para baixar o conteúdo do CSV
                    if 'pdf' in link_element['href']: continue
                    response = requests.get(embrapa_url.replace('index.php', link_element['href']))
                    # Checando se o download foi bem-sucedido
                    if response.status_code == 200:
                        # Salvando o conteúdo do arquivo
                        name = link_element['href'].split('/')[-1]
                        csv_content = response.content.decode('utf-8')
                        
                        # Criando um StringIO para processar o conteúdo como um arquivo
                        csv_stream = io.StringIO(csv_content)
                        first_line = csv_stream.readline()
                        
                        # Detectando o delimitador na primeira linha
                        detected_delimiter = detect_delimiter(first_line)
                        
                        # Voltando ao início do stream para ler tudo novamente
                        csv_stream.seek(0)
                        
                        # Lendo o CSV original com o delimitador detectado
                        csv_reader = csv.reader(csv_stream, delimiter=detected_delimiter)
                        
                        # Reescrevendo o CSV com ";" como delimitador
                        with open(f"data/data_{name}", "w", newline='') as file:
                            csv_writer = csv.writer(file, delimiter=';')
                            for row in csv_reader:
                                csv_writer.writerow(row)
                        
                        print("Arquivo CSV baixado, modificado e salvo com sucesso.")
                    else:
                        print(f"Erro ao baixar o arquivo: {response.status_code}")
        else:
            download_link = []
            for subpages in values['sub_pages'].values():
                re = requests.get(subpages)
                soup = BeautifulSoup(re._content)
                for link_element in soup.find_all('a', class_='footer_content'):
                    if 'href' in link_element.attrs.keys() and 'DOWNLOAD' in link_element.text:
                        download_link.append(embrapa_url.replace('index.php', link_element['href']))
                        # Fazendo a requisição para baixar o conteúdo do CSV
                        if 'pdf' in link_element['href']: continue
                        response = requests.get(embrapa_url.replace('index.php', link_element['href']))
                        # Checando se o download foi bem-sucedido
                        if response.status_code == 200:
                            # Salvando o conteúdo do arquivo
                            name = link_element['href'].split('/')[-1]
                            csv_content = response.content.decode('utf-8')
                            
                            # Criando um StringIO para processar o conteúdo como um arquivo
                            csv_stream = io.StringIO(csv_content)
                            first_line = csv_stream.readline()
                            
                            # Detectando o delimitador na primeira linha
                            detected_delimiter = detect_delimiter(first_line)
                            
                            # Voltando ao início do stream para ler tudo novamente
                            csv_stream.seek(0)
                            
                            # Lendo o CSV original com o delimitador detectado
                            csv_reader = csv.reader(csv_stream, delimiter=detected_delimiter)
                            
                            # Reescrevendo o CSV com ";" como delimitador
                            with open(f"data/data_{name}", "w", newline='') as file:
                                csv_writer = csv.writer(file, delimiter=';')
                                for row in csv_reader:
                                    csv_writer.writerow(row)
                            
                            print(f"Arquivo {name} CSV baixado, modificado e salvo com sucesso 1.")
                        else:
                            print(f"Erro ao baixar o arquivo: {response.status_code}")
            values['download_link'] = download_link

def get_all():
    pages = get_pages(embrapa_url)
    if isinstance(pages, int):
        return pages
    pages = get_subpages(pages)
    get_dataframes(pages)
    return {'message' : 'Salvando as tabelas em base local'}
