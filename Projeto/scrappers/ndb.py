# AB#125
import bs4
import utilidadesppf
from bs4 import BeautifulSoup
import pandas as pd
import re
from lxml import etree
from re import findall
import requests
from datetime import datetime
from itertools import compress
import shutil
from utilidadesppf import getCodList, clean, getInfoBase
from urllib.request import Request, urlopen


def ndb2(path):
    try:
        # pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/ndb_02.csv'
        titulos = []
        textos = []
        links = []
        # links_base = getInfoBase(pathbase, filename, 'link')
        req = Request('https://www.ndb.int/newsroom/press_release/', headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(req).read()
        soup = BeautifulSoup(page_request, 'lxml')
        soup = soup.find('div', class_='data-doc-panel')
        soup = BeautifulSoup(str(soup.find_all('div',class_="data-doc-col-main")), 'lxml')
        # print(soup)

        for i in soup.find_all('a'):
            b = i['href']

            links.append(b)


        for i in links:
            req = Request(i, headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(req).read()
            soup = BeautifulSoup(page_request, 'lxml')

            titulo = clean(soup.find('h4').get_text())
            #print(titulo)
            texto = clean(soup.find('div', class_='press-release-part').get_text())
            titulos.append(titulo)
            textos.append(texto)




        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'ndb_')
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em ndb2')

# ndb2('.')


def ndb4(path, keywords = '(latin american region|brazil)'):
    try:
        links = []
        dia = datetime.today().strftime('%y%m%d') #setando o dia
        #page = requests.get('https://www.ndb.int/projects/list-of-all-projects/approved-projects/')  #pegando o response da pagina
        req = Request('https://www.ndb.int/projects/list-of-all-projects/approved-projects/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find('table') #busca pela tabela
        df = pd.read_html(str(table))[0]

        for link in table.find_all('a'): #busca por links
            links.append(link['href']) #adiciona à lista


        df = df.drop([r'BORROWER / INVESTEE / RECIPIENT', r'TARGET SECTOR'], axis = 1) #informações irrelevantes
        df = df.rename(columns={'PROJECT NAME' : 'prj_titulo', r'LOAN / INVESTMENT / COMMITMENT AMOUNT' : 'prj_valor'}) #mudando nome da coluna
        path = path + '''\\ndb_04.csv'''

        b = df['prj_titulo'].str.contains('Brazil')
        hasBrazil = ['Y' if x==True else 'N' for x in b]
        df['prj_brazil'] = hasBrazil
                
        df['link'] = links
        df['prj_instituicao']=['NDB']*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'ndb_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path, index = False)
    except Exception as e:
        print(e)
        print('Erro em ndb 4')

# ndb4('.')