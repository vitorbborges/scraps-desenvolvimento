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


def amazonscience2(path):
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
        filename = '\\amazonscience_02.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = Request('https://www.amazon.science/latest-news', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sopa = soup.find('ul', class_='ListB-items')

        keywords = 'brazil'

        for i in sopa.find_all('div', class_= 'PromoA-title'):
            info = i.find('a')['href']
            info = info
            links.append(info)  
        for i in links: 
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            titulo = soup3.find('h1').text
            titulos.append(clean(titulo))
            texto = soup3.find('div',class_= 'ArticlePage-articleContainer' ).text
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
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'amazonscience_')
        df.to_csv(path + filename, index = False)
        #print(df)
    except Exception as e:
        print(e)
        print('Erro em amazonscience2')

def amazonscience3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\amazonscience_03.csv'
        titulos = []
        textos = []
        links = ['https://www.amazon.science/about']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('h1', class_ = 'ArticlePage-headline').get_text()
            #print(titulo)
            texto = soup.find('div', class_ = 'RichTextArticleBody-body RichTextBody').get_text()
            #print(texto)
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['amazonscience']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'amazonscience_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em amazonscience3')   

