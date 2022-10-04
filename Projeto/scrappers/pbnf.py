# AB#19
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
from utilidadesppf import getCodList

def pbnf1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\pbnf_01.csv'
        titles = []
        links = []
        deadlines = []
        texts = []
        hasBrazil = []
        types = []
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        link = 'https://www.pbnf.nl/grantseekers/'
        #------------------------------------------------
        page = requests.get(link).content.decode('UTF-8')
        page_soup = BeautifulSoup(page, 'lxml')
        tam = 0
        title = 'PBNF Grant'
        for main_soup in page_soup.find_all('div', {'style': 'flex-basis:50%', 'class': 'wp-block-column'}):
            tam += 1
            links.append(link)
            titles.append(title)
            #-----------TITLES---------------
            df = pd.DataFrame()
            text = ''
            for p in main_soup.find_all('p', class_ = ''):
                #------------TEXTOS-------------
                new_text = p.text
                #--------------DEADLINES-------------
                if findall('closes on', new_text.lower()):
                    raw_dead = new_text.split('closes on')[1]
                    raw_dead = raw_dead.split(' ')
                    deadline = ' '.join(raw_dead[i] for i in range(3))
                    deadline = re.sub(',', '', deadline)
                text+=new_text
            #-------------ELEGTEXT---------------------
            eleg_text = ''
            for tagtext in main_soup.find_all('strong'):
                track = tagtext
                if(findall('eligible', tagtext.text.lower())):
                    for _ in range(10):
                        eleg_text+=track.text
                        track = track.findNext('p')
            eleg_texts.append(eleg_text)
            #--------------TIPO----------------
            if len(findall('grant', text.lower())):         
                types.append('grant')                
            elif len(findall('fellowship', text.lower())):  
                types.append('fellowship')          
            elif len(findall('scholarship', text.lower())): 
                types.append('scholarship')                   
            else:
                types.append('other')
            #--------------BRAZIL-------------------
            if findall(keywords, text.lower()):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            deadlines.append(deadline)
            texts.append(text)
        df['opo_titulo'] = titles
        df['link'] = links
        df['opo_deadline'] = deadlines
        df['opo_texto'] = texts
        df['opo_texto_ele'] = eleg_texts
        df['opo_tipo'] = types
        df['opo_brazil'] = hasBrazil
        df['codigo'] = getCodList(dia, tam, '_1_', filename)
        df['atualizacao'] = [dia]*tam
        df.to_csv(path+filename, index=False)
            


    except Exception as e:
        print(e)
        print('Erro em pbnf1')
        
#pbnf1(os.getcwd())