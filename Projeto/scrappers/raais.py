import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import shutil
from re import findall

def raais1(path, keywords='(brazil|latin america region)'):
    try:

        dia = datetime.today().strftime('%y%m%d')
        filename = '\\raais_01.csv'
        url = ['https://www.raais.org/grants']
        page = requests.get(url[0]).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h1',style="white-space:pre-wrap;").text
        
        
        txt =''
        for i in soup.find('h1',style="white-space:pre-wrap;").next_siblings:
            
            if str(i)[:2] == '<p':
                txt += i.text
            else:
                break
        texto = txt
        
        hasBrazil = []    
        if(findall(keywords, texto.lower())):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
            
        tipos=[]    
        if(findall('grant', texto.lower())):         
            tipos.append('grant')                
        elif(findall('fellowship', texto.lower())):  
            tipos.append('fellowship')          
        elif(findall('scholarship', texto.lower())): 
            tipos.append('scholarship')                   
        else:
            tipos.append('other')
        
        deadlines = ['Não Econtrado.']
        
        df = pd.DataFrame()
        df['opo_titulo'] = [titulo]
        df['link'] = url
        df['opo_deadline'] = deadlines
        df['opo_texto'] = [texto]
        df['opo_texto_ele'] = [texto]
        df['opo_tipo'] = tipos
        df['opo_brazil'] = hasBrazil
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'raais_')
        df['atualizacao'] = [dia]*len(url)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em raais1')
        


def raais2(path):
    try:

        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\raais_02.csv'
        url = 'https://www.raais.org/news'
        page_response = requests.get(url).content.decode('UTF-8')
        soup = BeautifulSoup(page_response, 'lxml')
        links = [url + l['href'][5:] for l in soup.find_all('a', class_='u-url')]
        links_base = getInfoBase(pathbase, filename, 'link')
        titulos = [t.text for t in soup.find_all('a', class_='u-url')]
        textos = []
        
        new_links = getNewInfo(links_base, links)
        
        if(new_links):
            for i in new_links:
                page = requests.get(i).content.decode('UTF-8')
                soup = BeautifulSoup(page, 'lxml')
                
                txt = ''
                for j in soup.find_all('p', style='white-space:pre-wrap;'):
                    txt += j.text
                
                textos.append(clean(txt))
                
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'raais_')
            df.to_csv(path + filename, index = False)

        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
            
    except Exception as e:
        print(e)
        print('Erro em raais2')
        
def raais3(path):
    try:

        dia = datetime.today().strftime('%y%m%d')
        filename = '\\raais_03.csv'
        titulos = []
        textos = []
        url = ['https://www.raais.org/mission']
        page = requests.get(url[0]).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        
        txt = ''
        for i in soup.find_all('p', style='white-space:pre-wrap;'):
            txt += i.text
            
        textos.append(clean(txt))
        titulos.append(soup.find('h1', style="white-space:pre-wrap;").text)
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['raais']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = url
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'raais_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em raais3')


def raais4(path, keywords = '(brazil|latin america region)'):
    try:
      
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\raais_04.csv'
        url = ['https://www.raais.org/grants']
        instituicao = 'raais'
        page = requests.get(url[0]).content.decode('UTF-8')
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h2',style="white-space:pre-wrap;").text
        txt =''
        for i in soup.find('h2',style="white-space:pre-wrap;").next_siblings:
            
            if str(i)[:2] == '<p':
                txt += i.text
            else:
                break
        
        
        hasBrazil = []    
        if(findall(keywords, txt.lower())):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
            
        value = 'Não Econstrado.'
        
        df = pd.DataFrame()
        df['prj_titulo'] = [titulo]
        df['link'] = url
        df['prj_instituicao'] = [instituicao]*len(df.index)
        df['prj_valor'] = [value]*len(df.index)
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'raais_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em raais4')




        
        