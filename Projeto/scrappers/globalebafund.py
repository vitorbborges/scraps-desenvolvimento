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

def globalebafund1(path, keywords = '(brazil|latin america region)'): 
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
        filename = '\\globalebafund_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://globalebafund.org/grantees/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        


        for i in soup.find_all('div', class_=lambda x: x and x.endswith('_wp-block-column"')):
            #print(i)
            info = i.find('a')['href']
            if info.startswith("https"):
                info = i.find('a')['href']
                info = info
                links.append(info)
                #print(links)

            else: 
                pass


        for i in links: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            titulo = soup3.find('header', class_='entry-header responsive-max-width').find('h1').text
            titulos.append(clean(titulo))
            texto = soup3.find('p==$0')
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
        df['codigo'] = getCodList(dia, len(df.index), '1', 'globalebafund_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        #print(df)
        
    except Exception as e:
        print(e)
        print('Erro em globalebafund1')

def globalebafund2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\globalebafund_02.csv'
        titulos = []
        textos = []
        links = 'https://globalebafund.org/announcements/'
        hasBrazil = []
        tipos = []
        scrape = []
        keywords = 'brazil'
        page_response = requests.get(links, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
        soup = BeautifulSoup(page_response, 'lxml')


        for z in soup.find_all('div', class_='wp-block-media-text__content'):
            titulo = z.find('em').text
            texto = z.text
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)


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
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'globalebafund_')
        df.to_csv(path + filename, index = False)

    except Exception as e:
        print(e)
        print('globalebafund2')

def globalebafund3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\globalebafund_03.csv'
        titulos = []
        textos = []
        links = ['https://globalebafund.org/about/', 'https://globalebafund.org/about/what-is-eba/', 'https://globalebafund.org/about/contact/']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('h1', class_ = 'entry-title').get_text()
            #print(titulo)
            texto = soup.find('div', class_ = 'wp-block-media-text__content').get_text()
            #print(texto)
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['globalebafund']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'globalebafund_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em globalebafund3')   
