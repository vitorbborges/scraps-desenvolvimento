# AB#129
from utilidadesppf import getCodList, getInfoBase, getNewInfo, clean
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen
import os

def dfg1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\dfg_01.csv'
        titles = [] #
        links = [] #
        deadlines = [] 
        texts = []
        hasBrazil = [] #
        types = [] #
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime("%y"))
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        
        page_request = requests.get('https://www.dfg.de/en/research_funding/announcements_proposals/calls_for_proposals/index.html').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        
        presoup = page_soup.find_all('div', class_='pmUebersicht')
        soup2 = BeautifulSoup(str(presoup),'html.parser')
        
        for a in soup2.find_all('a', href=True):
            links.append('https://www.dfg.de/en/research_funding/announcements_proposals/calls_for_proposals/'+a['href'])
        
        
        new_links = getNewInfo(links_base, links)
        # new_links=links
        
        if(new_links):
            for i in new_links:
                page_request = requests.get(i).content.decode('utf-8')
                page_soup = BeautifulSoup(page_request, 'lxml')
                titulo = page_soup.find('span', class_="bab-breadcrumb-eintrag").get_text()
                titles.append(titulo)
                text = clean(page_soup.find('div', class_='row bab-modul-fliesstext').get_text())
                # print(text)
                texts.append(text)
                dead= page_soup.find('div', class_='row bab-modul-fliesstext').find('strong')
                if dead and len(dead.text) <= 20:
                    dead=dead.get_text()
                else:
                    dead =" "
                deadlines.append(dead)
        
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
            df['opo_texto_ele'] = texts
            df['opo_texto'] = texts
            df['opo_brazil'] = hasBrazil   
            df['opo_tipo'] = types      
            df['opo_deadline'] = deadlines   
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'dfg_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em dfg1')


#dfg1(os.getcwd())

def dfg2(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+ '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/dfg_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        req = Request('https://www.dfg.de/en/service/press/news/', headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(req).read()
        soup = BeautifulSoup(page_request, 'lxml')
        soup = soup.find('div', class_='col-cs-122 col-md-9')
        soup = BeautifulSoup(str(soup.find_all('div',class_='text')), 'lxml')



        for new in soup.find_all('a', class_ = 'link-intern'):
            link = new['href']
            link = link[2:]
            #print("https://www.dfg.de/en/service/press" + link)


            links.append("https://www.dfg.de/en/service/press" + link)

            

        new_links = getNewInfo(links_base, links)
        new_links= links

        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('h1').find_next('h1').get_text())
                #print(titulo)
                texto = clean(page_soup.find('main').get_text())
                #print(texto)
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'dfg_')
            df.to_csv(path+filename, index=False) #primeira coluna: índice
        else:
            #print('Não há alteração em novas noticias')
            shutil.copy(pathbase+filename, '.\\'+dia)

    except Exception as e:
        print(e)
        print('Erro em dfg2')

#dfg2(os.getcwd())

def dfg3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '/dfg_03.csv'
        titulos = []
        textos = []
        links = ['https://www.dfg.de/en/research_funding/individual_grants_programmes/individual_funding/index.html']

        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1').find_next('h1').get_text())
            titulos.append(titulo)
            texto = clean(soup.find('main').get_text())
            textos.append(texto)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['dfg']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'dfg_')
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em dfg3')

#dfg3(os.getcwd())
