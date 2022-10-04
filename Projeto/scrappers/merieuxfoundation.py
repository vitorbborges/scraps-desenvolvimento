#AB #128

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

def merieuxfoundation2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\merieuxfoundation_02.csv'
        titulos = []
        textos = []
        links = []
        page = requests.get('https://www.fondation-merieux.org/en/news/').text
        soup = BeautifulSoup(page, 'lxml')
        sites = soup.find_all('a', class_ = 'block-news')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in new_links:
                page2 = requests.get(i).text
                soup2 = BeautifulSoup(page2, 'lxml')
                titulo = soup2.find('h1', class_ = 'title-heading').get_text()
                texto = soup2.find('div', class_ = 'content-ajax').get_text()
                titulos.append(clean(titulo))
                textos.append(clean(texto))
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'merieuxfoundation_')
            df.to_csv(path + filename, index = False)
            
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
        
    except Exception as e:
        print(e)
        print('Erro em merieuxfoundation2')
        
#merieuxfoundation2('.')

def merieuxfoundation3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\merieuxfoundation_03.csv'
        titulos = []
        textos = []
        links = ['https://www.fondation-merieux.org/en/who-we-are/', 'https://www.fondation-merieux.org/en/what-we-do/']

        for i in links:
            page = requests.get(i).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = soup.find('h1', class_ = 'title-heading').get_text()
            texto = soup.find('div', class_ = 'content-ajax').get_text()
            titulos.append(clean(titulo))
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['merieuxfoundation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'merieuxfoundation_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em merieuxfoundation3')
        
#merieuxfoundation3('.')
