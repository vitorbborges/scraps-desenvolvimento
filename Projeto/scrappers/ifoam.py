# AB#137
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
import os

def ifoam2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\ifoam_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.ifoam.bio/news-and-press').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='row grid grid--card-layout')
        for new in soup.find_all('a'):
            link = 'https://www.ifoam.bio/' + new['href']
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('div', class_='d-flex flex-column pb-2').get_text())
                texto = clean(page_soup.find('div', class_='section__bg col-12 px-0 py-4').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'ifoam_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em ifoam2')

#ifoam2(os.getcwd())

def ifoam3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.ifoam.bio/our-work/where/latin-america', 'https://www.ifoam.bio/why-organic', 'https://www.ifoam.bio/about-us']
        filename = '\\ifoam_03.csv'
        dia = datetime.today().strftime('%y%m%d')
        req = Request(links[0], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h2', class_='glide-slide__title text-white mb-4').text
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='section__bg col-12 px-0 col-md-8 py-4').get_text())
        textos.append(texto)

        req = Request(links[1], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h1', class_='bg-color-title-image__title text-left').text
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='section__bg col-12 px-0 col-md-8 py-4').get_text())
        textos.append(texto)

        req = Request(links[2], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h2', class_='glide-slide__title text-white mb-4').text
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='section__bg col-12 px-0 col-md-8 py-4').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['ifoam']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'ifoam_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em ifoam3')
        
#ifoam3(os.getcwd())
