#AB #83

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import requests

def kfw3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\kfw_03.csv'
        titulos = []
        textos = []
        links = ['https://www.kfw.de/About-KfW/']
        for link in links:
            req = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(req.text, 'lxml')
            titulo = clean(soup.find('div', class_ = 'u-margin-3').get_text())
            texto1 = soup.find('div', class_ = 'text-image').get_text()
            texto2 = soup.find('div', class_ = 'text-image__image-container').get_text()
            titulos.append(titulo)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['kfw']*len(df.index)
        df['pol_texto'] = clean(texto1 + texto2)
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'kfw_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em kfw3')
        
#kfw3('.')