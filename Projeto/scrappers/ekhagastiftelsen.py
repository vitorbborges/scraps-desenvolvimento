# AB#40
# AB#148
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList
from re import findall
from utilidadesppf import getInfoBase, getNewInfo, clean
import shutil
from urllib.request import Request, urlopen


def ekhagastiftelsen3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\ekhagastiftelsen_03.csv'
        titulos = []
        textos = []
        links = ['https://www.ekhagastiftelsen.se/eng/vem.shtml', 'https://www.ekhagastiftelsen.se/eng/instruktioner.shtml', "https://www.ekhagastiftelsen.se/eng/budget.shtml", 'https://www.ekhagastiftelsen.se/eng/rapportering.shtml', 'https://www.ekhagastiftelsen.se/eng/utbetalning.shtml']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'section-heading').find('h3').get_text()
            texto = soup.find('div', class_ = 'col-md-12').get_text()
            titulos.append(clean(titulo))
            textos.append(clean(texto))
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['ekhagastiftelsen']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'ekhagastiftelsen_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em agropolis3')   

def ekhagastiftelsen4(path): 
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = []
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        values = []
        scrape = []
        texto_elegivel = []
        filename = '\\ekhagastiftelsen_04.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://www.ekhagastiftelsen.se/eng/anslag.shtml', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sopa = soup.find('table', class_='table')

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
        
            if info.startswith('http://'):
                links.append(info)
            else: 
                info = 'https://www.ekhagastiftelsen.se/eng/' + info
                links.append(info)


        for i in links: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            titulo = soup3.find('div', class_='col-md-12').find('h5').text
            titulos.append(clean(titulo))
            value = soup3.find('tbody').find_all('td')[-1].text
            values.append(clean(value))

    
        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = links 
        df['prj_instituicao'] = ['Ekhagastiftelsen']*len(df.index)
        df['prj_valor'] = values
        df['prj_brazil'] = ['N']*len(df.index)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'ekhagastiftelsen_')
        df.to_csv(path+filename, index=False)

        
    except Exception as e:
        print(e)
        print('Erro em ekhagastiftelsen4')
