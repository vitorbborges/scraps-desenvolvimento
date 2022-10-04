import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import pandas as pd
from re import findall

def microsoftai3(path):
    try:

        dia = datetime.today().strftime('%y%m%d')
        filename = '\\microsoftai_03.csv'
        titulos = []
        textos = []
        links = ['https://www.microsoft.com/en-us/ai/ai-for-earth-grants']
        page = requests.get(links[0]).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        
        titulos.append(soup.find('div', class_="m-area-heading").find('h2').text)
        textos.append(soup.find('div', class_="m-area-heading").find_all('p')[1].text)
        
        for i in soup.find_all('div', class_="m-content-placement x-clearfix")[0].find_all('h3'):
            titulos.append(i.text)
            
        for i in soup.find_all('div', class_="m-content-placement x-clearfix")[0].find_all('div', class_="c-paragraph"):
            textos.append(clean(i.text))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['microsoftai']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'microsoftai_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em microsoftai3')
        
def microsoftai4(path, keywords = '(brazil|latin america region)'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\microsoftai_04.csv'
        titulos = []
        textos = []
        hasBrazil = []
        
        url = 'https://microsoft.github.io/AIforEarth-Grantees/'
        page = requests.get(url).content.decode('UTF-8')
        soup = soup = BeautifulSoup(page, 'lxml')
        
        title_html = soup.find('ul').find_all('h3')
        
        for i in range(0,len(title_html), 2):
            txt = title_html[i].text +' - '+ title_html[i+1].text
            titulos.append(txt)
        
        text_html = soup.find('ul').find_all('p')
        
        for i in range(1,len(text_html), 2):
            text = text_html[i].text
            textos.append(text)
            if(findall(keywords, text.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
        
        link_html = soup.find('ul').find_all('a')[1:-1]
        links = [l['href'] for l in link_html]
        instituicao = 'microsoftai'
        value = 'Não Econtrado.'
        
        df = pd.DataFrame()
        df['prj_titulo'] = titulos
        df['link'] = links
        df['prj_instituicao'] = [instituicao]*len(df.index)
        df['prj_valor'] = [value]*len(df.index)
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'microsoftai_')
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em microsoftai4') 
