# AB#99
from utilidadesppf import getCodList, getInfoBase, getNewInfo, clean
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen
import os

def englishrvo1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\englishrvo_01.csv'
        titles = [] #
        links = [] #
        deadlines = [] 
        texts = []
        hasBrazil = [] #
        types = [] #
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime("%y"))
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        
        page_request = requests.get('https://english.rvo.nl/subsidies-programmes?filter5=8245').content.decode('utf-8')
        soup = BeautifulSoup(page_request, 'lxml')
        
        for i in soup.find_all('div', class_='views-field-title'):
            link = i.find('a')['href']
            # print('https://english.rvo.nl'+ link)
            links.append('https://english.rvo.nl' + link)
        
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for i in new_links:
                page_request = requests.get(i).content.decode('utf-8')
                page_soup = BeautifulSoup(page_request, 'lxml')
                titulo = clean(page_soup.find('h1').get_text())
                titles.append(titulo)
                text = clean(page_soup.find('div', class_='content').get_text())
                texts.append(text)
                if page_soup.find('span', class_='rest') != None:
                    deadlines.append(page_soup.find('span', class_='rest').text)
                else:
                    deadlines.append('Deadline não encontrada')
                added = False
                for x in soup.find_all('div', class_="subsidie-item"):
                    if x.find('a').text == titulo:
                        if(findall(keywords, str(x).lower())):
                            hasBrazil.append('Y')
                            added = True
                        else:
                            hasBrazil.append('N')
                            added = True
                if not added:
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
            df['link'] = new_links    
            df['opo_texto_ele'] = texts
            df['opo_texto'] = texts
            df['opo_brazil'] = hasBrazil   
            df['opo_tipo'] = types      
            df['opo_deadline'] = deadlines   
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'englishrvo_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em englishrvo1')


#englishrvo1(os.getcwd())

def englishrvo2(path = '''/Volumes/HD 1TB''', keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+ '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/englishrvo_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://english.rvo.nl/news/news', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        #print(soup)
        soup3 = BeautifulSoup(str(soup.find_all('div', class_ = "content-wrap")), 'lxml') # índice de notícias da página principal 

        for link in soup3('a', href=True):
            #print("https://english.rvo.nl" + link['href'])
            #print(soup.get_text)()
            links.append("https://english.rvo.nl" + link['href'])

        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            texto = soup.find('div', class_ = "content").get_text()
            titulo = soup.find('h1', class_ = "clearfix").get_text()
            textos.append(clean(texto))
            titulos.append(clean(titulo))
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'englishrvo_')
        df.to_csv(path + filename, index = False)
    
    except Exception as e:
        print(e)
        print('Erro em englishrvo2')

#englishrvo2(os.getcwd())


def englishrvo3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '/englishrvo_03.csv'
        titulos = []
        textos = []
        link = 'https://english.rvo.nl/about-us'
        req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').text)
        titulos.append(titulo)
        soup2 = clean(soup.find('p').next_sibling.text)
        soup3 = clean(soup.find('p').next_sibling.next_sibling.text)
        textos.append(soup2 + soup3)
                
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['englishrvo']*len(df.index)
        df['pol_texto'] = (soup2 + soup3)
        df['link'] = link
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'englishrvo_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em englishrvo3')
        
#englishrvo3(os.getcwd())
