#AB #140
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


#notícias em javascript;

def aucklandzoo3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\aucklandzoo_03.csv'
        titulos = []
        textos = []
        links = ['https://www.aucklandzoo.co.nz/about-the-zoo']
        page = Request('https://www.aucklandzoo.co.nz/about-the-zoo', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1', class_ = "title").get_text()
        texto = BeautifulSoup(str(soup.find_all('div', class_ = 'constrain-content')), 'lxml').get_text()
        titulos.append(clean(titulo))
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['aucklandzoo']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'aucklandzoo_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em aucklandzoo3')
        
#aucklandzoo3('.')
