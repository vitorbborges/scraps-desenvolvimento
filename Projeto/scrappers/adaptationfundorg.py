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

def adaptationfundorg2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\adaptationfundorg_02.csv'
        titulos = []
        textos = []
        links = []
        page_response = requests.get('https://www.adaptation-fund.org/news-and-events/news/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('h2', class_ = 'entry-title')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        #new_links = getNewInfo(links_base, links)

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)

        new_links = getNewInfo(links_base, links)
            
        if(new_links):            
            for i in new_links:
                page_response2 = requests.get(i).content.decode('UTF-8')
                soup3 = BeautifulSoup(page_response2, 'lxml')
                texto = soup3.find('div', class_ = 'post-content').get_text()
                titulo = soup3.find('h1', class_ = 'entry-title').get_text()
                textos.append(clean(texto))
                titulos.append(titulo)
                    
            df = pd.DataFrame()
            df['not_titulo'] = pd.Series(titulos)
            df['link'] = new_links
            df['not_texto'] = pd.Series(textos)
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'adaptationfundorg_')
            df.to_csv(path + filename, index = False)    
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
        
    except Exception as e:
        print(e)
        print('Erro em adaptationfundorg2')
        
#adaptationfundorg2('.')  

def adaptationfundorg3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\adaptationfundorg_03.csv'
        titulos = []
        textos = []
        links = ['https://www.adaptation-fund.org/about/']

        page_response = requests.get('https://www.adaptation-fund.org/about/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('h1').get_text()
        texto = soup.find('div', class_ = 'post-content').get_text()
        textos.append(clean(texto))
        titulos.append(titulo)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['adaptationfundorg']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'adaptationfundorg_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em foundationorg3')
        
#adaptationfundorg3('.')

def adaptationfundorg4(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().year
        filename = '\\adaptationfundorg_04.csv'
        links = []
        titulos = []
        textos = []
        valor = []
        prj_inst = []
        hasBrazil = []
        page_response = requests.get('https://www.adaptation-fund.org/projects-programmes/project-information/projects-photo-view/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        keywords = 'brazil'
        sites = soup.find_all('h2', class_ = 'entry-title')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')


        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('https://www.adaptation-fund.org/project'):
                new_info = info
                links.append(new_info)
                    
        new_links = getNewInfo(links_base, links)
        
        if (new_links):
            for i in new_links:
                page_response = requests.get(i).content.decode('UTF-8')
                soup = BeautifulSoup(page_response, 'lxml')
                titulo = soup.find('h1', class_ = 'entry-title').get_text()
                titulos.append(titulo)
                texto = soup.find('div', class_ = 'project-content').get_text()
                value = soup.find('div', class_ = 'project-terms').find_next('span').find_next('span').get_text()
                valor.append(value)
                if(findall(keywords, texto.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')    
                instituicao = 'adaptationfundorg4'
                prj_inst.append(instituicao)
            
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
                
        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = new_links
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = valor
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'adaptationfundorg4')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em adaptationfundorg4')
        
#adaptationfundorg4('.')
