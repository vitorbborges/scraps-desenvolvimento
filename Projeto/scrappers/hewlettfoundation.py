#AB #52

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
import os
import requests

def hewlettfoundation3(path):
    try: 
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\hewlettfoundation_03.csv'
        titulos = []
        textos = []
        links = ['https://hewlett.org/about-us/', 'https://hewlett.org/about-us/hewlett-family-and-history/', 'https://hewlett.org/about-us/values-and-policies/', 'https://hewlett.org/about-us/our-programs/', 'https://hewlett.org/about-us/our-policies/']

        for i in links: 
            page_request = requests.get(i).text
            soup = BeautifulSoup(page_request, 'lxml')
            titulo = soup.find('h1', class_ = 'entry-title').get_text()
            texto = soup.find('div', class_ = 'row no-bottom-margin').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
    
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['hewlettfoundation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'hewlettfoundation_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)    
        
    except Exception as e:
        print(e)
        print('Erro em hewlett3')
        
#hewlettfoundation3(os.getcwd())
