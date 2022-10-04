#AB #109

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import requests
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def florestal3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\florestal_03.csv'
        titulos = []
        textos = []
        links = ['https://www.florestal.gov.br/desenvolvimento-florestal']
        page_response = requests.get('https://www.florestal.gov.br/desenvolvimento-florestal',verify=False).content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('h1', class_ = 'title').get_text()
        titulos.append(clean(titulo))
        texto = soup.find('div', class_ = 'body').get_text()
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['florestal']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'florestal_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em florestal3')  
        
#florestal3('.')