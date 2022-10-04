# AB#104
from utilidadesppf import getInfoBase, getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
from urllib.request import Request, urlopen
import re



def gfdrr2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\gfdrr_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.gfdrr.org/en/news').text
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='view-content')
        for new in soup.find_all('div', class_='views-row'):
            link = new.find('a')['href']
            links.append(link)
            titulo = clean(new.find('div',class_= 'views-field-title').get_text())
            texto = clean(new.find('div', class_= 'views-field views-field-nothing-1 views-field-summary').get_text())
            titulos.append(titulo)
            textos.append(texto)
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'gfdrr_')
        df['atualizacao'] = [dia]*len(df.index)
        
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em gfdrr2')


def gfdrr3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.gfdrr.org/en/gfdrr-labs', 'https://www.gfdrr.org/en/resilient-infrastructure', 'https://www.gfdrr.org/en/resilient-cities', 'https://www.gfdrr.org/en/hydromet-services-and-early-warning-systems', 'https://www.gfdrr.org/en/financial-protection', 'https://www.gfdrr.org/en/social-resilience', 'https://www.gfdrr.org/en/resilience-climate-change', 'https://www.gfdrr.org/en/global-facility-disaster-reduction-and-recovery']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\gfdrr_03.csv'
        for link in links:
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('div', class_='col-xs-12').find('h1').text)
            titulos.append(titulo)
            texto = clean(soup.find_all('div', class_='container')[4].get_text())
            texto = re.sub('(Read More|View All Grants)', '', texto)
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['gfdrr']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'gfdrr_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em gfdrr3')


def gfdrr4(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\gfdrr_04.csv'
        titles = [] 
        links = []
        instituicoes = []
        hasBrazil = []# 
        values = []
        dia = datetime.today().strftime("%y%m%d")
        request = requests.get('https://www.gfdrr.org/en/region/brazil').content.decode('utf-8')
        soup = BeautifulSoup(request, 'lxml')
        for opo in soup.find('table', class_='table table-hover table-striped').find('tbody').find_all('tr'):

            link ='https://www.gfdrr.org/' + str(opo.find('a')['href'])
            links.append(link)

            titulo = opo.find('a').text
            titles.append(titulo)

            inst = opo.find('td', class_='views-field views-field-field-funding-source').text
            instituicoes.append(inst)

            if(findall(keywords, opo.find('td', class_='views-field views-field-field-country').text.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            
            valor = opo.find('td', class_='views-field views-field-field-amount').text
            values.append(valor)

            df = pd.DataFrame()       
            df['prj_titulo'] = titles  #
            df['link'] = links#
            df['prj_instituicao'] = instituicoes
            df['prj_valor'] = values 
            df['prj_brazil'] = hasBrazil   
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'gfdrr_')
            
            df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em gfdrr4')




