#AB #30

import bs4
from bs4 import BeautifulSoup
import re
from lxml import etree
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

#https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/


def govbrmj3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\govbrmj_03.csv'
        titulos = []
        textos = []
        links = ['https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/']

        page = Request('https://www.gov.br/mj/pt-br/assuntos/seus-direitos/consumidor/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('span', id = 'breadcrumbs-current').get_text()
        texto = soup.find('h3', class_ = 'mceContentBody documentContent template-document_view portaltype-document site-pt-br section-assuntos subsection-seus-direitos subsection-seus-direitos-consumidor subsection-seus-direitos-consumidor-copy_of_o-que-e-senacon icons-on userrole-authenticated userrole-site-administrator userrole-member userrole-contributor userrole-editor userrole-reader userrole-owner userrole-reviewer').get_text()
        titulos.append(titulo)
        textos.append(clean(texto))
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['govbr']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'govbrmj_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
            print(e)
            print('Erro em govbrmj3')
        
#govbrmj3('.')


