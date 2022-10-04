import bs4
from bs4 import BeautifulSoup, SoupStrainer
from bs4.dammit import EncodingDetector
import re
from re import findall
import pandas as pd
import requests
from collections import OrderedDict
from urllib.request import Request, urlopen
import urllib
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import os

def humboldt1(path, keywords = 'brazil'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/humboldt_01.csv'
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        tipos = []
        links = []
        texto_elegivel = []
        toggle = True
        links_base = getInfoBase(pathbase, filename, 'link')
        
        i = 1
        
        while toggle == True:
            link = 'https://www.humboldt-foundation.de/en/apply/sponsorship-programmes/programme-search?tx_solr%5Bpage%5D=' + str(i)
            i += 1
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            sites = soup.find_all('div', class_ = 'list__item')
            
            if sites == []:
                toggle = False
                
            else:
                soup2 = BeautifulSoup(str(sites), 'lxml')
                for j in soup2.findAll('a'):
                    info = j['href']
                    if info.startswith('/en/apply/sponsorship-programmes/'):
                        new_info = ('https://www.humboldt-foundation.de' + info)
                        links.append(new_info)
                
        new_links = getNewInfo(links_base, links) 
        if(new_links):
            for link in new_links:
                page = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'headline headline--1 f-w-semibold').get_text()
                titulos.append(titulo)
                texto = soup.find('div', class_ = 'article-content__inner').get_text()
                textos.append(clean(texto)[:32667])
                
                if re.findall(keywords, str(soup).lower()) != []:
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
                if 'grant' in titulo.lower():         
                    tipos.append('grant')                
                elif 'fellowship' in titulo.lower():  
                    tipos.append('fellowship')          
                elif 'scholarship' in titulo.lower(): 
                    tipos.append('scholarship')                   
                else:
                    tipos.append('other')
                deadlines.append('deadlines não encontradas')
        else:
            #print('Não há alteração em novas notícias')
            try:
                shutil.copy(pathbase+filename, '.\\'+dia)
            except:
                None
                
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = new_links
        df['opo_deadline'] = deadlines 
        df['opo_texto'] = textos 
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['opo_brazil'] = hasBrazil
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'humboldt_')
        df['atualizacao'] = [dia]*len(new_links)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em humboldt1')
        
#humboldt1(os.getcwd())
    
def humboldt2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/humboldt_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://www.humboldt-foundation.de/en/explore/newsroom/news', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('article', class_ = 'newsroom-item')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')


        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/en/explore/newsroom/news/'): 
                new_info = ('https://www.humboldt-foundation.de' + info) 
                links.append(new_info)
                
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in new_links:
                page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'headline headline--1 f-w-semibold').get_text()
                n_titulo = titulo.replace('#', ' ')
                #print(n_titulo)
                texto = soup.find('div', class_ = 'article-content').get_text()
                titulos.append(n_titulo)
                textos.append(clean(texto))
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'humboldt_')
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
    except Exception as e:
        print(e)
        print('Erro em humboldt2')
        
#humboldt2(os.getcwd())  

def humboldt3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '/humboldt_03.csv'
        titulos = []
        textos = []
        links = ['https://www.humboldt-foundation.de/en/explore/about-the-humboldt-foundation/about-the-foundation']
        page = Request('https://www.humboldt-foundation.de/en/explore/about-the-humboldt-foundation/about-the-foundation', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1', class_ = 'headline headline--1 f-w-semibold').get_text()
        texto = soup.find('div', class_ = 'article-content').get_text()
        titulos.append(titulo)
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['humboldt']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'humboldt_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em humboldt3')
        
#humboldt3(os.getcwd()) 
