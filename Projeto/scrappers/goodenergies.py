#AB #91
import requests
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def goodenergies3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\goodenergies_03.csv'
        titulos = []
        titulos2 = []
        textos = []
        textos2 = []
        links = ['https://www.goodenergies.org/who-we-are/about-us/#', 'https://www.goodenergies.org/what-we-do/our-work/', 'https://www.goodenergies.org/who-we-are/governance-and-team/', 'https://www.goodenergies.org/what-we-do/energy/']
        links2 = ['https://www.goodenergies.org/what-we-do/forests/'] 

        for i in links:
            page = requests.get(i).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = soup.find('span', style = 'color: #123e85;').get_text()
            texto = soup.find('div', class_ = 'panel-layout').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))

        page2 = requests.get('https://www.goodenergies.org/what-we-do/forests/').text
        soup2 = BeautifulSoup(page2, 'lxml')
        titulo2 = soup2.find('span', style = 'color: #339966;').get_text()
        texto2 = soup2.find('article', class_ = 'post page').get_text()
        titulos2.append(titulo2)
        textos2.append(clean(texto2))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos + titulos2 
        df['pol_instituicao'] = ['goodenergies'] * len(df.index)
        df['pol_texto'] = textos + textos2
        df['link'] =  links + links2
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'goodenergies_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em goodenergies3')
