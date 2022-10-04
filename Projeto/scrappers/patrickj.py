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


def patrickj2(path):
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
        filename = '\\patrickj_02.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://www.mcgovern.org/news-insights/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sopa = soup.find('div', class_='blog')

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
            info = info
            links.append(info)  
            links2 = []
            for i in links:
                if i not in links2:
                    links2.append(i)


        for word in links2[:]:
            if word.startswith('?'):
                links2.remove(word)



            
        for i in links2: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            pretitulo = soup3.find('div', class_='page-title-inner')
            titulo = pretitulo.find('h1').get_text()
            titulos.append(clean(titulo))
            texto = soup3.find_all('div', class_ = 'col-12 col-md-10 col-lg-8')[-1].text
            #print(texto)
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
        df['not_titulo'] = pd.Series(titulos)
        df['link'] = pd.Series(links)
        df['not_texto'] = pd.Series(textos)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'patrickj_')
        df.to_csv(path + filename, index = False)

    except Exception as e:
        print(e)
        print('Erro em patrickj2')

def patrickj3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\patrickj_03.csv'
        titulos = []
        textos = []
        links = ['https://www.mcgovern.org/about/']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'page-title-inner').find('h1').get_text()
            texto = soup.find('div', class_ = 'gutenberg-body').text
            titulos.append(clean(titulo))
            textos.append(clean(texto))
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['patrickj']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'patrickj_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em patrickj3')   

def patrickj4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\patrickj_04.csv'
        titulos = []
        links = []
        paginas = []
        values = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_page = 'https://www.mcgovern.org/grants/'
        link_page2 = 'https://www.mcgovern.org/grants/'

        page = requests.get(link_page).content.decode('utf-8')
        page_soup = BeautifulSoup(page, 'lxml')

        proj = page_soup.find('div', class_='grants container').find_all('article', class_='col-12 col-md-12 col-lg-9 offset-lg-1 grants-tease tease tease-grants')

        for a in proj:
            link = a.find('a')['href']
            links.append(link)
            #print(links)

      
        for z in proj:
            title = z.find('h2').text
            titulos.append(clean(title))
            #print(titulos)
            valor = z.find('div', class_= 'grant-field-container').text
            valor = re.sub(' ', '', valor)
            #print(valor)
            values.append(clean(valor))             
        df = pd.DataFrame()
        df['prj_titulo'] = pd.Series(titulos) 
        df['link'] = pd.Series(links) 
        df['prj_instituicao'] = ['PATRICKJ']*len(df.index)
        df['prj_valor'] = pd.Series(values)
        df['prj_brazil'] = ['Y']*len(df.index)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'patrickj_')
        df.to_csv(path+filename, index=False)
        

    except Exception as e:
        print(e)
        print('Erro em patrickj4')
