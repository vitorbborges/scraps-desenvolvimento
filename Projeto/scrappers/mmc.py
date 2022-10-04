# AB#113
from utilidadesppf import getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
from urllib.request import Request, urlopen
def mmc1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\mmc_01.csv'
        titles = [] #
        deadlines = [] #
        texts = [] #
        hasBrazil = [] #
        types = [] #
        dia = datetime.today().strftime("%y%m%d")
        page_request = requests.get('https://www.mmc.gov/grants-and-research-survey/current-funding-opportunities/').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        titulo = clean(page_soup.find('h1', class_='heading').text)
        titles.append(titulo)
        text = clean(page_soup.find('article', class_='content').get_text())
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
        deadline = page_soup.find('section', class_='article-box-section').find('p').text
        deadlines.append(deadline)
        df = pd.DataFrame()          
        df['opo_titulo'] = titles  
        df['link'] = ['https://www.mmc.gov/grants-and-research-survey/current-funding-opportunities/']    
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'mmc_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em mmc1')


def mmc3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.mmc.gov/about-the-commission/our-mission/marine-mammal-protection-act/', 'https://www.mmc.gov/about-the-commission/our-mission/endangered-species-act-and-other-legislation-and-agreements/', 'https://www.mmc.gov/about-the-commission/commission-policies/', 'https://www.mmc.gov/priority-topics/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\mmc_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='heading').text)
            titulos.append(titulo)
            texto = clean(soup.find('article', class_='content').get_text())
            textos.append(texto)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['mmc']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'mmc_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em mmc3')
