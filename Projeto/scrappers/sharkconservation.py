# AB#100
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
from urllib.request import Request, urlopen
from datetime import datetime
import shutil
from itertools import compress
def sharkconservation1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\sharkconservation_01.csv'
        titles = [] #
        deadlines = [] #
        texts = [] #
        hasBrazil = [] #
        types = [] #
        dia = datetime.today().strftime("%y%m%d")
        req = Request('https://www.sharkconservationfund.org/small-grant-rfp/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        page_soup = BeautifulSoup(page, 'lxml')
        text = clean(page_soup.find('div', class_='content__content').get_text())
        texts.append(text)
        titulo = clean(page_soup.find('h1', class_='hero__heading').get_text())
        titles.append(titulo)
        if(findall(keywords, text.lower())):
                    hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
        if len(findall('grant', text.lower())):         
            types.append('grant')                
        elif len(findall('fellowship', text.lower())):  
            types.append('fellowship')          
        elif len(findall('scholarship', text.lower())): 
            types.append('scholarship')                   
        else:
            types.append('other')
        deadline = clean(page_soup.find('div', class_='content__content').find_all('p')[-4].get_text())
        deadlines.append(deadline)
        df = pd.DataFrame()          
        df['opo_titulo'] = titles  
        df['link'] = ['https://www.sharkconservationfund.org/small-grant-rfp/']    
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'sharkconservation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em sharkconservation1')

def sharkconservation3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.sharkconservationfund.org/who-we-are/', 'https://www.sharkconservationfund.org/what-we-fund/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\sharkconservation_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='hero__heading').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='content__content').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['sharkconservation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'sharkconservation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em sharkconservation3')

