# AB#134
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen
def forestgeo1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\forestgeo_01.csv'
        titles = [] #
        deadlines = [] #
        texts = [] #
        hasBrazil = [] #
        types = [] #
        eleg = []
        dia = datetime.today().strftime("%y%m%d")
        page_request = requests.get('https://forestgeo.si.edu/training-and-fellowships/grants-program').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        text = ''
        for p in page_soup.find_all('p'):
            text +=p.text
        texts.append(text)
        if(page_soup.find('h2', class_='rtecenter') is not None):
            titulo = page_soup.find('h2', class_='rtecenter').text
            titles.append(titulo)
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
            elegtexts = page_soup.find_all('p')[7:9]
            text = ''
            for p in elegtexts:
                text+=p.text
            eleg.append(text)
            deadline = page_soup.find('h6').find_all('strong')[0].text.split(':')[1].strip()
            deadlines.append(deadline)
            df = pd.DataFrame()          
            df['opo_titulo'] = titles  
            df['link'] = ['https://forestgeo.si.edu/opportunities/grants-program']    
            df['opo_texto'] = texts   
            df['opo_texto_ele'] = eleg
            df['opo_brazil'] = hasBrazil   
            df['opo_tipo'] = types      
            df['opo_deadline'] = deadlines   
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'forestgeo_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em forestgeo1')

def forestgeo2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\forestgeo_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://forestgeo.si.edu/what-forestgeo/news-blog').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='view-content')
        for new in soup.find_all('a'):
            link = 'https://forestgeo.si.edu/' + new['href']
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('div', class_='panel-pane pane-node-title').find('h1').get_text())
                texto = clean(page_soup.find('div', class_='field field--name-body field--type-text-with-summary field--label-hidden').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'forestgeo_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em forestgeo2')



def forestgeo3(path):
    try:
        titulos = []
        textos = []
        links = ['https://forestgeo.si.edu/what-forestgeo/code-conduct', 'https://forestgeo.si.edu/training-and-fellowships/grants-program']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\forestgeo_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='page-title').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='content').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['forestgeo']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'forestgeo_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em forestgeo3')
