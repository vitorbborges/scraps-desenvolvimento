# AB#105
from utilidadesppf import getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen


def climateandlandusealliance2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\climateandlandusealliance_02.csv'
        titulos = []
        textos = []
        links = []
        page = requests.get('https://www.climateandlandusealliance.org/updates/').text
        soup = BeautifulSoup(page, 'lxml')
        for new in soup.find_all('div', class_='updates-box'):
            link = new.find('a')['href']
            links.append(link)
            titulo = clean(new.find('h3').get_text())
            texto = clean(new.find('div', class_='updates-content').get_text())
            titulos.append(titulo)
            textos.append(texto)
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'climateandlandusealliance_')
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em climateandlandusealliance2')


def climateandlandusealliance3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.climateandlandusealliance.org/initiatives/global/', 'https://www.climateandlandusealliance.org/initiatives/brazil/', 'https://www.climateandlandusealliance.org/about-us/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\climateandlandusealliance_03.csv'
        for link in links:
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('div', class_='page-intro').find('h1').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='leading-intro-text').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['climateandlandusealliance']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'climateandlandusealliance_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em climateandlandusealliance3')