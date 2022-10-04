# AB#59
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import os
from urllib.request import Request, urlopen
from itertools import compress
import shutil
from utilidadesppf import clean, getCodList, getNewInfo, getInfoBase


# TODO LIST
# opo_titulo --
# link --
# opo_deadline --
# opo_texto --
# opo_tipo --
# opo_brazil --
# codigo
# atualizacao
# retorna uma lista pra preenchimento da coluna de códigos


def foundationfar1(path, keywords='(brazil|latin america region)'):
    try:
        # ----------------------LISTAS------------------------
        filename = '\\foundationfar_01.csv'
        titles = []
        links = []
        deadlines = []
        texts = []
        hasBrazil = []
        types = []
        eleg_texts = []
        dia = datetime.today().strftime("%y%m%d")
        ano = datetime.today().strftime('%y')
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        # ----------------------------------------------------
        page = requests.get('https://foundationfar.org/grants-funding/open-opportunities/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        main_soup = BeautifulSoup(page.text, 'lxml')
        
        a = main_soup.find_all('a', class_='card1-wrap box1 -a4 -i1h -mh1')
        for card in a:
            links.append(card['href'])
        
        new_links = getNewInfo(links_base, links)
        if (new_links):
            for link in new_links:
                page = requests.get(link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                link_soup = BeautifulSoup(page.text, 'lxml')
                title = clean(link_soup.find('title').text)
                titles.append(title)
                
                for i in a:
                    if link in str(i):
                        deadline = i.find('time')
                        if deadline:
                            deadline = deadline.text
                        else:
                            deadline = 'December 31, 20' + ano
                        deadlines.append(deadline)
                
                text_soup = link_soup.find('div', class_='-xw:3')
                text = ''
                # -----------------TEXT---------------------
                for result in text_soup.find_all('p'):
                    text_part = result.text
                    text += text_part
                texts.append(text)
                # --------------ELEGTEXTS---------------
                dt = link_soup.find('dt', class_='accordion1-title')
                if dt:
                    span = dt.find('span').text
                    if 'eligible' in span.split(" ") or span == 'Who can apply?':
                        eleg_text = dt.find_next_sibling().text
                        eleg_texts.append(eleg_text)
                    else:
                        eleg_texts.append(text)
                else:
                    eleg_texts.append(text)
                        
                # ----------------BRAZIL---------------
                if findall(keywords, text):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
                # ---------------TIPO------------------
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
            df['opo_texto'] = texts
            df['opo_texto_ele'] = texts
            df['opo_brazil'] = hasBrazil
            df['opo_tipo'] = types
            df['opo_deadline'] = deadlines
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'foundationfar_')
            df['atualizacao'] = [dia] * len(df.index)
            df.to_csv(path + filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase + filename, '.\\' + dia)
    except Exception as e:
        print(e)


def foundationfar2(path):
    try:
        dia = datetime.today().strftime("%y%m%d")
        titulos = []  # done
        links = []  # done
        textos = []
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        filename = '\\foundationfar_02.csv'
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://foundationfar.org/news/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_soup = BeautifulSoup(page.text, 'lxml')
        for article in page_soup.find_all('article', class_='teaser1'):
            link = article.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if new_links:
            for link in new_links:
                page = requests.get(link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_soup = BeautifulSoup(page.text, 'lxml')
                titulo = page_soup.find('h1').text
                titulos.append(titulo)
                text_area = page_soup.find('div', class_='-xw:3')
                texto = ''
                for p in text_area.find_all('p'):
                    texto += p.text
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia] * len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'foundationfar_')
            df.to_csv(path + filename, index=False)
        else:
            #print('Não há alteração em novas noticias')
            shutil.copy(pathbase + filename, '.\\' + dia)

    except Exception as e:
        print(e)
        print('Erro em foundationfar2')


def foundationfar3(path):
    try:
        titulos = []
        textos = []
        links = ['https://foundationfar.org/what-we-do/',
                 'https://foundationfar.org/grants-funding/funding-approval-process/#how-we-develop-research-programs',
                 'https://foundationfar.org/grants-funding/funding-approval-process/#how-we-fund-research']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\foundationfar_03.csv'
        page = requests.get('https://foundationfar.org/what-we-do/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('h1', class_='-mb:m5').text)
        titulos.append(titulo)
        texto = ''
        for p in soup.find_all('p'):
            texto += p.text
        texto = clean(texto)
        textos.append(texto)

        page = requests.get(
            'https://foundationfar.org/grants-funding/funding-approval-process/#how-we-develop-research-programs',
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('ul', class_='tabs2-main').find('li').text)
        titulos.append(titulo)
        texto = clean(soup.find_all('div', class_='steps1')[0].get_text())
        textos.append(texto)

        page = requests.get('https://foundationfar.org/grants-funding/funding-approval-process/#how-we-fund-research',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        titulo = clean(soup.find('ul', class_='tabs2-main').find('li').findNextSibling().text)
        titulos.append(titulo)
        texto = clean(soup.find_all('div', class_='steps1')[1].get_text())
        textos.append(texto)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['foundationfar'] * len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'foundationfar_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em foundationfar3')


def foundationfar4(path, keywords='(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\foundationfar_04.csv'
        titulos = []
        links = []
        values = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://foundationfar.org/grants-funding/grants/', headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        
        for prj in soup.find_all('div', class_='card1 -mb:m3'):
            link = prj.find('a')['href']
            links.append(link)
            title = clean(prj.find('h3').get_text())
            titulos.append(title)
            info_area = prj.find('div', class_='grid-entries -gg:4 card-grant-g2')
            valor = clean(info_area.find_all('p')[2].text)
            valor = '$' + valor.split('$')[1]
            values.append(valor)
            location = clean(info_area.find_all('p')[3].text)
            if findall(keywords, location.lower()):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            if findall('matching', info_area.find_all('p')[-1].text.lower()):
                instituicao = clean(info_area.find_all('p')[-1].text)
                instituicao = instituicao.split('Funders ')[1]
            else:
                instituicao = 'FoundationFar'
            prj_inst.append(instituicao)
        df = pd.DataFrame()
        df['prj_titulo'] = titulos
        df['link'] = links
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = values
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia] * len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'foundationfar_')
        df.to_csv(path + filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em foundationfar4')
