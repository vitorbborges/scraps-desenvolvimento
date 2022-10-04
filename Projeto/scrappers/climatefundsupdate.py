# AB#48
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from itertools import compress
from urllib.request import Request, urlopen

def climatefundsupdate2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\climatefundsupdate_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://climatefundsupdate.org/news/newcategory/news-cat/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('a', rel = "bookmark")
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for link in soup2.find_all('a'):
            info = (link['href'])
            links.append(info)

        new_links = getNewInfo(links_base, links)

        if(new_links):
            for link in links:
                page = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h3', class_ = "entry-title").get_text()
                texto = soup.find('div', class_ = "entry-content").get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
        
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'climatefundsupdate_')
        df.to_csv(path + filename, index = False)
    
    except Exception as e:
        print(e)
        print('Erro em climatefundsupdate2')
        
# climatefundsupdate2('.')


def climatefundsupdate4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\climatefundsupdate_04.csv'
        titulos = []
        links = []
        values = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_response = requests.get('https://climatefundsupdate.org/the-funds').content.decode('utf-8')
        soup = BeautifulSoup(link_response, 'lxml')
        table = soup.find('table')
        table_str = str(table) #converter para string
        df  = pd.read_html(table_str)[0] # Criando o dataframe a partir da tabela em HTML
        # print(df.columns)
        df = df.rename(columns={'Fund': 'prj_instituicao', 'Project': 'prj_titulo','Disbursement (USD mn)':'prj_valor'})
        df = df.drop(columns=['Fund focus','Fund Type', 'Number of projects approved','Pledge (USD mn)','Deposit (USD mn)', 'Approval (USD mn)'])

        for prj in soup.find_all('tr'):
            if(prj.find('a') is not None):
                link = prj.find('a')['href']
                # print(link)
                links.append('https://climatefundsupdate.org'+link)

        df['link'] = links 
        df['prj_brazil'] = ['N']*len(df.index)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'climatefundsupdate_')
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em climatefundsupdate4')

# climatefundsupdate4('.')

