import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
import requests
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def lcaof3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\lcaof_03.csv'
        titulos = []
        textos = []
        links = ['https://www.lcaof.org/history', 'https://www.lcaof.org/mission']

        for i in links:
            page = requests.get(i).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = soup.find('h2', style = 'white-space:pre-wrap;').get_text()
            texto = soup.find('div', class_ = 'sqs-block html-block sqs-block-html').get_text()
            titulos.append(titulo)
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['lcaof']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'lcaof')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
            
    except Exception as e:
        print(e)
        print('Erro em lcaof3')
        
#lcaof3('.')
    
    
