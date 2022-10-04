# AB#93
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList, getInfoBase, getNewInfo, clean
from re import findall
from urllib.request import Request, urlopen
import os


def impact1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\impact_01.csv'
        titles = [] 
        links = [] 
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        page_response = requests.get('http://impact.man.eu/').content.decode('utf-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('h1', class_='visually-hidden').text
        titles.append(titulo)
        links.append('http://impact.man.eu/')

        text_area = soup.find('div', class_ = 'specialLead')
        text = ''
        for p in text_area.find_all('p'):
            text+=p.text
        eleg_text = soup.find_all('div', class_ = 'intro-text')[2].get_text()
        eleg_text = re.sub('\n', ' ', eleg_text)
        #print(eleg_text.strip())
        eleg_texts.append(eleg_text)
        texts.append(text)
        deadline = soup.find('div', class_ = 'text-center col-sm-12 col-md-8 col-md-offset-2').find('div', class_ = 'ctaBlockTextUnderCtaButton').text.split(':')[1]
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
        df['opo_texto_ele'] = eleg_texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'impact_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em impact1')

#impact1(os.getcwd())

def impact3(path):
    try:
        titulos = []
        textos = []
        link = 'http://impact.man.eu/#mission'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\impact_03.csv'
        req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        i = 0
        for pol in soup.find_all('div', class_='matrix container'):
            if i >=2 :
                break
            titulo = pol.find('h2', class_='h1').text
            titulos.append(titulo)
            texto = pol.text
            texto = clean(texto)
            textos.append(texto)
            i +=1
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['impact']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = [link]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'impact_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em impact3')
        
#impact3(os.getcwd())

