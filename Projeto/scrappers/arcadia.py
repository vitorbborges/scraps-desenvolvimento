
# AB#55
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import os
from itertools import compress
import shutil
from urllib.request import Request, urlopen
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
#funções:
#retorna uma lista pra preenchimento da coluna de códigos

#retorna os links obtidos na base principal

def getLinksBase(path, filename):
    links_base = []
    path = path + filename
    try:
        dfbase = pd.read_csv(path)
        links_base=(dfbase['link'].tolist())
    except:
        pass
    return links_base
#retorna os links que ainda nao foram lidos
def getNewLinks(links_base, links):
    track =[i in links_base for i in links] 
    new_links_bool = [not bool for bool in track] 
    new_links=(list(compress(links,new_links_bool)))
    return new_links

def arcadia2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\arcadia_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.arcadiafund.org.uk/articles-case-studies?sort-by=&programme=&focus-area=&content-type=news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for card in soup.find_all('div', class_ = 'card'):
            link = card.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = page_soup.find('h2', class_ = 'uk-margin-large-bottom').text
                titulos.append(titulo)
                texto = ''
                for p in page_soup.find_all('p'):
                    texto+=p.text
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'arcadia_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em arcadia2')

#arcadia2(os.getcwd())

def arcadia3(path):
    try:
        titulos = []
        textos = []
        link = 'https://www.arcadiafund.org.uk/how-we-operate'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\arcadia_03.csv'
        page = requests.get(link).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').text)
        titulos.append(titulo)
        texto = clean(soup.find('section', class_='section uk-background-white').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['arcadia']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = [link]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'arcadia_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em arcadia3')

#arcadia3(os.getcwd())

def arcadia4(path, keywords = '(latin american region|brazil)'):
    
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\arcadia_04.csv'
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        page_link = 'https://www.arcadiafund.org.uk/grant-directory?sort-by=title&sort-direction=DESC&programme=&focus-area=&year-awarded=&status=&organisation='
        links = []
        df = []
        
        page = requests.get(page_link).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        
        table = soup.find_all('div', class_="project__title-content")
        table_info = soup.find_all('div', class_="project__text-info")
            
        for i in range(len(table)):
            row = []
            row.append(table[i].find('p', class_="project__title-content-org").text)
            row.append(table[i].find('p', class_="project__title-content-project").text)
            for j in table[i].find_all('p', class_="project__title-content-standard"):
                row.append(j.text)
                
            row.append(clean(table_info[i].find('div', class_="grant__description").text))
            row.append(table_info[i].find('a')['href'])
            links.append(table_info[i].find('a')['href'])
            
            txt = (str(row[1])+str(row[7])).lower()
            if findall(keywords, txt):
                row.append('Y')
            else:
                row.append('N')
            
            df.append(row)
        
        df = pd.DataFrame(df, columns = ['Organization', 'prj_titulo', 'Programme', 'Focus', 'Awarded', 'Status', 'prj_valor', 'Description', 'link', 'prj_brazil'])
        df = df.drop(columns = ['Organization', 'Programme', 'Focus', 'Awarded', 'Status', 'Description'])
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'arcadia_')
        df['atualizacao'] = [dia]*len(df.index)
        df['prj_instituicao'] = ['arcadia']*len(df.index)
        new_links = getNewInfo(links_base, links)
        df = df[df['link'].isin(new_links)]
    
        df.to_csv(path+filename, index=False)
        
        
    except Exception as e:
        print(e)
        print('Erro em arcadia 4')

#arcadia4(os.getcwd())    
