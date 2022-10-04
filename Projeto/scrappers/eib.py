import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import os

# eib2 protegido por javascript;

def eib3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\eib_03.csv'
        titulos = []
        textos = []
        links = ['https://www.eib.org/en/about/index.htm']
        for i in links:
        
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            titulo = soup.find('h1').get_text()
            titulos.append(titulo)
            texto = soup.find('div', class_ = 'text-left').get_text()
            texto2 = soup.find('div', class_ = 'banner__text--not-full-width float-right').get_text()
            textos.append(clean(texto) + clean(texto2))
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['eib']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'eib_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em eib3')
        
#eib3(os.getcwd())

#eib4
        
if __name__ == '__main__':

    dia = datetime.today().strftime('%y%m%d')
    ano = datetime.today().year
    filename = '/eib_04.csv'
    links = []
    titulos = []
    textos = []
    valor = []
    prj_inst = []
    hasBrazil = []
    
    parser = 'html.parser'
    resp = urllib.request.urlopen('https://www.eib.org/en/projects/loans/index.htm?q=&sortColumn=loanParts.loanPartStatus.statusDate&sortDir=desc&pageNumber=0&itemPerPage=25&pageable=true&language=EN&defaultLanguage=EN&loanPartYearFrom=1959&loanPartYearTo=2021&orCountries.region=true&orCountries=true&orSectors=true')
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    
    for link in soup.find_all('a', href=True):
        print(link['href'])
