#AB #154

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

def sustaintechx3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\sustaintechx_03.csv'
        titulos = []
        titulos2 = []
        textos = []
        textos2 = []
        links = ['https://www.sustaintechx.com/']
        page = requests.get('https://www.sustaintechx.com/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = soup.find('div', id = "comp-kou0t9z01").get_text()
        titulo2 = soup.find('div', id = "comp-kou0taac").get_text()
        texto = soup.find('div', id = "comp-kou0t9za").get_text()
        texto2 = soup.find('div', id = "comp-kou0taag").get_text()
        titulos.append(titulo)
        titulos2.append(titulo2)
        textos.append(clean(texto))
        textos2.append(clean(texto2))

        df = pd.DataFrame()
        df['pol_titulo'] = (titulos + titulos2)
        df['pol_instituicao'] = ['sustaintechx']*len(df.index)
        df['pol_texto'] = (textos + textos2)
        df['link'] = links*2
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'sustaintechx_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em sustaintechx')
        
#sustaintechx3('.')
