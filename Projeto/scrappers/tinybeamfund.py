# AB#136
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from itertools import compress
from urllib.request import Request, urlopen


def tinybeamfund1(path, keywords='(brazil|latin america region)'):
    try:
        filename = '\\tinybeamfund_01.csv'
        titulos = []
        textos = []
        links = ['https://tinybeamfund.org/Research-Planning-Grants-Program',
                 'https://tinybeamfund.org/Fellowship-Awards']  #

        hasBrazil = []
        types = []
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime("%y"))
        for link in links:
            page = requests.get(link, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = clean(soup.find('h1', class_='pageBannerTitle').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='blockContents').get_text())
            textos.append(texto)

            if findall(keywords, texto.lower()):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            if len(findall('grant', texto.lower())):
                types.append('grant')
            elif len(findall('fellowship', texto.lower())):
                types.append('fellowship')
            elif len(findall('scholarship', texto.lower())):
                types.append('scholarship')
            else:
                types.append('other')

        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_texto'] = textos
        df['opo_texto_ele'] = textos
        df['opo_brazil'] = hasBrazil
        df['opo_tipo'] = types
        df['opo_deadline'] = ['31 de dezembro de ' + ano] * len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'tinybeamfund_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em tinybeamfund1')


def tinybeamfund3(path):
    try:
        instituicoes = []
        titulos = []
        textos = []
        links = ['https://tinybeamfund.org/About-Us',
                 'https://tinybeamfund.org/Research-Planning-Grants-Program',
                 'https://tinybeamfund.org/Our-Approach',
                 'https://tinybeamfund.org/Fellowship-Awards']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\tinybeamfund_03.csv'
        for link in links:
            page = requests.get(link, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = clean(soup.find('h1', class_='pageBannerTitle').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='blockContents').get_text())
            textos.append(texto)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['tinybeamfund'] * len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'tinybeamfund_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em tinybeamfund3')
