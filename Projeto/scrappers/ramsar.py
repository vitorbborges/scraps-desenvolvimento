import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import os

def ramsar2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\ramsar_02.csv'
        titulos = []
        textos = []
        links = []
        lista = []
        page_response = requests.get('https://www.ramsar.org/search?f%5B0%5D=type%3Anews#search-news').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('span', class_ = 'field-content')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/news'):
                new_info = ('https://www.ramsar.org' + info)
                lista.append(new_info)
                
        links = pd.unique(lista).tolist()
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in new_links:
                page_response = requests.get(i).content.decode('UTF-8')
                soup = BeautifulSoup(page_response, 'lxml') 
                titulo = soup.find('div', class_ = 'field field-name-title field-type-ds field-label-hidden').get_text()
                titulos.append(titulo)
                texto = soup.find('div', class_ = 'field field-name-body field-type-text-with-summary field-label-hidden').get_text()
                textos.append(clean(texto))
            
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'ramsar_')
            df.to_csv(path + filename, index = False) 
            
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
    except Exception as e:
        print(e)
        print('Erro em ramsar2')
        
#ramsar2(os.getcwd())
        
def ramsar3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.ramsar.org/about/the-convention-on-wetlands-and-its-mission', 'https://www.ramsar.org/about/the-bodies-of-the-convention', 'https://www.ramsar.org/about/transparency', 'https://www.ramsar.org/about/resource-mobilization-grants']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\ramsar_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='title').text)
            titulos.append(titulo)
            texto = clean(soup.find_all('div', class_='field-items')[1].text)
            textos.append(texto)
            
        #Partnerships:
        link = 'https://www.ramsar.org/about/partnerships'
        req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1', class_='title').text)
        titulos.append(titulo)
        texto = clean(soup.find_all('div', class_='field-items')[1].text + soup.find_all('div', class_='field-items')[2].text)
        textos.append(texto)
        links.append(link)
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['ramsar']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'ramsar_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em ramsar3')
        
#ramsar3(os.getcwd())