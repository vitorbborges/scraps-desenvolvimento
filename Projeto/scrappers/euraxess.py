# AB#142
from utilidadesppf import getNewInfo, getInfoBase, getCodList
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen
from itertools import compress


def euraxess1(path, keywords='(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        filename = '\\euraxess_01.csv'
        titles = []
        links = []
        texts = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link = 'https://euraxess.ec.europa.eu/funding/search/'
        deadlines = []
        hasBrazil = []
        types = []
        dia = datetime.today().strftime("%y%m%d")
        while True:
            req = Request(link, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            request = urlopen(req).read()
            soup = BeautifulSoup(request, 'lxml')
            opo_area = soup.find('div', class_='view-content')
            for opo in opo_area.find_all('div', recursive=False):
                rabo = opo.find_all('a')[-1]['href']
                link = 'https://euraxess.ec.europa.eu/' + rabo
                links.append(link)
            if soup.find('li', class_='pager-next'):
                next = ''
                next = soup.find('li', class_='pager-next').find('a')
                if next is None:
                    break
                else:
                    next = next['href']
                    link = 'https://euraxess.ec.europa.eu/' + next
            else:
                break
        new_links = getNewInfo(links_base, links)
        if new_links:
            for link in new_links:
                req = Request(link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                request = urlopen(req).read()
                page_soup = BeautifulSoup(request, 'lxml')

                titulo = page_soup.find('h1', class_='head-title').text
                titles.append(titulo)
                if page_soup.find('div', class_='col-xs-12 col-sm-7 value field-deadline-date inline') is not None:
                    deadline = page_soup.find('div',
                                              class_='col-xs-12 col-sm-7 value field-deadline-date inline').get_text()
                else:
                    deadline = page_soup.find('div',
                                              class_='col-xs-12 col-sm-7 value field-deadline-text inline').get_text()
                deadline = re.sub('\n', '', deadline).strip()
                deadlines.append(deadline)

                text = page_soup.find('div', class_='longtext field-body').get_text()
                text = re.sub('\n', ' ', text)
                text = ' '.join(text.split())
                texts.append(text)

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
                    
            df = pd.DataFrame()
            df['opo_titulo'] = titles
            df['link'] = new_links
            df['opo_texto'] = texts
            df['opo_texto_ele'] = texts
            df['opo_brazil'] = hasBrazil
            df['opo_tipo'] = types
            df['opo_deadline'] = deadlines
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'euraxess_')
            df['atualizacao'] = [dia] * len(df.index)
            df.to_csv(path + filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase + filename, '.\\' + dia)
    except Exception as e:
        print(e)
        print('Erro em euraxess1')

#euraxess1('.')
