#AB #85

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
import requests

def giz2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\giz_02.csv'
        titulos = []
        textos = []
        links = []
        page = requests.get('https://www.giz.de/en/press/press_releases.html', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sites = soup.find_all('section', class_ = 'news-info')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/en/press'):
                new_info = ('https://www.giz.de' + info)
                links.append(new_info)
                
        new_links = getNewInfo(links_base, links)
        
        if(new_links):
            for i in new_links:
                page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                soup2 = BeautifulSoup(page2.text, 'lxml')
                titulo = soup2.find('h1', class_ = 'offset-md-3 col-md-6 col-xs-12').get_text()
                texto = soup2.find('article', class_ = 'article-aside').get_text()
                titulos.append(clean(titulo))
                textos.append(clean(texto))
                    
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'giz_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
                    
    except Exception as e:
        print(e)
        print('Erro em giz2')
        
#giz2('.')  

def giz3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\giz_03.csv'
        titulos = []
        textos = []
        links = ['https://www.giz.de/en/html/about_giz.html']

        page = Request('https://www.giz.de/en/html/about_giz.html', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1').get_text()
        titulos.append(titulo)
        texto = soup.find('div', class_ = 'page').get_text()
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['giz']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'giz_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
            print(e)
            print('Erro em giz3')
        
#giz3('.')   
        
