# AB#152
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re
from utilidadesppf import getCodList, getNewInfo, getInfoBase, clean
from re import findall
import requests
import shutil
from urllib.request import Request, urlopen
import os



def internationalclimateinitiative1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\internationalclimateinitiative _01.csv'
        titles = [] 
        deadlines = []
        links = ['https://www.international-climate-initiative.com/en/project-funding/information-for-applicants/iki-medium-grants/', 'https://www.international-climate-initiative.com/en/project-funding/information-for-applicants/iki-small-grants'] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eligibilities = []
        dia = datetime.today().strftime("%y%m%d")
        for link in links:
            request = requests.get(link).content.decode('UTF-8')
            soup = BeautifulSoup(request, 'lxml')
            titulo = soup.find('main').find('h2').text
            titles.append(clean(titulo))
        
        
            deadlines.append('Deadline não encontrada.')
        
            text = soup.find('div', class_='col col-sm-7').get_text()
            text = re.sub('\n', ' ', text)
            text = ' '.join(text.split())
            texts.append(text)
            
            eligibility = soup.find('div', class_='box box-sand').get_text()
            eligibility = re.sub('\n', ' ', eligibility)
            eligibility = ' '.join(eligibility.split())
            eligibilities.append(eligibility)
            
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
        df['link'] = links  
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = eligibilities
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'internationalclimateinitiative_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em internationalclimateinitiative1')

#internationalclimateinitiative1(os.getcwd())

def internationalclimateinitiative2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\internationalclimateinitiative_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.international-climate-initiative.com/en/infotheque/news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='search-results-news-list-container')
        for new in soup.find_all('li', class_='teaser'):
            link = 'https://www.international-climate-initiative.com/' + new.find('a')['href']
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('h2', itemprop = 'headline').text)
                texto = clean(''.join(page_soup.find('div', class_='news-single-item').get_text().split(titulo)))
                titulo = re.sub("#","",titulo)
                titulos.append(titulo)
                textos.append(texto)
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '2', 'internationalclimateinitiative_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em internationalclimateinitiative2')

#internationalclimateinitiative2(os.getcwd())

def internationalclimateinitiative3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.international-climate-initiative.com/en/about-iki/international-agreements', 'https://www.international-climate-initiative.com/en/about-iki/iki-funding-instrument', 'https://www.international-climate-initiative.com/en/about-iki/transparency']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\internationalclimateinitiative_03.csv'
        for link in links:
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h2').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='text').get_text())
            textos.append(texto)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['internationalclimateinitiative']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'internationalclimateinitiative_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em internationalclimateinitiative3')
        
#internationalclimateinitiative3(os.getcwd())
