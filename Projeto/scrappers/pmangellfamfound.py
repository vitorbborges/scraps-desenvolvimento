import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import requests
import pandas as pd
import urllib
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo

def pmangellfamfound1(path, keywords = 'brazil'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().year
        filename = '\\pmangellfamfound_01.csv'
        links = []
        titulos = []
        textos = []
        deadlines = []
        hasBrazil = []
        tipos = []
        scrape = []
        texto_elegivel = []
        page = Request('https://pmaff.wpengine.com/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        site = soup.find('a', class_ = 'more-link')
        soup2 = BeautifulSoup(str(site), 'lxml')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        page2 = Request(links[0], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request2 = urlopen(page2).read()
        soup3 = BeautifulSoup(page_request2, 'lxml')
        titulo = soup3.find('h1', class_ = 'entry-title').get_text()
        scrape.append(str(soup3))
        titulos.append(titulo)
        texto = soup3.find('div', class_ = 'entry-content').get_text()
        textos.append(texto)
        texto_elegivel.append(texto)
        ddln = soup3.find('p').get_text()
        deadline = soup3.find(text=re.compile(r'The deadline (.*?)CDT'))
        deadlines.append(deadline)
        if(findall(keywords, texto.lower())):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
        if(findall('grant', texto.lower())):         
            tipos.append('grant')                
        elif(findall('fellowship', texto.lower())):  
            tipos.append('fellowship')          
        elif(findall('scholarship', texto.lower())): 
            tipos.append('scholarship')                   
        else:
            tipos.append('other')

        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_texto'] = textos 
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['opo_deadline'] = deadline
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'pmangellfamfound_')
        df['atualizacao'] = [dia]*len(links)
        #df['html'] = scrape
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em pmangellfamfound1')
        
#pmangellfamfound1('.')

def pmangellfamfound3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\pmangellfamfound_03.csv'
        titulos = []
        textos = []
        links = ['http://pmangellfamfound.org/about-us/', 'http://pmangellfamfound.org/for-applicants/what-we-fund/']

        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            titulo = soup.find('h1', class_ = 'entry-title').get_text()
            texto = soup.find('div', class_ = 'entry-content').get_text()
            titulos.append(titulo)
            textos.append(clean(texto))
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['pmangellfamfound']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'pmangellfamfound_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em pmangellfamfound3')
        
#pmangellfamfound3('.')

def pmangellfamfound4(path, keywords = '(brazil|latin america region)'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\pmangellfamfound_04.csv'
        titulos = []
        valor = []
        hasBrazil = []
        prj_inst = []
        links = []
        page = Request('http://pmangellfamfound.org/?sfid=139', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('a', class_ = 'entry-title-link')
        soup2 = BeautifulSoup(str(sites), 'lxml')

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)
            
        for i in links:
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            titulo = soup3.find('h1', class_ = 'entry-title').get_text()
            titulos.append(titulo)
            value = soup3.find('div', class_ = 'entry-content').get_text()
            valor2 = re.search('\$(.*)\|', str(value))
            valor2 = valor2.group(0).split("|", 1)[0]
            valor2 = re.sub("\D", "", valor2)
            valor.append('$ ' + valor2)
            instituicao = 'pmangellfamfound'
            prj_inst.append(instituicao)
            hasBrazil.append('N')    
            
        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = links
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = valor
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'pmangellfamfound_')
        df.to_csv(path+filename, index=False)
    
    except Exception as e:
        print(e)
        print('Erro em pmangellfamfound4')
        
#pmangellfamfound4('.')
