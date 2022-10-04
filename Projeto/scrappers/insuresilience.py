# AB#153
import shutil
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList, getInfoBase, clean
from re import findall
import shutil
from urllib.request import Request, urlopen
import os

def insuresilience1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\insuresilience_01.csv'
        titles = [] 
        links = [] 
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        page_response = requests.get('https://www.insuresilience-solutions-fund.org/call-for-proposals').content.decode('utf-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('span', class_='hero__headline').get_text()
        titles.append(titulo)

        links.append('https://www.insuresilience-solutions-fund.org/call-for-proposals')

        text = soup.find('div', class_ = 'wrap wrap--text').get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split())
        texts.append(text)


        deadline = soup.find('div', class_='section__content').find('p').text
        deadlines.append(deadline)

        eleg_text = soup.find('header', id='target-countries-and-groups')
        eleg_text = eleg_text.parent.get_text()
        eleg_text = re.sub('\n', ' ', eleg_text)
        eleg_text = ' '.join(eleg_text.split())
        eleg_texts.append(eleg_text)

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
        df['link'] = links  
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = eleg_texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'insuresilience_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em insuresilience1')

#insuresilience1(os.getcwd())

def insuresilience2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\insuresilience_02.csv'
        titulos = []
        textos = []
        titulos_base = getInfoBase(pathbase, filename, 'not_titulo')
        page = requests.get('https://www.insuresilience-solutions-fund.org/news-events').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for new in soup.find_all('article', class_='item item-news'):
            titulo = clean(new.find('h3', class_='item__headline / headline').text)
            if(titulo not in titulos_base):
                titulos.append(titulo)
                texto = clean(new.find('div', class_='item__content / copy').get_text())
                textos.append(texto)
        if titulos:
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = ['https://www.insuresilience-solutions-fund.org/news-events']*(len(df.index))
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'insuresilience_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em insuresilience2')

#insuresilience2(os.getcwd())

def insuresilience3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.insuresilience-solutions-fund.org/our-work', 'https://www.insuresilience-solutions-fund.org/about/about-isf']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\insuresilience_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='headline').get_text())
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='section__content').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['insuresilience']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'insuresilience_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em insuresilience3')
        
#insuresilience3(os.getcwd())
