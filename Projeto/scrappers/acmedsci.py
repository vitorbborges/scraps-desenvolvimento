#AB #111

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import requests
import pandas as pd
import urllib
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def acmedsci1(path, keywords = 'brazil'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().year
        filename = '/acmedsci_01.csv'
        links = ['https://acmedsci.ac.uk/grants-and-schemes/grant-schemes/gcrf-networking-grants']
        titulos = []
        textos = []
        deadlines = []
        hasBrazil = []
        tipos = []
        scrape = []
        texto_elegivel = []
        page_response = requests.get('https://acmedsci.ac.uk/grants-and-schemes/grant-schemes/gcrf-networking-grants').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        scrape.append(str(soup))

        titulo = soup.find('h1').get_text()
        titulos.append(clean(titulo))

        texto = soup.find('section', id = 'tab1').get_text()
        textos.append(clean(texto))

        if(findall('grant', texto.lower())):         
            tipos.append('grant')                
        elif(findall('fellowship', texto.lower())):  
            tipos.append('fellowship')          
        elif(findall('scholarship', texto.lower())): 
            tipos.append('scholarship')                   
        else:
            tipos.append('other')

        texto_ele = soup.find('section', id = 'tab2').get_text()
        texto_elegivel.append(clean(texto_ele))

        if(findall(keywords, texto.lower())):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
            
        deadline = soup.find('p', style = 'text-align: left;').get_text()
        removelist = "/"
        deadline = re.sub(r'[^\d'+removelist+']', '', '31/12/' + deadline)
        deadlines.append(deadline)

        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_deadline'] = deadline
        df['opo_texto'] = [textos + texto_elegivel] 
        df['opo_texto_ele'] = texto_elegivel
        df['opo_tipo'] = tipos
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'acmedsci_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em acmedsci1')   
        
#acmedsci1('.')

def acmedsci2(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\acmedsci_02.csv'
        titulos = []
        textos = []
        links = []
        link = []
        page_response = requests.get('https://acmedsci.ac.uk/more/news').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        
        links = [re.sub(" ",'',i) for i in links]
        for i in soup.find_all('a', href=True):
            info = i['href']
            if info.startswith('/more/news/'):
                new_info = ('https://acmedsci.ac.uk' + info) 
                link.append(new_info)
                
        links = pd.unique(link).tolist()
        links = [re.sub(" ",'',i) for i in links]
        new_links = getNewInfo(links_base, links)


        if(new_links):
            for i in new_links:
                page_response2 = requests.get(i).content.decode('UTF-8')
                soup2 = BeautifulSoup(page_response2, 'lxml')
                titulo = soup2.find('div', class_ = 'col content left').find_next('h1').get_text()
                texto = soup2.find('div', class_ = 'col content left').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'acmedsci_')
            df.to_csv(path + filename, index = False)    
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
    
    except Exception as e:
        print(e)
        print('Erro em acmedsci2')   
        
#acmedsci2('.')

def acmedsci3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\acmedsci_03.csv'
        titulos = []
        textos = []
        links = ['https://acmedsci.ac.uk/policy/overview/how-policy', 'https://acmedsci.ac.uk/about/support-us/how-we-are-funded']

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('h1').get_text()
            texto = soup.find('div', class_ = 'page-content').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['acmedsci']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'acmedsci_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em acmedsci1')   
        
#acmedsci3('.') 
