# AB#40
import pandas as pd
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import requests
from urllib.request import Request, urlopen
import re
from utilidadesppf import getCodList, getInfoBase, getNewInfo, clean
from re import findall
import shutil
def rufford1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\rufford_01.csv'
        titles = [] 
        links = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        ano = datetime.today().strftime('%y')
        page_response = requests.get('https://apply.ruffordsmallgrants.org/help/criteria').content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        titulo = 'Rufford Foundation'
        titles.append(titulo)

        links.append('https://apply.ruffordsmallgrants.org/help/criteria')

        text = soup.find('div', class_= 'col-md-9').get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split()).strip()
        texts.append(text)

        text_area = soup.find('div', class_= 'row')
        top = text_area.find('h3')
        eleg_text = ''
        while('criteria' not in top.text.lower().split()):
            top = top.findNext('h3')
        while(True):
            top = top.find_next_sibling()
            if(top.name == 'h3'):
                break
            else:
                eleg_text += top.get_text()
        
        eleg_text = re.sub('\n', ' ', eleg_text)
        eleg_text = ' '.join(eleg_text.split()).strip()
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
        df['link'] = links  
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = eleg_texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = '31 de dezembro de 20' + ano
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'rufford_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em rufford1')



def rufford2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rufford_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.rufford.org/news/').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for new in soup.find_all('div', class_='news-card light'):
            link = 'https://www.rufford.org' + new.find('a')['href']
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('h1').get_text())
                texto = clean(page_soup.find('div', class_='content').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'rufford_')
            df.to_csv(path+filename, index=False)
        else:
        #    print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em rufford2')



def rufford3(path):
    try:
        titulos = []
        textos = []
        link = 'https://www.rufford.org/about/'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rufford_03.csv'
        req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').text)
        titulos.append(titulo)
        texto = clean(soup.find('div', class_='column').get_text())
        textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['rufford']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = [link]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'rufford_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em rufford3')

def rufford4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rufford_04.csv'
        titulos = []
        links = []
        hasBrazil = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_response = requests.get('https://www.rufford.org/projects/?continent=central_and_latin_america&q=&sort_by=-created').content.decode('utf-8')
        soup = BeautifulSoup(link_response, 'lxml')
        for prj in soup.find_all('article', class_='project-listing-item'):
            link = 'https://www.rufford.org' + prj.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if (new_links):
            for link in new_links:
                req = Request(link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page = urlopen(req).read()
                page_soup = BeautifulSoup(page, 'lxml')
                title = clean(page_soup.find('h2').text)
                titulos.append(title)
                text = clean(page_soup.find('div', class_='column is-8').get_text())
                if (findall(keywords, text.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
            df = pd.DataFrame()
            df['prj_titulo'] = titulos
            df['link'] = new_links
            df['prj_instituicao'] = ['Rufford'] * len(df.index)
            df['prj_valor'] = ['NA'] * len(df.index)
            df['prj_brazil'] = hasBrazil
            df['atualizacao'] = [dia] * len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'rufford_')
            df.to_csv(path + filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em rufford4')
