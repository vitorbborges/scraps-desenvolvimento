import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
from itertools import compress
import shutil
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import urllib
from urllib.request import Request, urlopen
import os

def daad1(path, keywords='brazil'):    
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().year
        filename = '\\daad_01.csv'
        links = []
        titulos = []
        textos = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        i = 1
        titulotopo = ''
        toggle = True
        links_base = getInfoBase(pathbase, filename, 'link')
        
        while toggle == True:
            link = 'https://www.daad.org.br/pt/bolsas/busca/?type=a&origin=48&subjectgroup=0&q=0&status=0&page=0&onlydaad=&language=en&id=0&pg=' + str(i)
            page = requests.get(link)
            soup = BeautifulSoup(page.text, 'lxml')
        
            if titulotopo == soup.find('h3').text:
                #print('acabou')
                break
            i += 1
            titulotopo = soup.find('h3').get_text()
            pre_soup = soup.find_all('h3')
            soup2 = BeautifulSoup(str(pre_soup), 'lxml')
            #print(i)
            for link in soup2.find_all('a'):
                links.append('https://www.daad.org.br/pt/bolsas/busca/' + link['href'])
        
        new_links = getNewInfo(links_base, links) 
        if(new_links):
            for link in new_links:
                page = requests.get(link)
                soup = BeautifulSoup(page.text, 'lxml')
                scrape.append(str(soup))
                titulo = soup.find('h2', dir='ltr').get_text()
                texto = soup.find('div', class_="scholarship-detail").get_text()
                gtit = texto.lower()
                if ('grant' in gtit):
                    tipos.append('grant')
                elif ('fellowship' in gtit):
                    tipos.append('fellowship')
                elif ('scholarship' in gtit):
                    tipos.append('scholarship')
                elif ('award' in gtit):
                    tipos.append('award')
                else:
                    tipos.append('other')
                elegibilidade.append("Y")
                titulos.append(titulo)
                texto = clean(texto)
                textos.append(texto)
                texto_elegivel.append(texto)
                deadlines.append('31 de dezembro de ' + str(ano))   
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        #df['html'] = scrape
        df['link'] = new_links
        df['opo_deadline'] = deadlines
        df['opo_texto'] = textos
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['opo_brazil'] = elegibilidade
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'daad_')
        df['atualizacao'] = [dia]*len(new_links)
        df.to_csv(path+filename, index=False)
    
    except Exception as e:
        print(e)
        print('Erro em daad1')

#daad1(os.getcwd())

def daad2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/daad_02.csv'
        titulos = []
        textos = []
        links = []
        page = 'http://www.daad.org.br/pt/quem-somos/noticias/'
        page_request = requests.get(page)
        soup = BeautifulSoup(page_request.text, 'lxml')
        sites = soup.find_all('div', class_ = "teaser two-column-teaser")
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')
        
        for link in soup2.find_all('a'):
            info = (link['href'])
            links.append(info)
        
        for link in links:
            page = requests.get(link).content.decode('utf-8')
            page_soup = BeautifulSoup(page, 'lxml')
            titulo = page_soup.find('title').get_text()
            texto = BeautifulSoup(str(page_soup.find('div', class_ = "site-main col-md-8")), 'lxml').get_text()
            textos.append(clean(texto))
            titulos.append(clean(titulo))
            
        
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'daad')
        df.to_csv(path+filename, index=False)
    
    except Exception as e:
        print(e)
        print('Erro em daad2')
        
#daad2(os.getcwd())

def daad3(path): 
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '/daad_03.csv'
        links = ['https://www.daad.org.br/pt/quem-somos/sobre-o-daad/']
        titulos = []
        textos = []
        page = 'https://www.daad.org.br/pt/quem-somos/sobre-o-daad/'
        page_request = requests.get(page)
        soup = BeautifulSoup(page_request.text, 'lxml')
        titulo = clean(soup.find('div', class_ = "site-headline col-sm-12").get_text())
        texto = clean(soup.find('div', class_ = "site-main col-md-8 general-template").get_text())
        titulos.append(titulo)
        textos.append(texto)
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['daad']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'daad_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em daad3')

#daad3(os.getcwd())