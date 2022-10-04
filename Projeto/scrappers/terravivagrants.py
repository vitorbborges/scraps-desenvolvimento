# AB#63
from utilidadesppf import *
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from itertools import compress
import os

def terravivagrants1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\terravivagrants_01.csv'
        sites = ['https://terravivagrants.org/category/cross-cutting/', 'https://terravivagrants.org/category/water-resources/', 'https://terravivagrants.org/category/energy-climate-change/', 'https://terravivagrants.org/category/biodiversity-conservation-wildlife/', 'https://terravivagrants.org/category/agriculture-fisheries-forestry/']
        responses = []
        titles = [] 
        links = [] 
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        dia = datetime.today().strftime("%y%m%d")
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        for site in sites:
            page_request = requests.get(site).content.decode('UTF-8')
            page_soup = BeautifulSoup(page_request, 'lxml')
            for opo in page_soup.find_all('article'):
                try:
                    link = opo.find('a')['href']
                    if(link not in ['https://terravivagrants.org/contact-us/', 'https://terravivagrants.org/links-and-resources/', 'https://terravivagrants.org/photos/', 'https://terravivagrants.org/legal-information/']):
                        links.append(link)
                except:
                    None
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page_request = requests.get(link).content.decode('UTF-8')
                page_soup = BeautifulSoup(page_request, 'lxml')
                page_soup = page_soup.find('article', class_ = 'post')
                titulo = page_soup.find('h1').text
                titles.append(titulo)
                deadline = page_soup.find('p', class_= 'post-meta').text.split('|')[0]
                deadlines.append(deadline)
                text = page_soup.find('span', style = 'font-weight: 400;').text
                texts.append(text)
                if(findall(keywords, text.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
                if len(findall('grant', text.lower())):         
                    types.append('grant')                
                elif len(findall('fellowship', text.lower())):  
                    types.append('fellowship')          
                elif len(findall('scholarship', text.lower())): 
                    types.append('scholarship')                   
                else:
                    types.append('other')
                df = pd.DataFrame()          
            df['opo_titulo'] = titles  
            df['link'] = new_links
            df['opo_texto'] = texts
            df['opo_texto_ele'] = texts
            df['opo_brazil'] = hasBrazil
            df['opo_tipo'] = types
            df['opo_deadline'] = deadlines
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'terravivagrants_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em terravivagrants1')

#terravivagrants1(os.getcwd())

def terravivagrants2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\terravivagrants_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://terravivagrants.org/funding-news/').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('article', class_='page')
        for new in soup.find_all('article'):
            try:
                link = new.find('a')['href']
                links.append(link)
            except:
                None
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                page_soup = page_soup.find('article', class_='post')
                titulo = clean(page_soup.find('h1').get_text())
                texto = clean(page_soup.find_all('p')[1].get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'terravivagrants_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em terravivagrants2')
