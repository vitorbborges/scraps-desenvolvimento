# AB#161
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import Request, urlopen
from utilidadesppf import getCodList, clean
from re import findall
def cargill1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\cargill_01.csv'
        titles = [] 
        links = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + datetime.today().strftime("%y")
        req = Request('https://www.cargillglobalscholars.com/scholarship/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h2', class_='accent').text
        titles.append(titulo)
        links.append('https://www.cargillglobalscholars.com/scholarship/')
        text = clean(soup.find('div', class_='one-col-padding m-b-30 links--black').get_text())
        i = 0
        for a in soup.find_all('a', class_='button-primary'):
            link = 'https://www.cargillglobalscholars.com/' + a['href']
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            if(soup.find('div', class_='content') is not None):
                text += clean(soup.find('div', class_='content').get_text())
            else:
                text += clean(soup.find('div', class_='one-col-padding m-b-30 links--black').get_text())
            if(i == 1):
                eleg_text = clean(soup.find('div', class_='content').get_text())
            i+=1
        eleg_texts.append(eleg_text)
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
        df['opo_texto_ele'] = eleg_texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = '31 de dezembro de '+ ano  
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'cargill_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em cargill1')


def cargill3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\cargill_03.csv'
        req = Request('https://www.cargillglobalscholars.com/about-cargill/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1', class_='accent').get_text())
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='narrow-inner').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['cargill']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = ['https://www.cargillglobalscholars.com/about-cargill/']
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'cargill_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em cargill3')





