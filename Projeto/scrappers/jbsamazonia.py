# AB#40
# AB#148
from tkinter.ttk import Style
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList
from re import findall
from utilidadesppf import getInfoBase, getNewInfo, clean
import shutil
from urllib.request import Request, urlopen


def jbsamazonia3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\jbsamazonia_03.csv'
        titulos = []
        textos = []
        links = ['https://fundojbsamazonia.org/en/about-us/how-we-operate/#', 'https://fundojbsamazonia.org/en/about-us/the-fund/', 'https://fundojbsamazonia.org/en/about-us/governance-and-transparency/', 'https://fundojbsamazonia.org/en/about-us/about-jbs/', 'https://fundojbsamazonia.org/en/about-us/about-the-biome/']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('header', class_ = 'header_interna').find('h1').get_text()
            #print(titulo)
            texto = soup.find('div', class_ = 'section mcb-section').get_text()
            #print(texto)
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['jbsamazonia']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'jbsamazonia_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em jbsamazonia3')   

def jbsamazonia4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\jbsamazonia_04.csv'
        titulos = []
        links = ['https://fundojbsamazonia.org/en/projects/supported-projects/']
        paginas = []
        values = ['null']
        links_base = getInfoBase(pathbase, filename, 'link')
        link_page = 'https://fundojbsamazonia.org/en/projects/supported-projects/'
        link_page2 = []

        page = requests.get(link_page).content.decode('utf-8')
        page_soup = BeautifulSoup(page, 'lxml')
        sopa = page_soup.find('div', class_='sections_group')
      

        for i in sopa.find_all('div', class_='nome_projeto_apoiado'):
            #page = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            title = i.text
            titulos.append(clean(title))
            #print(title)
            link = 'https://fundojbsamazonia.org/en/projects/supported-projects/'
            links.append(link)
            #print(titulos)          
        df = pd.DataFrame()
        df['prj_titulo'] = titulos
        df['link'] = pd.Series(links) 
        df['prj_instituicao'] = ['jbsamazonia']*len(df.index)
        df['prj_valor'] = pd.Series(values)
        df['prj_brazil'] = ['Y']*len(df.index)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'jbsamazonia_')
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em jbsamazonia4')
