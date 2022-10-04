#AB #124
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import requests
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo



#usaid1 
#protegido por javascript

def usaid2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\usaid_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://www.usaid.gov/news-information/press-releases/2021', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('span', class_ = 'field-content')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/news-information/'):
                new_info = ('https://www.usaid.gov' + info)
                links.append(new_info)    
                
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in links:
                page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'title').get_text()
                texto = soup.find('div', class_ = 'field field-name-body field-type-text-with-summary field-label-hidden').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'usaid_')
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas notícias!')
            shutil.copy(pathbase+filename, '.\\'+dia) 
                   
    except Exception as e:
        print(e)
        print('Erro em usaid2')
        
#usaid2('.')
        
def usaid3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\usaid_03.csv'
        titulos = []
        textos = []
        links = []

        page = Request('https://www.usaid.gov/who-we-are', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find('ul', class_ = 'menu')
        soup2 = BeautifulSoup(str(sites), 'lxml')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/who-we-are/'):
                new_info = ('https://www.usaid.gov' + info)
                links.append(new_info)
    
        for i in links:
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            titulo = soup3.find('h1', class_ = 'title').get_text()
            texto = soup3.find('div', class_ = 'region-inner region-content-inner').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
    
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['usaid']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'usaid_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em usaid3')
    
#usaid3('.')
