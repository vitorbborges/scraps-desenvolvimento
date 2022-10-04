# AB#149
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re
from utilidadesppf import getCodList, getNewInfo, getInfoBase, clean
from re import findall
from urllib.request import Request, urlopen
import shutil
def eocaconservation1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\eocaconservation_01.csv'
        titles = [] 
        links = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        dia = datetime.today().strftime("%y%m%d")
        req = Request('https://www.eocaconservation.org/project-info.cfm?pageid=20', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        request = urlopen(req).read()
        soup = BeautifulSoup(request, 'lxml')
        soup = soup.find('div', class_='internal-left')
        titulo = 'Funding from Eoca'
        titles.append(titulo)
        links.append('https://www.eocaconservation.org/project-info.cfm?pageid=20')
        deadline = soup.find('h2').get_text()
        text = soup.get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split())
        texts.append(text)
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
        df = pd.DataFrame()
        df['opo_titulo'] = titles  
        df['link'] = links  
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = [deadline]
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'eocaconservation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em eocaconservation1')


def eocaconservation2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\eocaconservation_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        req = Request('https://www.eocaconservation.org/news-features.cfm', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        for card in soup.find('div', id = 'news-col').find_all('div', class_ = 'current-project'):
            link = card.find('a')['href']
            links.append('https://www.eocaconservation.org/' + link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page = urlopen(req).read()
                page_soup = BeautifulSoup(page, 'lxml')
                soup = page_soup.find('div', class_='internal-left')

                titulo = soup.find('h1').text
                titulos.append(titulo)
                texto = clean(soup.get_text())
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'eocaconservation_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em eocaconservation2')     

def eocaconservation3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\eocaconservation_03.csv'
        req = Request('https://www.eocaconservation.org/about-us.cfm', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('div', class_='internal-left').find('h1').text)
        titulos.append(titulo)
        texto = clean(soup.find('div', class_ = 'internal-left').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['eocaconservation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = ['https://www.eocaconservation.org/about-us.cfm']
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'eocaconservation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em eocaconservation3')
