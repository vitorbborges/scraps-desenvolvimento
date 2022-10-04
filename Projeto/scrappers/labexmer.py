# AB#158
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList, clean
from re import findall
from urllib.request import Request, urlopen
def labexmer1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\labexmer_01.csv'
        titles = [] 
        links = [] 
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        dia = datetime.today().strftime("%y%m%d")
        page_response = requests.get('https://www.labexmer.eu/en/international/postdoctoral-fellowships').content.decode('utf-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('h1', class_='documentFirstHeading').text
        titulo = clean(titulo)
        # print(titulo)
        titles.append(titulo)
        links.append('https://www.labexmer.eu/en/international/postdoctoral-fellowships')

        text = soup.find('div', id='content-core').get_text()
        text = clean(text)
        # print(text)
        texts.append(text)

        deadline = soup.find('div', id='content-core').find_all('p')[-3].get_text()
        # print(deadline)
        deadlines.append(deadline)


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
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'labexmer_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em labexmer1')

def labexmer3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\labexmer_03.csv'
        page = requests.get('https://www.labexmer.eu/en/about-us').text
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').get_text())
        titulos.append(titulo)
        texto = clean(soup.find('div', id = 'content-core').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['labexmer']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = ['https://www.labexmer.eu/en/about-us']
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'labexmer_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em labexmer3')