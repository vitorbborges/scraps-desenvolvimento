# AB#138
from requests.sessions import TooManyRedirects
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
import os

def twas1(path, keywords = '(brazil|latin america region|developing countries)'):
    try:
        filename = '\\twas_01.csv'
        titles = [] 
        links = []
        main_links = ['https://twas.org/opportunities/prizes-and-awards', 'https://twas.org/opportunities/research-grants', 'https://twas.org/opportunities/fellowships/phd', 'https://twas.org/opportunities/fellowships/postdoc'] #
        texts = [] #
        eleg_texts = []#
        hasBrazil = []# 
        types = [] #
        deadlines = []#
        dia = datetime.today().strftime("%y%m%d")
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        for link in main_links:
            request = requests.get(link).content.decode('utf-8')
            soup = BeautifulSoup(request, 'lxml')
            content = soup.find_all('div', class_ = 'view-content')[2]
            for opo in content.find_all('div', recursive=False):
                opo_link = 'https://twas.org/' + opo.find('a')['href']
                links.append(opo_link)
            if(soup.find('a',title =  'Go to next page')):
                main_links.append('https://twas.org/' + soup.find('a', title = 'Go to next page')['href'])
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                eleg_text = ''
                text = ''
                request = requests.get(link).content.decode('utf-8')
                soup = BeautifulSoup(request, 'lxml')
                #--------------------------------------------------------
                titulo = soup.find('div', class_= 'field-item even').text.strip()
                titles.append(titulo)
                #--------------------------------------------------------
                deadline = soup.find('div', class_ = 'deadline').find('div', class_ = 'value').text
                if(not deadline or deadline == 'None'):
                    deadline = 'Sem deadline'
                deadlines.append(deadline)
                #--------------------------------------------------------
                text += soup.find_all('div', class_= 'field-items')[1].get_text().strip()
                text += soup.find_all('div', class_= 'field-items')[2].get_text().strip()
                text = re.sub('\n', ' ', text)
                texts.append(text)
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
                #--------------------------------------------------------
                for tagtext in soup.find_all(['h4', 'strong']):
                    if(tagtext.text == 'Eligibility'):
                        track = tagtext.findNext()
                        while(track.name != 'h4' and track.name != 'strong'):
                            eleg_text += re.sub('\n', ' ', track.get_text())
                            track = track.findNext()
                        if(track.name == 'h4' or track.name == 'strong'):
                            break
                if(eleg_text == ''):
                    eleg_text = text
                eleg_texts.append(eleg_text)
            df = pd.DataFrame()          
            df['opo_titulo'] = titles  #
            df['link'] = new_links#
            df['opo_texto'] = texts   
            df['opo_texto_ele'] = eleg_texts
            df['opo_brazil'] = hasBrazil   
            df['opo_tipo'] = types      
            df['opo_deadline'] = deadlines#
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'twas_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em twas1')

#twas1(os.getcwd())

def twas2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\twas_02.csv'
        titulos = []
        textos = []
        links = []
        toggle = True
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://twas.org/news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find_all('div', class_='view-content')[4]
        for link in soup.find_all('a'):
            if(toggle):
                links.append('https://www.twas.org/' + link['href'])
            toggle = not toggle
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                page_soup = page_soup.find('div', class_='cat1')
                titulo = clean(page_soup.find('h2').text)
                titulos.append(titulo)
                texto = clean(page_soup.find('div', class_='field field-name-body field-type-text-with-summary field-label-hidden').get_text())
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'twas_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em twas2')
        
#twas2(os.getcwd())