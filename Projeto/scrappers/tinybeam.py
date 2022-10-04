# AB#136
from utilidadesppf import getNewInfo, getInfoBase, getCodList
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from itertools import compress
from urllib.request import Request, urlopen


def tinybeamfund1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\tinybeamfund_01.csv'
        titles = [] 
        links = ['https://tinybeamfund.org/Grant-Recipients/', 'https://tinybeamfund.org/burning-questions-initiative/fellowship-awards/'] #
        texts = [] 
        hasBrazil = [] 
        types = ['grant', 'fellowship'] 
        deadlines = []
        dia = datetime.today().strftime("%y%m%d")
        for link in links:
            page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_soup = BeautifulSoup(page.text, 'lxml')
            titulo = page_soup.find_all('div', class_= 'blockContents')
            titles.append(titulo)
            text = ''
            text_area = page_soup.find('div', class_= 'blockContents')
            for li in text_area.find_all('p'):
                text +=li.text
            texts.append(text)
            if(findall(keywords, text.lower())):
                        hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            #deadline = page_soup.find('div', class_ = 'callout').find('p').text
            #deadline = deadline.replace("(", "").replace(")", "")
            #deadlines.append(deadline)
        df = pd.DataFrame()          
        df['opo_titulo'] = titles  
        df['link'] = links
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        #df['opo_deadline'] = deadlines
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'tinybeamfund_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em tinybeamfund1') 

# tinybeamfund1('.')