#AB #77

import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from re import findall
import requests
from datetime import datetime
from itertools import compress
import shutil
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import urllib
from urllib.request import Request, urlopen

def forskningsradet1(path, keywords = 'brazil'):
    try:
        filename = '\\forskningsradet_01.csv'
        dia = datetime.today().strftime('%y%m%d')
        links = []
        textos = []
        titulos = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        page_response = requests.get('https://www.forskningsradet.no/en/call-for-proposals/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')

        for new in soup.find_all('div', class_ = "date-card__grid date-card__grid-primary"):

            for i in new.find('a'):
                links.append('https://www.forskningsradet.no' + new.find('a')['href'])
                #print('https://www.forskningsradet.no' + new.find('a')['href'])
                
            #len(links)
            for i in links:
                req = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}) 
                page_request = urlopen(req).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = "proposal-page--heading").get_text()
                texto = soup.find('div', class_ = "content-container proposal-page--description").get_text()
                if soup.find('div', class_ = "tab-content-section") is not None:
                    texto2 = soup.find('div', class_ = "tab-content-section").get_text()
                else:
                    texto2 = ''
                deadline = BeautifulSoup(str(soup.find_all('span', class_ = 'proposal-data--value-text')), 'lxml').get_text()
                texto3 = (texto + texto2)
                gtit = texto3.lower()
                if ('grant' in gtit):
                    tipos.append('grant')
                elif ('fellowship' in gtit):
                    tipos.append('fellowship')
                elif ('scholarship' in gtit):
                    tipos.append('scholarship')
                elif ('award' in gtit):
                    tipos.append('award')
                else:
                    tipos.append('other')
                    
                if keywords in (texto3):
                    #print("Y") 
                    var = "Y"
                else:
                    #print("N")
                    var = "N"
                elegibilidade.append(var)
                deadlines.append((deadline.split(',')[1]))
                titulos.append(titulo)
                textos.append(clean(texto + texto2))
                texto_elegivel.append(clean(texto + texto2))
                scrape.append(str(soup))

        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_deadline'] = deadlines
        df['opo_texto'] = textos
        df['opo_texto_ele'] = texto_elegivel
        df['opo_tipo'] = tipos
        df['opo_brazil'] = elegibilidade
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'forskningsradet_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em forskningsradet1')
        
#forskningsradet1('.')

#notícias em javascript;

def forskningsradet3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '/forskningsradet_03.csv'
        links = ['https://www.forskningsradet.no/en/about-the-research-council/what-we-do/' , 'https://www.forskningsradet.no/en/apply-for-funding/international-funding/']
        titulos = []
        textos = []
        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            titulo = soup.find('h1', class_ = "heading").get_text()
            texto = soup.find('div', class_ = "content-container content-area-page--content").get_text()
            titulos.append(titulo)
            textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['forskningsradet']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'forkningsradet_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em forkningsradet3')
        
#forskningsradet3('.')
    
    
