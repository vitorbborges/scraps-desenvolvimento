# AB#95
from utilidadesppf import getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
from urllib.request import Request, urlopen

def waittfoundation1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\waittfoundation_01.csv'
        titles = [] #
        deadlines = [] #
        texts = [] #
        hasBrazil = [] #
        types = [] #
        eleg = []
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime('%y'))
        page_request = requests.get('https://www.waittfoundation.org/copy-of-roc-grants').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        text = clean(page_soup.find('div', id = 'Containerd0dla').get_text())
        texts.append(text)
        titulo = clean(page_soup.find('span', style ='color:#000000;').get_text())
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

        eleg_text = clean(page_soup.find('div', id = 'comp-kdz52nvd1').get_text())
        eleg.append(eleg_text)

        deadline = '31 de dezembro de ' + ano
        deadlines.append(deadline)
        df = pd.DataFrame()          
        df['opo_titulo'] = titles  
        df['link'] = ['https://www.waittfoundation.org/copy-of-roc-grants']    
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = eleg
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'waittfoundation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em waittfoundation1')


def waittfoundation3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.waittfoundation.org/about-1', 'https://www.waittfoundation.org/national-geographic-society-grants']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\waittfoundation_03.csv'

        page = requests.get(links[0]).text
        soup = BeautifulSoup(page, 'lxml')
        titulo = links[0].split('.org/')[1].split('-')[0]
        titulos.append(titulo)
        texto = ''
        for i in soup.find_all('p', class_='font_7'):
            texto += i.text
        textos.append(clean(texto))

        page = requests.get(links[1]).text
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find_all('h2', class_='font_2')[1].text)
        titulos.append(titulo)
        texto = ''
        for i in soup.find_all('p', class_='font_8'):
            texto += i.text
        textos.append(clean(texto))
        
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['waittfoundation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'waittfoundation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em waittfoundation3')

