#AB #103

import bs4
from bs4 import BeautifulSoup
import re
from lxml import etree
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

def rockefeller2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rockefellerfoundation_02.csv'
        titulos = []
        textos = []
        links = []
        link = []
        page_response = requests.get('https://www.rockefellerfoundation.org/news/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')

        sites = soup.find_all('div', class_ = 'post-title')
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
                titulo = soup.find('div', class_ = 'container').find_next('h1').get_text()
                texto = soup.find('div', class_ = 'content-wrapper').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'rockefellerfoundation_')
            df.to_csv(path + filename, index = False)
            
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
    except Exception as e:
        print(e)
        print('Erro em rockefellerfoundation2')  
        
#rockefellerfoundation2('.')
    
def rockefeller3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rockefellerfoundation_03.csv'
        titulos = []
        textos = []
        links = ['https://www.rockefellerfoundation.org/about-us/our-history/', 'https://www.rockefellerfoundation.org/grants/grantmaking-policy/']

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'container').find_next('h1').get_text()
            texto = soup.find('div', class_ = 'content-wrapper').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['rockefellerfoundation']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'rockefellerfoundation_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em rockefellerfoundation3')   
        
#rockefellerfoundation3('.') 

def rockefeller4(path, keywords = 'brazil'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rockefellerfoundation_04.csv'
        titulos = []
        valor = []
        hasBrazil = []
        prj_inst = []
        links = []
        
        page_response = requests.get('https://www.rockefellerfoundation.org/grants/?post_type=grant&grant_active_status=active&keyword=&from_month=&from_year=&to_month=10&to_year=2021').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('div', class_ = 'post-title') 
        soup2 = BeautifulSoup(str(sites), 'lxml')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        for i in soup.find_all('div', attrs={'class': 'post-title'}):
            titulo = i.get_text()
            titulos.append(titulo)
            instituicao = 'Rockefeller Foundation'
            prj_inst.append(instituicao)
            
        for i in soup.find_all('div', attrs={'class': 'post-amount'}):
            value = i.get_text()
            valor.append(value)

        for i in soup.find_all('div', attrs={'class': 'post-description'}):
            text = i.get_text()
            if(findall(keywords, text.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
                
        df = pd.DataFrame()
        df['prj_titulo'] = titulos
        df['link'] = links
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = valor
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'rockefellerfoundation_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em rockefellerfoundation4')   
        
#rockefellerfoundation4('.')
        
        
        
