# AB#139
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
import requests
import shutil
import re
from utilidadesppf import getCodList, getNewInfo, getInfoBase, clean
from re import findall
from urllib.request import Request, urlopen
import os

def okczoo1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\okczoo_01.csv'
        titles = [] 
        links = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        dia = datetime.today().strftime("%y%m%d")
        ano = date.today().year
        page_response = requests.get("https://www.okczoo.org/can-grant-program", headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).content.decode('utf-8')
        soup = BeautifulSoup(page_response, 'lxml')
        big = soup.find('div', class_ = 'inner-content pull-left')
        soup = big.find('div', class_ = 'templatecontent')
        titulo = soup.find('h1').text
        titles.append(titulo)
        links.append('https://www.okczoo.org/can-grant-program')
        text = big.get_text()
        text = re.sub('\n', ' ', text)
        text = " ".join(text.split())
        texts.append(text)
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
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = ['31 de dezembro de ' + str(ano)] 
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'okczoo_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em okczoo1')






def okczoo2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\okczoo_02.csv'
        titulos = []
        textos = []
        links = []
        i = 0
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.okczoo.org/news', headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for new in soup.find_all('div', class_='news-archive-entry-container'):
            link = 'https://www.okczoo.org/' + new.find('a')['href']
            if i < 10:
                links.append(link)
            else:
                break
            i+=1
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                page_soup = page_soup.find('div', class_='news-archive-container')
                titulo = clean(page_soup.find('h2').get_text())
                texto = ''
                for p in page_soup.find_all('p'):
                    texto += p.get_text()
                texto = clean(texto)
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'okczoo_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em okczoo2')

        
def okczoo3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.okczoo.org/conservation-projects', 'https://www.okczoo.org/okc-living-classroom-grant-program']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\okczoo_03.csv'
        for link in links:
            page = requests.get(link, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}).content.decode('utf-8')
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h2').text)
            titulos.append(titulo)
            texto = clean(soup.find_all('div', class_='templatecontent')[2].get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['okczoo']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'okczoo_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em okczoo3')
        

