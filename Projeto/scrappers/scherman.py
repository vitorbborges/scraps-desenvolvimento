# AB#96
from utilidadesppf import getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
from urllib.request import Request, urlopen


def scherman1(path, keywords='(brazil|latin america region)'):
    try:
        filename = '\\scherman_01.csv'
        titles = []  #
        deadlines = []  #
        texts = []  #
        hasBrazil = []  #
        types = []  #
        lista = []
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime('%y'))
        page_request = requests.get('https://www.scherman.org/how-to-apply#anchor%201').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        lista = page_soup.find_all('h2', style='white-space:pre-wrap;')[-2:]
        for titulo in lista:
            titulo = clean(titulo.get_text())
            titles.append(titulo)

        text1 = clean(page_soup.find_all('div', class_='sqs-block html-block sqs-block-html')[3].get_text())
        text2 = clean(page_soup.find_all('div', class_='sqs-block html-block sqs-block-html')[-1].get_text())
        text = text1 + text2
        texts.append(clean(page_soup.find_all('div', class_='sqs-block html-block sqs-block-html')[3].get_text()))
        texts.append(clean(page_soup.find_all('div', class_='sqs-block html-block sqs-block-html')[-2].get_text()))

        if findall(keywords, text.lower()):
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

        deadline = '31 de dezembro de ' + ano
        deadlines.append(deadline)
        df = pd.DataFrame()
        df['opo_titulo'] = titles
        df['link'] = ['https://www.scherman.org/how-to-apply#anchor%201'] * len(df.index)
        df['opo_texto'] = texts
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil * len(df.index)
        df['opo_tipo'] = types * len(df.index)
        df['opo_deadline'] = deadlines * len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'scherman_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em scherman1')


def scherman3(path):
    try:
        titulos = []
        textos = []
        link = 'https://www.scherman.org/mission-and-history'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\scherman_03.csv'
        page = requests.get(link, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        soup = soup.find('div', class_='row sqs-row')
        titulo = clean(soup.find('h2').text)
        titulos.append(titulo)
        texto = clean(soup.get_text())
        textos.append(texto)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['scherman'] * len(df.index)
        df['pol_texto'] = textos
        df['link'] = [link] * len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'scherman_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em scherman3')
