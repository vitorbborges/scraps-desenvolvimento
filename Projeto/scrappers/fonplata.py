# AB#37
from distutils.log import error
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
from googletrans import Translator
from urllib.request import Request, urlopen
def fonplata1(path, keywords = '(brazil|latin america region|member countries of fonplata)'):
    try:
        filename = '\\fonplata_01.csv'
        titles = [] #
        links = [] #
        deadlines = [] #
        texts = [] #
        hasBrazil = [] #
        types = [] #
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        page_request = requests.get('https://www.fonplata.org/es/oportunidades/reclutamiento-de-personal').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        for opo in page_soup.find_all('div', class_='opportunity-pages-row views-row'):
            link = opo.find('a')['href']
            links.append('https://www.fonplata.org/'+link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page_request = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page_request, 'lxml')
                titulo = page_soup.find('div', class_='field field--name-node-title field--type-ds field--label-hidden field--item').find('h2').text
                titulo = re.sub('\\n', '', titulo)
                titles.append(titulo)
                deadline = page_soup.find('div', class_='field field--name-field-application-deadline field--type-datetime field--label-inline').find('time').text
                deadlines.append(deadline)
                text = page_soup.find('span', style = 'font-family:"Tahoma",sans-serif').text
                tradutor = Translator()
                #text = tradutor.translate(text).text
                #texts.append(text)
                eleg_text = page_soup.find('div', class_= 'text-work-opportunity field field--name-field-requirements-hr field--type-text-long field--label-hidden field--item').get_text()
                #eleg_text = tradutor.translate(eleg_text).text
                eleg_text = re.sub('\n', ' ', eleg_text)
                eleg_texts.append(eleg_text)

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

            df = pd.DataFrame()          
            df['opo_titulo'] = titles  
            df['link'] = new_links    
            df['opo_texto'] = text  
            df['opo_texto_ele'] = eleg_texts
            df['opo_brazil'] = hasBrazil   
            df['opo_tipo'] = types      
            df['opo_deadline'] = deadlines   
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'fonplata_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em fonplata1')

def fonplata2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fonplata_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.fonplata.org/es/noticias/listado').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for card in soup.find_all('div', class_ = 'fields-taxonomy views-row'):
            link = card.find('a')['href']
            links.append('https://www.fonplata.org/' + link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = page_soup.find('div', class_='field field--name-node-title field--type-ds field--label-hidden field--item').find('h2').text
                titulos.append(titulo)
                texto = ''
                text_area = page_soup.find('div', class_='body-news field field--name-body field--type-text-with-summary field--label-hidden field--item')
                for p in text_area.find_all('p'):
                    texto+=p.text
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'fonplata_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em fonplata2')



def fonplata3(path):
    try:
        instituicoes = []
        titulos = []
        textos = []
        links = ['https://www.fonplata.org/es/financiamiento/programa-de-cooperacion-tecnica', 'https://www.fonplata.org/es/financiamiento/modalidades-de-financiamiento', 'https://www.fonplata.org/es/financiamiento', 'https://www.fonplata.org/es/institucional/nuestra-historia', 'https://www.fonplata.org/es/institucional/mision-y-vision']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fonplata_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='page-title').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='region region-content').find('div', class_='content').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['fonplata']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'fonplata_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em fonplata3')
