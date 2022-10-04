# AB#102
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen


def packard3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.packard.org/about-the-foundation/our-investments/', 'https://www.packard.org/grants-and-investments/mission-investing/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\packard_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h2', class_='super-title').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='wpb_wrapper').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['packard']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'packard_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em packard3')

def packard4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\packard_04.csv'
        titulos = []
        links = []
        values = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_response = requests.get('https://www.packard.org/grants-and-investments/grants-database/?grant_keyword&program_area&award_amount&award_year=2021#038;program_area=&award_amount=&award_year=2021').content.decode('utf-8')
        soup = BeautifulSoup(link_response, 'lxml')
        soup = soup.find('table')
        for prj in soup.find_all('tr'):
            if(prj.find('a') is not None):
                link = prj.find('a')['href']
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                page_soup = page_soup.find('div', class_='wpb_wrapper')
                title = clean(page_soup.find('h2').text)
                titulos.append(title)
                valor = clean(page_soup.find_all('p')[2].text.split(':')[1])
                values.append(valor)   
                location = clean(page_soup.find_all('p')[5].text)
                if(findall(keywords, location.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')

                instituicao = clean(page_soup.find_all('p')[6].text)
                if(findall('www', instituicao)):
                    instituicao = instituicao.split('.')[1].split('.')[0]
                else:
                    instituicao = 'Packard'
                prj_inst.append(instituicao)
            df = pd.DataFrame()
            df['prj_titulo'] = titulos 
            df['link'] = new_links 
            df['prj_instituicao'] = prj_inst
            df['prj_valor'] = values
            df['prj_brazil'] = hasBrazil
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'packard_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em packard4')