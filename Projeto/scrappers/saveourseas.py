# AB#119
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo


# LIST
# opo_titulo --
# link --
# opo_deadline --
# opo_texto --
# opo_tipo --
# opo_brazil
# codigo --
# atualizacao --

# retorna os links obtidos na base principal
def getLinksBase(path, filename):
    links_base = []
    path = path + filename
    try:
        dfbase = pd.read_csv(path)
        links_base = (dfbase['link'].tolist())
    except:
        pass
    return links_base


# retorna os links que ainda nao foram lidos
def getNewLinks(links_base, links):
    track = [i in links_base for i in links]
    new_links_bool = [not bool for bool in track]
    new_links = (list(compress(links, new_links_bool)))
    return new_links


def saveourseas1(path, keywords='(latin american region|brazil)'):
    try:
        # -------------------------------------------------
        titles = []
        deadlines = []
        texts = []
        eleg_texts = []
        types = []
        hasBrazil = []
        status = []
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().strftime('%y')

        links = ['https://saveourseas.com/grants/funding-applications/keystone-grants/',
                 'https://saveourseas.com/grants/funding-applications/small-grants/']
        for i in links:
            req = Request(i, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            # ------------------TITULO---------------
            title = soup.find('h1').get_text()
            titles.append(title)
            # ----------------------TEXTO---------------
            texto = soup.find('div', class_="the-content").get_text()
            eleg_texts.append(texto)
            texts.append(texto)
            # -------------- DEADLINE ------------
            tag_close_date = soup.find('div', class_="the-content").find('p').find_next('p').get_text()
            deadlines.append(tag_close_date)
            # ---------------TIPO-----------------------
            if len(findall('grant', texto.lower())):
                types.append('grant')
            elif len(findall('fellowship', texto.lower())):
                types.append('fellowship')
            elif len(findall('scholarship', texto.lower())):
                types.append('scholarship')
            else:
                types.append('other')
            # ---------------------LINKS-------------------
            if findall(keywords, texto):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')

        df = pd.DataFrame()
        df['opo_titulo'] = titles
        df['opo_texto'] = texts
        df['opo_texto_ele'] = eleg_texts
        df['link'] = links
        df['opo_tipo'] = types
        df['opo_brazil'] = hasBrazil
        df['opo_deadline'] = deadlines
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'saveourseas_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + '\\saveourseas_01.csv', index=False)

    except Exception as e:
        print(e)
        print('Erro em saveourseas1')


def saveourseas2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/saveourseas_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://saveourseas.com/news/ocean-news/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sites = soup.find_all('div', class_="col-md-12 col-md-offset-0 col-lg-10 col-lg-offset-1")
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for link in soup2.find_all('a'):
            info = (link['href'])
            links.append(info)

        new_links = getNewInfo(links_base, links)

        if new_links:
            for link in links:
                page = Request(link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_request = urlopen(page).read()
                soup = BeautifulSoup(page_request, 'lxml')
                titulo = soup.find('h1').get_text()
                texto = soup.find('div', class_="the-content").get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['atualizacao'] = [dia] * len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'saveourseas_')
            df.to_csv(path + filename, index=False)
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase + filename, '.\\' + dia)



    except Exception as e:
        print(e)
        print('Erro em saveourseas2')


def saveourseas3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\saveourseas_03.csv'
        titulos = []
        textos = []
        links = ['https://saveourseas.com/foundation/philosophy/']
        page = Request('https://saveourseas.com/foundation/philosophy/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1').get_text()
        texto = soup.find('div', class_="the-content").get_text()
        titulos.append(titulo)
        textos.append(clean(texto))

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['saveourseas'] * len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'saveourseas_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em saveourseas3')
