import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
import numpy as np
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def govmma2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\govmma_02.csv'
        titulos = []
        textos = []
        links = []
        lista = []
        page = Request('https://www.gov.br/mma/pt-br/assuntos/noticias', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('article', class_ = 'tileItem visualIEFloatFix tile-collective-nitf-content')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')


        for i in soup2.find_all('a'):
            info = (i['href'])
            if info.startswith(('https://www.gov.br/mma/pt-br/noticias', 'https://www.gov.br/mma/pt-br/assuntos/noticias')):
                new_info = info
                #print(new_info)
            links.append(new_info)
    
        lista = np.unique(links).tolist()
        new_links = getNewInfo(links_base, lista)

        if(new_links):
            for i in new_links:
                page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'documentFirstHeading').get_text()
                texto = soup.find('div', property = 'rnews:articleBody').get_text()
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
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'govmma_')
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em govmma2')
        
#govmma2(os.getcwd())

def govmma3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\govmma_03.csv'
        titulos = []
        textos = []
        links = ['https://www.gov.br/mma/pt-br/acesso-a-informacao/institucional/secretarias']

        page = Request('https://www.gov.br/mma/pt-br/acesso-a-informacao/institucional/secretarias', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1', class_ = "documentFirstHeading").get_text()
        texto = soup.find('div', id = "parent-fieldname-text").get_text()
        titulos.append(titulo)
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['govmma']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'govmma_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em govmma3')
        
#govmma3(os.getcwd())
