# AB#22
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from utilidadesppf import getCodList, getNewInfo, getInfoBase, clean
from urllib.request import Request, urlopen
import shutil
from re import findall
import requests

def greenclimate2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\greenclimate_02.csv'
        titulos = []
        textos = []
        links = []
        errorlinks = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.greenclimate.fund/news').text
        soup = BeautifulSoup(page, 'lxml')
        for card in soup.find_all('div', class_= 'col-auto col-card mb-4'):
            link = card.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).text
                soup = BeautifulSoup(page, 'lxml')
                if(soup.find('div', class_='col-lg-9 pl-0 lax') is not None):
                    titulo = clean(soup.find('div', class_='col-lg-9 pl-0 lax').find('h1').text)
                else:
                    errorlinks.append(link)
                    continue
                titulos.append(titulo)
                texto = clean(soup.find('div', class_='content-container').get_text())
                textos.append(texto)
            for badlink in errorlinks:
                new_links.remove(badlink)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'greenclimate_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em greenclimate2')     

def greenclimate3(path):
    try:
        instituicoes = []
        titulos = []
        textos = []
        links = ['https://www.greenclimate.fund/about/secretariat', 'https://www.greenclimate.fund/about/secretariat#structure', 'https://www.greenclimate.fund/about/secretariat/management', 'https://www.greenclimate.fund/about/secretariat/headquarters', 'https://www.greenclimate.fund/about#overview']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\greenclimate_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            soup = soup.find('div', class_='content-container')
            titulo = clean(soup.find('h2', class_='h5 mb-4 title-line title-line--small text-sansserif font-weight-bold text-primary pull-out-left').text)
            titulos.append(titulo)
            texto = clean(soup.get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['GreenClimate']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'greenclimate_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em greenclimate3')




def greenclimate4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\greenclimate_04.csv'
        titulos = []
        links = []
        values = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')
        req = Request('https://www.greenclimate.fund/projects', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        for prj in soup.find_all('div', class_='col-auto col-card'):
            link = prj.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page = urlopen(req).read()
                page_soup = BeautifulSoup(page, 'lxml')
                title = clean(page_soup.find('h1', class_='display-4').text)
                titulos.append(title)
                valor = clean('USD' + str(page_soup.find("h3", {"class":"mb-0 pt-5 display-3 font-weight-light text-primary tabular-nums scrollmagic-animated"})['data-chart-dataset']))
                values.append(valor)   
                location = clean(page_soup.find('ul', class_='list-unstyled h6 line-height-loose d-lg-flex flex-wrap').text)
                if(findall(keywords, location.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')

                instituicao = clean(page_soup.find('h5', class_='mt-1 mb-3').text)
                prj_inst.append(instituicao)
            df = pd.DataFrame()
            df['prj_titulo'] = titulos 
            df['link'] = new_links 
            df['prj_instituicao'] = prj_inst
            df['prj_valor'] = values
            df['prj_brazil'] = hasBrazil
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'greenclimate_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em greenclimate4')
