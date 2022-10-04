#AB #116

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

def waltdisneycompany2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\waltdisneycompany_02.csv'
        titulos = []
        textos = []
        links = []
        page_response = requests.get('https://thewaltdisneycompany.com/news/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('div', class_ = 'entry-meta')
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
                titulo = soup.find('h1', class_ = 'entry-title').get_text()
                titulos.append(titulo)
                texto = soup.find('div', class_ = 'entry-content').get_text()
                textos.append(clean(texto)[:32667])
            
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'waltdisneycompany_')
            df.to_csv(path + filename, index = False) 
            
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
    except Exception as e:
        print(e)
        print('Erro em waltdisneycompany2')  
        
#waltdisneycompany2('.')

def waltdisneycompany3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\waltdisneycompany_03.csv'
        titulos = []
        textos = []
        links = ['https://thewaltdisneycompany.com/about/']
        page_response = requests.get('https://thewaltdisneycompany.com/about/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = clean(soup.find('div', class_ = 'copy').get_text())
        titulos.append(titulo)
        texto = soup.find('div', class_ = 'outer-container site-content').get_text()[:32667]
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['waltdisneycompany']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'waltdisneycompany_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em waltdisneycompany3')  
        
#waltdisneycompany3('.')