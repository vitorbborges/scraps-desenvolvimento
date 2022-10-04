# AB#143
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList, clean
from re import findall
from urllib.request import Request, urlopen
def fundinnovation1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\fundinnovation_01.csv'
        titles = [] 
        links = [] 
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        ano = datetime.today().strftime('%y')
        page_response = requests.get('https://fundinnovation.dev/en/application-form-step-0/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('h2').text
        #print(titulo)
        titles.append(titulo)


        links.append('https://fundinnovation.dev/en/application-form-step-0/')

        text = soup.find('div', class_= 'block-type-text').find('div', class_ = 'container-small').get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split()).strip()
        #print(text)
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
        df['opo_deadline'] = '31 de dezembro de 20' + ano
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'fundinnovation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em fundinnovation1')


def fundinnovation3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fundinnovation_03.csv'
        req = Request('https://fundinnovation.dev/en/#about', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='col col-md-5')
        titulo = clean(soup.find('h2').text)
        titulos.append(titulo)
        texto = clean(soup.find('p').get_text())
        textos.append(texto)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['fundinnovation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = ['https://fundinnovation.dev/en/#about'] 
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'fundinnovation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em fundinnovation3')
