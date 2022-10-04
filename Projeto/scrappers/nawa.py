# AB#146
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

def nawa1(path, keywords = 'brazil'):
    try:
        filename = '\\nawa_01.csv'
        titles = [] 
        links = []
        main_links = ['https://nawa.gov.pl/en/nawa-programmes/nawa-programmes-alias/ongoing'] #
        texts = [] #
        hasBrazil = []# 
        types = [] #
        deadlines = []#
        dia = datetime.today().strftime("%y%m%d")
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        deadlines_base = getInfoBase(pathbase, filename, 'opo_deadline')
        for link in main_links:
            request = requests.get(link).content.decode('utf-8')
            soup = BeautifulSoup(request, 'lxml')
            for opo in soup.find_all('div', class_='eb-category-5 eb-event-container'):
                opo_link = 'https://nawa.gov.pl/' + opo.find('a')['href']
                opo_deadline = opo.find('span', class_='eb-event-date-info').find('meta', itemprop="endDate")['content']
                deadlines.append(opo_deadline)
                links.append(opo_link)

        new_deadlines = getNewInfo(deadlines_base, deadlines)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                eleg_text = ''
                text = ''
                request = requests.get(link).content.decode('utf-8')
                soup = BeautifulSoup(request, 'lxml')
                #--------------------------------------------------------
                titulo = soup.find('h2', class_= 'eb-page-heading header').get_text().strip()
                titles.append(titulo)
                #--------------------------------------------------------
                text = soup.find('div', class_='eb-description-details clearfix').get_text()
                text = re.sub('\n', ' ', text)
                text = ' '.join(text.split())
                texts.append(text)
                if(soup.find_all(keywords, text.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N') 
                if len(soup.find_all('grant', text.lower())):         
                    types.append('grant')            
                elif len(soup.find_all('fellowship', text.lower())):  
                    types.append('fellowship')          
                elif len(soup.find_all('scholarship', text.lower())): 
                    types.append('scholarship')                   
                else:
                    types.append('other')
                #--------------------------------------------------------
            df = pd.DataFrame()          
            df['opo_titulo'] = pd.Series(titles)  #
            df['link'] = pd.Series(new_links)#
            df['opo_texto'] = pd.Series(texts)   
            df['opo_texto_ele'] = pd.Series(texts)
            df['opo_brazil'] = pd.Series(hasBrazil)   
            df['opo_tipo'] = pd.Series(types)    
            df['opo_deadline'] = pd.Series(new_deadlines)
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'nawa_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)

    except Exception as e:
        print(e)
        print('Erro em nawa1')



def nawa2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\nawa_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://nawa.gov.pl/en/nawa/news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='blog')
        for new in soup.find_all('a'):
            link = 'https://nawa.gov.pl/' + new['href']
            if link not in links and len(links) < 4:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('div', class_='page-header').find('h1').get_text())
                texto = clean(page_soup.find('div', itemprop = 'articleBody').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'nawa_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em nawa2')



def nawa3(path):
    try:
        titulos = []
        textos = []
        links = ['https://nawa.gov.pl/en/nawa', 'https://nawa.gov.pl/en/recognition/legal-framework-for-recognition']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\nawa_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('div', class_='page-header').find('h1').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='item-page').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['nawa']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'nawa_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em nawa3')
