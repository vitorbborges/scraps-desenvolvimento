# AB#60
from fileinput import filename
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
import requests
from utilidadesppf import clean, getCodList
import shutil


# LIST
#opo_titulo --
#link --
#opo_deadline --
#opo_texto --
#opo_tipo 
#opo_brazil 
#codigo --
#atualizacao --


def itto1(path, keywords = '(brazil|latin america region)'):
    try:
        #------------------------------------------
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        titles = []
        links = []
        deadlines = []
        filename = '\\itto_01.csv'
        texts = []
        types = []
        hasBrazil = []
        dia = datetime.today().strftime('%y%m%d')
        #----------------------------------------------
        main_link = 'https://www.itto.int/'
        page = requests.get('https://www.itto.int/').content.decode('utf-8')
        main_soup = BeautifulSoup(page, 'lxml')
        pre_soup = main_soup.find('div', id = 'contents1002012')
        opo_list = pre_soup.find('div', class_ = 'list-group')
        for raw_link in opo_list.find_all('a')[:-1]:
            link = raw_link['href']
            title = raw_link.text       
            titles.append(title)
            print(raw_link)
            #if(link not in links and link != '#'):
                #links.append(link)
        print(links)
        if(links):
            page = requests.get(links[0]).content.decode('utf-8')
            soup = BeautifulSoup(page, 'lxml')
            for opo in soup.find_all('div', class_ = 'row news_list'):
                deadlines.append(opo.find_all('p')[3].text)
                text = str(opo.find_all('p')[1].text) + str(opo.find_all('p')[2].text)
                texts.append(text)
                if len(findall('grant', text.lower())):         
                        types.append('grant')                
                elif len(findall('fellowship', text.lower())):  
                    types.append('fellowship')          
                elif len(findall('scholarship', text.lower())): 
                    types.append('scholarship')                   
                else:
                    types.append('other')
                if(findall(keywords, text.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
                    
            df = pd.DataFrame()
            df['opo_titulo'] = titles
            df['link'] = links
            df['opo_texto'] = texts
            df['opo_texto_ele'] = texts
            df['opo_brazil'] = hasBrazil
            df['opo_tipo'] = types
            df['opo_deadline'] = deadlines
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'roddenberry_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index=False)
            
        else:
            shutil.copy(path+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em itto1')


def itto3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        links = ['https://www.itto.int/about_itto/', 'https://www.itto.int/focus_areas/', 'https://www.itto.int/membership_information/']
        filename = '\\itto_03.csv'
        for link in links:
            page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = clean(soup.find('h1').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', id = 'main_contents').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['itto']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'itto_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em itto3')