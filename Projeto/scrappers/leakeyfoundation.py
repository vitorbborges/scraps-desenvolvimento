#AB #94

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
import requests
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def leakeyfoundation1(path, keywords= '(brazil|latin america region)'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().year
        filename = '\\leakeyfoundation_01.csv'
        links = ['https://leakeyfoundation.org/grants/research-grants/', 'https://leakeyfoundation.org/grants/baldwins/', 'https://leakeyfoundation.org/grants/francisbrownfund/', 'https://leakeyfoundation.org/grants/fieldschool/', 'https://leakeyfoundation.org/grants/primate-research-fund/']
        titulos = []
        textos = []
        deadlines = []
        hasBrazil = []
        tipos = []
        scrape = []
        texto_elegivel = []

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            scrape.append(str(soup))
            titulo = soup.find('h2', class_ = 'page-title').get_text()
            titulos.append(titulo)
            texto = soup.find('div', class_ = 'entry').get_text()
            textos.append(texto)
            texto_elegivel.append(texto)
            
            if(findall(keywords, texto.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            
            if(findall('grant', texto.lower())):         
                tipos.append('grant')                
            elif(findall('fellowship', texto.lower())):  
                tipos.append('fellowship')          
            elif(findall('scholarship', texto.lower())): 
                tipos.append('scholarship')                   
            else:
                tipos.append('other')
                               
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_texto'] = textos
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'leakeyfoundation_')
        df['atualizacao'] = [dia]*len(links)
        #df['html'] = scrape
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em leakeyfoundation1')
        
#leakeyfoundation1('.')

def leakeyfoundation2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\leakeyfoundation_02.csv'
        titulos = []
        textos = []
        links = []
        page_response = requests.get('https://leakeyfoundation.org/blog/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('div', class_ = 'col-sm-7')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in new_links:
                page_response2 = requests.get(i).content.decode('UTF-8')
                soup3 = BeautifulSoup(page_response2, 'lxml')
                titulo = soup3.find('h2', class_ = 'page-title').get_text()
                texto = soup3.find('div', class_ = 'row maincontent lower').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
            
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'leakeyfoundation_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)    
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
                    
    except Exception as e:
        print(e)
        print('Erro em leakeyfoundation2')
        
#leakeyfoundation2('.')

def leakeyfoundation3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\leakeyfoundation_03.csv'
        titulos = []
        textos = []
        links = ['https://leakeyfoundation.org/about/', 'https://leakeyfoundation.org/about/history/', 'https://leakeyfoundation.org/about/the-leakey-family/']

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('h2', class_ = 'page-title').get_text()
            titulos.append(titulo)
            texto = soup.find('div', class_ = 'entry').get_text()
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['leakeyfoundation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'leakeyfoundation_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em leakeyfoundation3')
        
#leakeyfoundation3('.')
