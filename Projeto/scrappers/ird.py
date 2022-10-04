#AB #121

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import requests
import numpy as np
import pandas as pd
import urllib
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

#irdfr2

def irdfr2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\irdfr_02.csv'
        titulos = []
        textos = []
        links = []
        page_response = requests.get('https://en.ird.fr/sections/release-press-office').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('div', class_ = 'results__list')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        new_links = getNewInfo(links_base, links)
        
        if(new_links):
            for i in new_links:
                page_response = requests.get(i).content.decode('UTF-8')
                soup = BeautifulSoup(page_response, 'lxml')
                titulo = soup.find('li', class_ = 'breadcrumb__link').find_next('span').get_text()
                titulos.append(titulo)
                texto = soup.find('div', class_ = 'page__content-main article-content').get_text()
                textos.append(clean(texto))
            
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'irdfr_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)   
        else:
            #print('Não há alteração em novas notícias')
            try:
                shutil.copy(pathbase+filename, '.\\'+dia)
            except:
                None
            
    except Exception as e:
        print(e)
        print('Erro em irdfr2')  
        
#irdfr2('.')

def irdfr3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\irdfr_03.csv'
        titulos = []
        textos = []
        links = ['https://en.ird.fr/our-identity', 'https://en.ird.fr/ird-france-and-worldwide']

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'title-wrapper').get_text()
            texto = soup.find('div', class_ = 'page__content-main article-content').get_text()
            titulos.append(clean(titulo))
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['irdfr']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'irdfr_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em irdfr3')   
        
#irdfr3('.') 
