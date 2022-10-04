# AB#40
# AB#148
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList
from re import findall
from utilidadesppf import getInfoBase, getNewInfo, clean
import shutil
from urllib.request import Request, urlopen

def futureoflife1(path, keywords = '(brazil|latin america region)'): 
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = []
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\futureoflife_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = Request('https://futureoflife.org/grant-programs/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sopa = soup.find('div', class_='flex_column_table av-equal-height-column-flextable -flextable')

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
            info = info
            links.append(info)  

        #print(links)

        for i in links: 
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            titulo = soup3.find('div', class_='sma-program-profile-card-left').find('h2').text
            #print(titulo)
            titulos.append(clean(titulo))
            texto = soup3.find('div', class_ = 'fr-view').get_text()
            textos.append(clean(texto))
            if(findall(keywords, texto.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            if(findall('grant', texto.lower())):         
                tipos.append('grant')                
            elif(findall('fellowship', texto.lower())):  
                tipos.append('fellowship')          
            elif(findall('scholarship', texto.lower())): 
                tipos.append('scholarship')                   
            else:
                tipos.append('other')
            scrape.append(str(soup))
       
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_texto'] = textos 
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['codigo'] = getCodList(dia, len(df.index), '1', 'futureoflife_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        #print(df)
        
    except Exception as e:
        print(e)
        print('Erro em futureoflife1')



def futureoflife2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = []
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\futureoflife_02.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = Request('https://futureoflife.org/newsletters/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sopa = soup.find('div', class_='avia-content-slider-inner')

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
            info = info
            links.append(info)  

        links = list(dict.fromkeys(links))
        #print(links)
        for i in links: 
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            try:
                titulo = soup3.find('h1').text
                titulos.append(clean(titulo))
            except:
                titulo = soup3.find('b').text
                titulos.append(clean(titulo))
            #print(titulos)
            texto = soup3.find('section', class_ = 'av_textblock_section').text
            textos.append(clean(texto))
            if(findall(keywords, texto.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            if(findall('grant', texto.lower())):         
                tipos.append('grant')                
            elif(findall('fellowship', texto.lower())):  
                tipos.append('fellowship')          
            elif(findall('scholarship', texto.lower())): 
                tipos.append('scholarship')                   
            else:
                tipos.append('other')
            scrape.append(str(soup))

        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'futureoflife_')
        df.to_csv(path + filename, index = False)

    except Exception as e:
        print(e)
        print('Erro em futureoflife2')

def futureoflife3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\futureoflife_03.csv'
        titulos = []
        textos = []
        links = ['https://futureoflife.org/grants-faq/']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'entry-content').find('h1').get_text()
            #print(titulo)
            texto = soup.find('div', class_ = 'entry-content').get_text()
            #print(texto)
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['futureoflife']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'futureoflife_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em futureoflife3')   

