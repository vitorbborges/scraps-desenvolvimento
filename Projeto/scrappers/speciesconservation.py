import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
import requests
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def speciesconservation1(path, keywords = '(brazil|latin america region)'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().year
        filename = '\\speciesconservation_01.csv'
        links = []
        titulos = []
        textos = []
        deadlines = []
        hasBrazil = []
        tipos = []
        scrape = []
        texto_elegivel = []
        page_response = requests.get('https://www.speciesconservation.org/grants/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        scrape.append(str(soup))
        link = 'https://www.speciesconservation.org/grants/'
        links.append(link)
        titulo = soup.find('div', id = 'page-wrapper').find('h1').get_text()
        titulos.append(titulo)
        texto = soup.find('div', id = 'page-content').get_text()
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
            
        deadline = soup.find('p', {'p': re.compile('deadline')})
            
        deadlines = list(dict.fromkeys(deadlines))
        deadlines.append(deadline)
                            
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_deadline'] = deadlines 
        #df['html'] = scrape
        df['opo_texto'] = textos 
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['opo_brazil'] = hasBrazil
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'speciesconservation_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em speciesconservation1')
        
#speciesconservation1('.')

def speciesconservation2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\speciesconservation_02.csv'
        titulos = []
        textos = []
        links = []
        page_response = requests.get('https://www.speciesconservation.org/media-center/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find_all('article', class_ = 'directory-listing')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/media-center'):
                new_info = ('https://www.speciesconservation.org' + info)
                links.append(new_info)
                
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in new_links:
                page_response2 = requests.get(i).content.decode('UTF-8')
                soup3 = BeautifulSoup(page_response2, 'lxml')
                texto = soup3.find('div', id = 'page-content').get_text()
                titulo = soup3.find('div', id = 'page-content').find('h3').get_text()
                textos.append(clean(texto))
                titulos.append(titulo)
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'speciesconservation_')
            df.to_csv(path + filename, index = False)    
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
                    
    except Exception as e:
        print(e)
        print('Erro em speciesconservation2')
        
#speciesconservation2('.')  

def speciesconservation3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\speciesconservation_03.csv'
        titulos = []
        textos = []
        links = ['https://www.speciesconservation.org/about-us/', 'https://www.speciesconservation.org/about-us/how-does-the-fund-work', 'https://www.speciesconservation.org/about-us/vision-and-mission']

        for i in links:
            page_response = requests.get(i).content.decode('UTF-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('h1').get_text()
            texto = soup.find('article', class_ = 'row').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['speciesconservation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'speciesconservation_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em speciesconservation3')
        
#speciesconservation3('.')

def speciesconservation4(path, keywords = 'brazil'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\speciesconservation_04.csv'
        titulos = []
        textos = []
        hasBrazil = []
        links = []
        instituicao = 'species conservation'
        value = 'valor não encontrado'
        keywords = 'brazil'
        page_response = requests.get('https://www.speciesconservation.org/large-grants/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        sites = soup.find('div', class_ = 'text-up-grid-wrapper')
        soup2 = BeautifulSoup(str(sites), 'lxml')

        for i in soup2.findAll('a'):
            info = i['href']
            if info.startswith('/large'):
                new_info = ('https://www.speciesconservation.org' + info)
                links.append(new_info)


        for i in soup.find_all('p', attrs={'class': 'grid-title'}):
            titulo = i.get_text()
            titulos.append(titulo)
            
        for i in soup.find_all('p', attrs={'class': 'location-description'}):
            text = i.get_text()
            textos.append(text)
            if(findall(keywords, text.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')

        df = pd.DataFrame()
        df['prj_titulo'] = titulos
        df['link'] = links
        df['prj_instituicao'] = [instituicao]*len(df.index)
        df['prj_valor'] = [value]*len(df.index)
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'speciesconservation_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em speciesconservation4')   
        
#speciesconservation4('.')
            
