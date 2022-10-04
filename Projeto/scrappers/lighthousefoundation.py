#AB #92

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

def lighthousefoundation3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\lighthousefoundation_03.csv'
        titulos = []
        textos = []
        links = ['https://lighthouse-foundation.org/en/The-Motivation.html', 'https://lighthouse-foundation.org/en/Cooperation.html']

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('h1', class_ = 'page-title').get_text()
            texto = soup.find('section', class_ = 'row pos2 sectiontype2 last').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['lighthousefoundation']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'lighthousefoundation_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em lighthousefoundation3')   
        
#lighthousefoundation3('.') 

def lighthousefoundation4(path, keywords = 'brazil'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\lighthousefoundation_04.csv'
        titulos = []
        texto = []
        valor = []
        hasBrazil = []
        prj_inst = []
        lista = []
        links = []
        instituicao = 'lighthouse foundation'
        page_response = requests.get('https://lighthouse-foundation.org/en/Project-Finder.html').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('div', class_ = 'box-wrapper')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        
        for i in soup2.findAll('a'):
            info = i['href']
            if info.endswith('.html'):
                new_info = ('https://lighthouse-foundation.org/en/' + info)
                lista.append(new_info)
                
        links = pd.unique(lista).tolist()

        for i in links: 
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml') 
            titulo = soup.find('h1', class_ = 'page-title').get_text()
            titulos.append(clean(titulo))
            prj_inst.append(instituicao)
            valor.append('valor não encontrado')
            text = soup.find('div', id = 'content').get_text()
            texto.append(text)
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
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'lighthousefoundation_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em lighthousefoundation4')   
        
#lighthousefoundation4('.')
