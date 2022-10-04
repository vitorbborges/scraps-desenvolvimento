# AB#147
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList, clean
from re import findall
from urllib.request import Request, urlopen
def oceantrainingpartnership1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\oceantrainingpartnership_01.csv'
        titles = [] 
        links = [] 
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        ano = '20' + str(datetime.today().strftime('%y'))
        dia = datetime.today().strftime("%y%m%d")
        link_page = 'http://www.oceantrainingpartnership.org/opencall' + ano
        #print(link_page)
        page_response = requests.get(link_page).content.decode('utf-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = soup.find('h1', class_='page-title').text
        titles.append(clean(titulo))
        #print(titles)
        links.append('http://www.oceantrainingpartnership.org/opencall' + ano)

        deadline = soup.find('span', class_ = 'date-display-range').find('span', class_='date-display-end').text
        deadlines.append(deadline)

        text = soup.find('div', class_ = 'content').get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split())
        texts.append(text)



   
        eleg_text = ''
        for h2 in soup.find_all('h2'):
            if('who' in h2.text.lower().split()):
                track = h2.findNext()
                eleg_text = track.get_text()
                break
        eleg_texts.append(eleg_text)
            

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
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'oceantrainingpartnership_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em oceantrainingpartnership1')


def oceantrainingpartnership3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oceantrainingpartnership_03.csv'
        req = Request('http://www.oceantrainingpartnership.org/about', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1', class_='page-title').text)
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='field-item even').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['oceantrainingpartnership']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = ['http://www.oceantrainingpartnership.org/about']
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'oceantrainingpartnership_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em oceantrainingpartnership3')
