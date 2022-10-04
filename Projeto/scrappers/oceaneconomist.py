#AB #157

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


def oceaneconomist2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/oceaneconomist_02.csv'
        titulos = []
        textos = []
        link_news = []
        links = ['https://ocean.economist.com/blue-finance', 'https://ocean.economist.com/governance', 'https://ocean.economist.com/innovation', 'https://ocean.economist.com/protectors']

        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            sites = soup.find_all('div', class_ = "card-footer")
            soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for link in soup2.find_all('a'):
            info = ('https://ocean.economist.com' + link['href'])
            link_news.append(info)
    
        fulllist = list(dict.fromkeys(link_news))
        new_links = getNewInfo(links_base, fulllist)

        if(new_links):
            for i in new_links:
                page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1').get_text()
                texto = soup.find('div', class_ = "content").get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)

        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'oceaneconomist_')
        df.to_csv(path + filename, index = False)
    
    except Exception as e:
        print(e)
        print('Erro em oceaneconomist2')
        
#oceaneconomist2('.')

def oceaneconomist3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oceaneconomist_03.csv'
        titulos = []
        textos = []
        links = ['https://ocean.economist.com/about']
        page = Request('https://ocean.economist.com/about', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1').get_text()
        texto = soup.find('div', class_ = "about-content").get_text()
        texto2 = soup.find('div', class_ = "css-10delsy").get_text()
        texto3 = soup.find('div', class_ = "css-15m6kg").get_text()
        titulos.append(titulo)
        textos.append(clean(texto + texto2 + texto3))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['oceaneconomist']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'oceaneconomist_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em oceaneconomist3')
        
#oceaneconomist3('.')
