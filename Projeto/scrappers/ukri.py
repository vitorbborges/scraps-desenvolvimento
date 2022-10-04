#AB 

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

def ukri2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\ukri_02.csv'
        titulos = []
        textos = []
        links = []
        links2 = []
        page = Request('https://www.ukri.org/news/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('a', class_ = 'ukri-linked-panel__link')
        sites2 = soup.find_all('div', class_ = '')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        soup3 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')
        
        links.append(soup.find('a', class_='ukri-linked-panel__link')['href'])
        for i in soup2.findAll('a'):
            info = (i['href'])
            links.append(info)
        
        new_links = getNewInfo(links_base, links)
        
        if(new_links):
            for link in new_links:
                page = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'govuk-heading-xl main-area__page-title').get_text()
                texto = soup.find('div', class_ = 'entry-content').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
                
        else:
            #print('Não há alteração em novas notícias')
            try:
                shutil.copy(pathbase+filename, '.\\'+dia)
            except:
                None
        
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'ukri_')
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em ukri2')
        
#ukri2('.')

def ukri3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '//ukri_03.csv'
        titulos = []
        textos = []
        links = ['https://www.ukri.org/about-us/who-we-are/', 'https://www.ukri.org/about-us/what-we-do/','https://www.ukri.org/about-us/who-we-fund/', 'https://www.ukri.org/about-us/our-structure/', 'https://www.ukri.org/about-us/policies-standards-and-data/corporate-policies-and-standards/', 'https://www.ukri.org/about-us/policies-standards-and-data/good-research-resource-hub/', 'https://www.ukri.org/about-us/policies-standards-and-data/data-collection/']
        
        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            titulo = soup.find('h1', class_ = "govuk-heading-xl main-area__page-title").get_text()
            texto = BeautifulSoup(str(soup.find('div', class_ = "entry-content")), 'lxml').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
    
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['ukri']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'ukri_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    
    except Exception as e:
        print(e)
        print('Erro em ukri3')
        
#ukri3('.')
