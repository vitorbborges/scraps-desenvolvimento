# AB#90

import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
from itertools import compress
import shutil
from utilidadesppf import getCodList, clean
from urllib.request import Request, urlopen
import os


def tinker1(path, keywords = '(latin american region|brazil)'):
    try:
        dia = datetime.today().strftime("%y%m%d")
        deadlines = [] #
        texts = [] #
        eleg_texts = []
        link = 'https://tinker.org/institutional-grants-apply-page/'
        page = requests.get(link).content
        main_soup = BeautifulSoup(page.decode('utf-8', errors='ignore'), 'lxml')
        
        titulos = []
        for i in main_soup.find_all('span', style='font-size: 22px; color: #43a5ff; font-weight: 600 !important;'):
            titulos.append(i.text)
        
        deadlines = []
        
        for i in main_soup.find_all('ul', class_='date'):
            
            deadlines.append(i.find_all('span')[3].text)
            
        text = main_soup.find('div', class_ = 'wpb_wrapper').find('p').text
        texts.append(text)
        eleg_text = main_soup.find('div', class_ = 'vc_column-inner vc_custom_1576522861854').get_text()
        eleg_text = re.sub('\n', ' ', eleg_text)
        eleg_text = re.sub("\s\s+" , " ", eleg_text)
        eleg_text = eleg_text.strip()
        eleg_texts.append(eleg_text)
        regions = str(main_soup.find_all('div', style = 'font-weight: 600 !important;'))
        if (findall(keywords, str(eleg_text).lower())):
            hasBrazil = 'Y'
        else:
            hasBrazil = 'N'
        
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['opo_texto'] = texts*len(deadlines)
        df['opo_texto_ele'] = eleg_texts*len(deadlines)
        df['link'] = [link]*len(deadlines)
        df['opo_brazil'] = [hasBrazil] * len(deadlines)
        df['opo_tipo'] = ['grant']*len(deadlines)
        df['opo_deadline'] = deadlines
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'tinker_')
        df['atualizacao'] = [dia]*len(df.index)
        path = path+'\\tinker_01.csv'
        df.to_csv(path, index = False)

    except Exception as e:
        print(e)
        print('Erro em tinker1')


#tinker1(os.getcwd())


def tinker3(path):
    try:
        titulos = []
        textos = []
        link = 'https://tinker.org/about-us/#overview'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\tinker_03.csv'
        soup = BeautifulSoup(requests.get(link).text, 'lxml')
        titulo = clean(soup.find('h3').text)
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='wpb_text_column wpb_content_element').findNextSibling().get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['tinker']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = [link]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'tinker_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em tinker3')
        
#tinker3(os.getcwd())

def tinker4(path, keywords = '(latin american region|brazil)'):
    try:
        links = []
        dia = datetime.today().strftime('%y%m%d') #setando o dia
        page = requests.get('https://tinker.org/grantee-database/')  #pegando o response da pagina
        soup = BeautifulSoup(page.text, 'lxml')
        page_number = soup.find('div', class_='dataTables_info').text
        page_number = int(re.findall(pattern='[0-9]+', string=page_number)[-1])
        page = requests.get(f'https://tinker.org/grantee-database/?order=desc&orderby=meeting_date&per_page={page_number}&filter_program=&filter_year=2020&filter_location=&search=')  #pegando o response da pagina
        soup = BeautifulSoup(page.text, 'lxml')
        table = soup.find('table', class_= 'tablepress tablepress-id-1 dataTable no-footer') #busca pela tabela
        toggle = True #evita pegar links repetidos (pega um, ignora outro...)
        i = 0
        for link in table.find_all('a'): #busca por links
            if toggle == True:
                links.append(link['href']) #adiciona à lista
            toggle = not toggle
            
        df = pd.read_html(str(table))[0]
        
        prj_brazil = []
        for i in df['Project Location']:
            if i == 'Brazil':
                prj_brazil.append('Y')
            else:
                prj_brazil.append('N')
        
        df = df.drop(['Project Duration (in months)', 'Program Area', 'Award Year', 'Project Location'], axis = 1) #informações irrelevantes   
         
        df = df.rename(columns={'Grantee': 'prj_instituicao', 'Project Title' : 'prj_titulo', 'Amount Awarded' : 'prj_valor'}) #mudando nome da coluna
        path = path + '''\\tinker_04.csv'''
        df['prj_brazil'] = prj_brazil
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'tinker_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path, index = False)
    except Exception as e:
        print(e)
        print('Erro em tinker 4')
        
#tinker4(os.getcwd())
