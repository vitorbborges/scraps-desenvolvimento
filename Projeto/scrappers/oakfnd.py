# AB#49
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from itertools import compress
from urllib.request import Request, urlopen

# SITE PROTEGIDO POR JAVASCRIPT

def oakfnd1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\oakfnd_01.csv'
        titles = [] 
        links = ['https://oakfnd.org/grant-making/'] #
        texts = [] 
        hasBrazil = [] 
        deadl=[]
        types = ['grant'] 
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime("%y"))
        for link in links:

            page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_soup = BeautifulSoup(page.text, 'lxml')
            # print(page_soup)
            titulo = page_soup.find('h1').text
            # print(titulo)
            titles.append(titulo.strip())
            text_area = clean(page_soup.find('div', class_= 'block block--text').text)
            # print(text_area)
            texts.append(text_area)
            if(findall(keywords, text_area.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')

            deadl.append('31/12/'+ano)


        df = pd.DataFrame()          
        df['opo_titulo'] = titles  
        df['link'] = links
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadl
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'oakfnd_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em oakfnd1')

# oakfnd1('.')

def oakfnd3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oakfnd_03.csv'
        titulos = []
        textos = []
        links = ['https://oakfnd.org/values-mission-history/', 'https://oakfnd.org/values-mission-history/cbod/', 'https://oakfnd.org/values-mission-history/child-safeguarding/']

        for i in links:
            # page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            # page_request = urlopen(page).read()

            page = requests.get(i).content.decode('utf-8')
            soup = BeautifulSoup(page, 'lxml')
            try:
                titulo = soup.find('h1').get_text()
            except Exception as e:
                titulo = soup.find('h2').get_text() 
            texto = soup.find('div', class_ = 'block block--text').get_text()
            titulos.append(clean(titulo))
            textos.append(clean(texto))
    
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['oakfnd'] * len(df.index)
        df['pol_texto'] = textos 
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'oakfnd_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em oakfnd3')
        
#oakfnd3('.')