# AB#13
from datetime import datetime
import requests
import shutil
import bs4
from bs4 import BeautifulSoup
import re
from utilidadesppf import getNewInfo, getCodList, getInfoBase, clean
import pandas as pd
from urllib.request import Request, urlopen
import os

def iadb2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\iadb_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.iadb.org/en/press-room').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        card = soup.find('div', class_ = 'pr-news-container')
        print(card)
        #print('carta', card.prettify())
        #for card in soup.find_all('div', class_ = 'pb-2 col-sm-12 col-xs-12 px-0'):
            #print('Encontrou = ', card.prettify())
            #link = card.find('a')['href']
           # links.append('https://www.iadb.org/' + link)
           # print(link)
        new_links = getNewInfo(links_base, links)
        print(new_links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = page_soup.find('div', class_= 'news-title').text
                titulos.append(titulo)
                texto = ''
                text_area = page_soup.find('div', class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')
                for p in text_area.find_all('p'):
                    texto+=p.text
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'iadb_')
            df.to_csv(path+filename, index=False)
        else:
            try:
                #print('Não há alteração em novas oportunidades')
                shutil.copy(pathbase+filename, '.\\'+dia)
            except:
                None
    except Exception as e:
        print(e)
        print('Erro em iadb2')


def iadb3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.iadb.org/en/about-us/integrity-and-accountability-idb', 'https://www.iadb.org/en/about-us/oversight', 'https://www.iadb.org/en/about-us/overview', 'https://www.iadb.org/en/about-us/how-are-we-organized']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\iadb_03.csv'
        for link in links:
            page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            soup = soup.find('div', class_='node__content')
            if(soup.find('h2') is not None):
                titulo = clean(soup.find('h2').get_text())
            else:
                titulo = 'How are we organized'
            titulos.append(titulo)
            texto = clean(soup.get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['iadb']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'iadb_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em iadb3')


def iadb4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\iadb_04.csv'
        titulos = []
        links = []
        values = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_page = 'https://www.iadb.org/en/projects-search?country=BR&sector=&status=&query=&page=0'
        for i in range(1):
            page = requests.get(link_page).content.decode('utf-8')
            page_soup = BeautifulSoup(page, 'lxml')
            for proj in page_soup.find('tbody').find_all('tr'):
                link = proj.find('a')['href']
                links.append('https://www.iadb.org' + link)
                link_page = 'https://www.iadb.org/en/projects-search' + page_soup.find('li', class_= 'pager__item pager__item--next').find('a')['href']
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                title = page_soup.find('h1', class_ = 'project-title').text
                titulos.append(title)
                valor = page_soup.find('div', class_= 'project-information project-section').find('span', class_ = 'project-field-data').text
                valor = re.sub(' ', '', valor)
                values.append(clean(valor))             
            df = pd.DataFrame()
            df['prj_titulo'] = titulos 
            df['link'] = new_links 
            df['prj_instituicao'] = ['IADB']*len(df.index)
            df['prj_valor'] = values
            df['prj_brazil'] = ['Y']*len(df.index)
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'iadb_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em iadb4')
        
#iadb2(os.getcwd())
