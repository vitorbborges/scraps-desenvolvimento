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

def govuk1(path, keywords = '(brazil|latin america region)'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\govuk_01.csv'
        links = []
        titulos = []
        textos = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        page = Request('https://ltsi.flexigrant.com/default.aspx', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        scrape.append(str(soup))
        conteudo = soup.find('div', id = 'MainContent_ContentInline_litContent')
        
        for i in soup.find_all('h2'):
            titulos.append(i.get_text())
        titulos = titulos[1:4]
        
        for i in titulos:
            links.append('https://ltsi.flexigrant.com/default.aspx')
            
        
        for i in soup.find_all('h2'):
            texto = i.find_next('p').get_text()
            if i.find_next('p').find_next('p') is not None:
                texto2 = i.find_next('p').find_next('p').get_text()
            else:
                texto2 = ''
            if i.find_next('ul') is not None:
                texto3 = i.find_next('ul').get_text()
            else: 
                texto3 = ''
            textos.append(texto + texto2 + texto3)
            
            
        textos = textos[1:4]
        textos = ([re.sub(r'\W',' ', i) for i in textos]) #muito bom
        deadlines = ['Deadline não econtrada']*len(titulos)
        elegibilidade = ['N']*len(titulos)
        tipos = ["grants"]*len(titulos)
        
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        #df['html'] = scrape
        df['opo_deadline'] = deadlines 
        df['opo_texto'] = textos 
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['opo_brazil'] = elegibilidade
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'govuk_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
            
    except Exception as e:
        print(e)
        print('Erro em govuk1')
        
#govuk1(os.getcwd())

def govuk2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\govuk_02.csv'
        titulos = []
        textos = []
        links = []
        links2 = []
        page = Request('https://www.gov.uk/search/news-and-communications', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('div', class_ = 'finder-results js-finder-results')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.findAll('a'):
            info = ('https://www.gov.uk' + i['href'])
            links.append(info)
    
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for link in new_links:
                page = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1', class_ = 'gem-c-title__text govuk-heading-l').get_text()
                texto = soup.find('div', class_ = 'gem-c-govspeak govuk-govspeak direction-ltr').get_text()
                titulos.append(clean(titulo))
                textos.append(clean(texto)[:32667])
        else:
            print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'govuk_')
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em govuk2')
        
#govuk2(os.getcwd())


