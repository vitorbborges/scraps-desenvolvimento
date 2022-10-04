# AB#46
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
from itertools import compress
import shutil
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
from urllib.request import Request, urlopen


def oceanfdn2(path, keywords = 'brazil'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oceanfdn_02.csv'
        titulos = []
        textos = []
        links = []
        page1 = requests.get('https://oceanfdn.org/post-category/news/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page1.text, 'lxml')
        soup2 = soup.find('div', class_ = "query-posts")
        soup3 = BeautifulSoup(str(soup.find_all('h3', class_ = "title")), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')


        for i in soup3.find_all('a'):
            links.append(i['href'])

        for i in links: 
            page = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = clean(soup.find('h1').text)
            texto = clean(soup.find('div', class_ = "wrap interior").get_text())
            texto = clean(soup.find('div', class_ = "wrap interior").text)
            textos.append(clean(texto))
            titulos.append(clean(titulo))
            df = pd.DataFrame()
            df['not_titulo'] = pd.Series(titulos)
            df['link'] = pd.Series(links)
            df['not_texto'] = pd.Series(textos)
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'oceanfdn_')
            df.to_csv(path+filename, index=False)
    
    except Exception as e:
        
        print(e)
        print('Erro em oceanfdn2')
        
# oceanfdn2('.')

def oceanfdn3(path):
    try: 
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oceanfdn_03.csv'
        titulos = []
        textos = []
        links = ['https://oceanfdn.org/about/', 'https://oceanfdn.org/projects/research-development-71/', 'https://oceanfdn.org/grantmaking/', 'https://oceanfdn.org/about/financial-information/']

        for link in links:  
            page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = clean(soup.find('h1').get_text())
            texto = BeautifulSoup(str(soup.find_all('p')), 'lxml').text
            titulos.append(clean(titulo))
            textos.append(clean(texto))
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['oceanfdn']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'oceanfdn_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    
    except Exception as e:
        
        print(e)
        print('Erro em oceanfdn3')
        
# oceanfdn3('.')
    
def oceanfdn4(path, keywords = '(latin american region|brazil)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oceanfdn_04.csv'
        titulos = []
        links = []
        values = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')

        dia = datetime.today().strftime('%y%m%d') #setando o dia
        page = requests.get('https://oceanfdn.org/projects/', headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'})
        soup = BeautifulSoup(page.text, 'lxml')
        texto= clean(soup.find('div',class_='theme-block projects').text)

        presoup = soup.find_all('h3')
        soup2 = BeautifulSoup(str(presoup),'html.parser')

        for link in soup2.find_all('a'): #busca por links
            links.append(link['href']) #adiciona à lista

        new_links = getNewInfo(links_base, links)
        
        # new_links = links

        for link in new_links:
            page = requests.get(link, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            page_soup = BeautifulSoup(page, 'lxml')
            prepagy = page_soup.find('div', class_="title")
            pagy = BeautifulSoup(str(prepagy), 'html.parser')
            title = page_soup.find('h1').text
            titulos.append(clean(title))
            values.append('Valor não encontrado')   
            prj_inst.append('The Ocean Foundation')
            if(findall(keywords, texto.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
                
        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = new_links 
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = values
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'oceanfdn_')
        df.to_csv(path + filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em oceanfdn 4')

# oceanfdn4('.')
