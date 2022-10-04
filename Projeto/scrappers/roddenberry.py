# AB#61
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList
import requests


#LIST
#opo_titulo --
#link -- 
#opo_deadline --
#opo_texto -- 
#opo_tipo --
#opo_brazil 
#codigo --
#atualizacao --

#retorna os links obtidos na base principal
def getLinksBase(path, filename):
    links_base = []
    path = path + filename
    try:
        dfbase = pd.read_csv(path)
        links_base=(dfbase['link'].tolist())
    except:
        pass
    return links_base
#retorna os links que ainda nao foram lidos
def getNewLinks(links_base, links):
    track =[i in links_base for i in links] 
    new_links_bool = [not bool for bool in track] 
    new_links=(list(compress(links,new_links_bool)))
    return new_links
def roddenberry1(path, keywords = '(latin american region|brazil)'):
    try:
#-------------------------------------------------
        titles = []
        links = []
        deadlines = []
        texts = []
        eleg_texts = []
        types = []
        hasBrazil = []
        status =[]
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().strftime('%y')
        page = requests.get('https://roddenberryfoundation.org/our-work/catalyst-fund/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        #------------------TITULO---------------
        title = soup.find('h1').text
        titles.append(title)
        #----------------------TEXTO---------------
        text = ''
        for box in soup.find_all('div', class_= 'article__content'):
            text+=box.get_text()
        eleg_text = soup.find_all('div', class_ = 'article__content')[7].text
        eleg_text = re.sub('\n', ' ', eleg_text)
        eleg_texts.append(eleg_text)
        text = re.sub('\n', ' ', text).strip()
        texts.append(text)
        #---------------TIPO-----------------------
        if len(findall('grant', text.lower())):         
                types.append('grant')                
        elif len(findall('fellowship', text.lower())):  
            types.append('fellowship')          
        elif len(findall('scholarship', text.lower())): 
            types.append('scholarship')                   
        else:
            types.append('other')
        #---------------------LINKS-------------------
        link = soup.find('div', class_ = 'intro__aside').find('a')
        links.append(link['href'])
        dead = soup.find('div', class_ = 'article__content').text
        if (findall(keywords, dead)):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
        df = pd.DataFrame() 
        df['opo_titulo'] = titles
        df['link'] = links
        df['opo_texto'] = texts
        df['opo_texto_ele'] = eleg_texts
        df['opo_brazil'] = hasBrazil
        df['opo_tipo'] = types
        df['opo_deadline'] = ['December 31, 20' + ano]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'roddenberry_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + '\\roddenberry_01.csv', index=False)   

    except Exception as e:
        print(e)
        print('Erro em roddenberry1')


def roddenberry2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\roddenberry_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getLinksBase(pathbase, filename)
        page = requests.get('https://roddenberryfoundation.org/blog/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_soup = BeautifulSoup(page.text, 'lxml')
        for news in page_soup.find_all('div', class_= 'post-info'):
            link = news.find('h2').find('a')['href']
            links.append(link)
        new_links = getNewLinks(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_soup = BeautifulSoup(page.text, 'lxml')
                titulo = page_soup.find('h1').text
                titulos.append(titulo)
                text_area = page_soup.find('div', class_='content')
                texto = ''
                for p in text_area.find_all('p'):
                    texto+=p.text
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'roddenberry_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas noticias')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em roddenberry2')



def roddenberry3(path):
    try:
        titulos = []
        textos = []
        links = ['https://roddenberryfoundation.org/', 'https://roddenberryfoundation.org/our-work/roddenberry-prize/', 'https://roddenberryfoundation.org/our-work/catalyst-fund/', 'https://roddenberryfoundation.org/our-work/roddenberry-fellowship/', 'https://roddenberryfoundation.org/our-work/plus-one-global-fund/', 'https://roddenberryfoundation.org/approach/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\roddenberry_03.csv'
        page = requests.get(links[0], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('h2').text)
        titulos.append(titulo)
        texto = clean(soup.get_text())
        textos.append(texto)

        page = requests.get(links[1], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('h3', class_='title').text)
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto += p.text
        texto = clean(texto)
        textos.append(texto)

        page = requests.get(links[2], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('h2', class_='title').text)
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto += p.text
        texto = clean(texto)
        textos.append(texto)

        page = requests.get(links[3], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('div', class_='intro__content').find('h1').text)
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto += p.text
        texto = clean(texto)
        textos.append(texto)


        page = requests.get(links[4], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('div', class_='intro__content').find('h1').get_text())
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto += p.text
        texto = clean(texto)
        textos.append(texto)

        page = requests.get(links[5], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('h1').text)
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto += p.text
        texto = clean(texto)
        textos.append(texto)



            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['roddenberry']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'roddenberry_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em roddenberry3')
