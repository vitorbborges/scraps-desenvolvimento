#AB #118

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

def mitsubishicorp2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\mitsubishicorp_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://www.mitsubishicorp.com/jp/en/pr/archive/2021/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('section', class_ = 'prTop')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/jp/en/pr/archive/2021/'):
                new_info = ('https://www.mitsubishicorp.com' + info)
                links.append(new_info)
        
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in links:
                page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = clean(soup.find('h2', class_ = 'prPageTitle').get_text())
                texto = soup.find('div', class_ = 'inner').get_text()
                titulos.append(clean(titulo))
                textos.append(clean(texto))
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia] * len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'mitsubishicorp_')
            df.to_csv(path + filename, index = False)        
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
                
        
    except Exception as e:
        print(e)
        print('Erro em mitsubishicorp2')
        
#mitsubishicorp2('.')

def mitsubishicorp3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\mitsubishicorp_03.csv'
        titulos = []
        textos = []
        links = ['https://www.mitsubishicorp.com/jp/en/about/']

        page = Request('https://www.mitsubishicorp.com/jp/en/about/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1', id = 'pageTitle').get_text()
        texto = soup.find('div', class_ = 'pageTitleLead').get_text()
        titulos.append(clean(titulo))
        textos.append(clean(texto))
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['mitsubishicorp']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'mitsubishicorp_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em mitsubishicorp3')
        
#mitsubishicorp3('.')
