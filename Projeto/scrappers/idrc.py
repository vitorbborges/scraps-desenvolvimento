# AB#82
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen

def idrc2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\idrc_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.idrc.ca/en/news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for new in soup.find_all('div', class_='col-sm-12 col-md-4'):
            link = new.find('a')['href']
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('div', class_='col-md-8 layout__region layout__region--main col').find('h1').get_text())
                texto = clean(page_soup.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden field__item').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'idrc_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em idrc2')

def idrc3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.idrc.ca/en/what-we-do', 'https://www.idrc.ca/en/about-idrc']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\idrc_03.csv'
        page = requests.get(links[0]).text
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1', class_='default-page-title idrc-pattern').text)
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto +=p.text
        texto = clean(texto)
        textos.append(texto)

        page = requests.get(links[1]).text
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('article').find('h2').text)
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='layout__region layout__region--main col').get_text())
        textos.append(texto)
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['idrc']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'idrc_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em idrc3')