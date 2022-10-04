# AB#79

import bs4
from bs4 import BeautifulSoup
import requests
import re
from re import findall
from datetime import datetime
import pandas as pd
from utilidadesppf import getCodList, clean
from urllib.request import Request, urlopen

def conservegrassland1(path, keywords = 'brazil'):
    try:
        filename = '\\conservegrassland_01.csv'
        titles = [] 
        links = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        ano = datetime.today().strftime('%y')
        page_response = requests.get('http://conservegrassland.org/our-programs/').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')

        links.append('http://conservegrassland.org/our-programs/')

        text = soup.find('div', class_="et_pb_section et_pb_section_1 et_section_regular").text
        text = re.sub('\n', ' ', text)
        text = clean(' '.join(text.split()).strip())
        texts.append(text)
        text_area = soup.find('div', class_='et_pb_row et_pb_row_1')
        top = text_area.find('h2').text
        titles.append(top)
        eleg_text = clean(text_area.find('strong').next_sibling)
        eleg_texts.append(eleg_text)
        

        text = soup.find('div', class_="et_pb_section et_pb_section_2 et_pb_with_background et_section_regular").get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split()).strip()
        texts.append(text)
        text_area = soup.find('div', class_='et_pb_row et_pb_row_3')
        top = text_area.find('h2').get_text()
        titles.append(top)
        eleg_text = clean(text_area.find('strong').next_sibling)
        eleg_texts.append(eleg_text)

        text = soup.find('div', class_="et_pb_section et_pb_section_3 et_section_regular").get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split()).strip()
        texts.append(text)
        text_area = soup.find('div', class_='et_pb_row et_pb_row_4')
        top = text_area.find('h2').get_text()
        titles.append(top)
        eleg_text = clean(text_area.find('strong').next_sibling)
        eleg_texts.append(eleg_text)

        for t in texts:
            if(findall(keywords, t.lower())):
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
        df['opo_titulo'] = pd.Series(titles)
        df['link'] = pd.Series(links)
        df['opo_texto'] = pd.Series(texts)   
        df['opo_texto_ele'] = pd.Series(eleg_texts)
        df['opo_brazil'] = pd.Series(hasBrazil)   
        df['opo_tipo'] = pd.Series(types)      
        df['opo_deadline'] = '31 de dezembro de 20' + ano
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'rufford_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em conservegrassland1')

def conservegrassland3(path):
    try:
        titulos = []
        textos = []
        links = ['http://conservegrassland.org/our-mission/', 'http://conservegrassland.org/where-we-work/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\conservegrassland_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('div', class_='et_pb_text_inner').find_all('h1')[1].text)
            titulos.append(titulo)
            texto = clean(soup.find_all('div', class_='et_pb_text_inner')[1].get_text())
            textos.append(texto)
        
        df = pd.DataFrame()
        df['pol_titulo'] = pd.Series(titulos)
        df['pol_texto'] = pd.Series(textos)
        df['link'] = pd.Series(links)
        df['pol_instituicao'] = ['conservegrassland']*len(df.index)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'conservegrassland_')
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em conservegrassland3')
