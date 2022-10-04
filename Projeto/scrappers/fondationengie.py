import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import os
import requests


def fondationengie2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fondationengie_02.csv'
        titulos = []
        textos = []
        links = []
        page = 'https://fondation-engie.com/en/category/news/'
        page_request = requests.get(page).text
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('div', class_ = 't-entry-text-tc single-block-padding')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = (i['href'])
            links.append(info)
            
        fulllist = list(dict.fromkeys(links))
        fulllist.remove('https://fondation-engie.com/en/author/eenov/')
        new_links = getNewInfo(links_base, fulllist)

        if(new_links):
            for i in new_links:
                page_request = requests.get(i).text
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'header-title font-555555 h1').get_text()
                texto = soup.find('div', class_ = 'uncode_text_column').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
        
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'fondationengie_')
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em fondationengie2')
        
#fondationengie2(os.getcwd())
        
def fondationengie3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fondationengie_03.csv'
        titulos = []
        textos = []
        links = ['https://fondation-engie.com/en/the-engie-foundation/', 'https://fondation-engie.com/en/impact-as-an-engine-social-and-environmental/', 'https://fondation-engie.com/en/the-governance-of-the-engie-foundation/']
        
        for i in links:
            page_request = requests.get(i).text
            soup = BeautifulSoup(page_request, 'lxml')
            titulo = soup.find('div', class_ ='heading-text el-text').get_text()
            texto = soup.find('div', class_ = "post-content un-no-sidebar-layout").get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
    
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['fondationengie']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'fondationengie_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em fondationengie3')
        
#fondationengie3(os.getcwd())

def fondationengie4(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = []
        links2 = []
        titulos = []
        valor = []
        hasBrazil = []
        prj_inst = []
        filename = '\\fondationengie_04.csv'
        dia = datetime.today().strftime('%y%m%d') 
        links_base = getInfoBase(pathbase, filename, 'link')
        
        req = 'https://fondation-engie.com/en/our-projects/'
        page = requests.get(req).text
        soup = BeautifulSoup(page, 'lxml') 
        sites = soup.find_all('a', tabindex = '-1')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        keywords = 'brazil'
        
        for i in soup2.findAll('a'):
            info = (i['href'])
            links.append(info)
        
        
        new_links = getNewInfo(links_base, links)
        
        for i in new_links:
            
            page = requests.get(i).text
            soup = BeautifulSoup(page, 'lxml')
            
            if soup.find('title').text != 'Page non trouvée - Fondation ENGIE':
                titulo = soup.find('h1', class_ = 'header-title font-555555 h1').get_text()
                links2.append(i)
                titulos.append(titulo)
                hasbr = clean(soup.find('div', class_ = 'uncode_text_column').text)
                if(findall(keywords, hasbr.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
                instituicao = 'ENGIE Fondation'
                prj_inst.append(instituicao)
                valor.append('Valor não encontrado')
                
            else:
                None
        
        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = links2
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = valor
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'fondationengie_')
        df.to_csv(path+filename, index=False)
                
    except Exception as e:
        print(e)
        print('Erro em fondationengie4')
        
#fondationengie4(os.getcwd())
