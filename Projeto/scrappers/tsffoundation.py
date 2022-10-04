#AB #101

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

def tsffoundation2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\tsffoundation_02.csv'
        titulos = []
        textos = []
        links = []
        page = requests.get('https://www.tspa.info/announcements/').text
        soup = BeautifulSoup(page, 'lxml')
        sites = soup.find_all('h2', class_ = 'entry-title')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in links:
                page = requests.get(i).text
                soup3 = BeautifulSoup(page, 'lxml')
                titulo = soup3.find('h1', class_ = 'entry-title').get_text()
                texto = soup3.find('div', class_ = 'entry-content').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
            
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia] * len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'tsffoundation_')
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
    except Exception as e:
        print(e)
        print('Erro em tsffoundation2')
        
#tsffoundation2('.')    

def tsffoundation3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\tsffoundation_03.csv'
        titulos = []
        textos = []
        links = ['https://tsffoundation.org/about/']

        page = requests.get('https://tsffoundation.org/about/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}, verify = False)
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = soup.find('h2', id = 'mission').get_text()
        texto = soup.find('div', class_ = 'entry-content').get_text()
        titulos.append(titulo)
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['tsffoundation'] * len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'tsffoundation_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em tsffoundation3')
        
#tsffoundation3('.')
