# AB#27
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
import requests
import shutil
from itertools import compress
from currency_converter import CurrencyConverter
from utilidadesppf import clean, getCodList
from utilidadesppf import getInfoBase, getNewInfo,  truncate


# def fundoamazonia2(path):
#     try:
#         pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
#         dia = datetime.today().strftime('%y%m%d')
#         filename = '\\fundoamazonia_02.csv'
#         titulos = []
#         textos = []
#         links = []
#         links_base = getInfoBase(pathbase, filename, 'link')
#         link_page = 'http://www.fundoamazonia.gov.br/en/news/'

#         pageresposta = requests.get(link_page).content.decode('utf-8')
#         soup = BeautifulSoup(pageresposta, 'lxml')

#         for paginas in soup.find('div', class_="pagination"):
#             paginas.append(soup.find('a', class_="pagination-next")['href'])
#             print(paginas)
#             link_page = 'http://www.fundoamazonia.gov.br' + soup.find('a', class_= 'pagination-next').find('href')
#             print(paginas)
#             print(link_page)


#             links = requests.get(link_page).content.decode('utf-8')
#             page_soup = BeautifulSoup(links, 'lxml')
#             titulo = page_soup.find('h2').text
#             titulos.append(titulo)
#             texto = ''
#             text_area = page_soup.find('div', class_='row')
#             for p in text_area.find_all('p'):
#                 texto+=p.text
#             textos.append(texto)
#         df = pd.DataFrame()
#         df['not_titulo'] = titulos
#         df['link'] = pd.Series(links)
#         df['not_texto'] = textos
#         df['atualizacao'] = [dia]*len(df.index)
#         df['codigo'] = getCodList(dia, len(df.index), '_2_', 'fundoamazonia_')
#         df.to_csv(path+filename, index=False)


#     except Exception as e:
#         print(e)
#         print('Erro em fundoamazonia2')






def fundoamazonia3(path):
    try:
        instituicoes = []
        titulos = []
        textos = []
        links = ['http://www.fundoamazonia.gov.br/pt/comunicacao/obrigacoes-contratuais/', 'http://www.fundoamazonia.gov.br/pt/fundo-amazonia/governanca/', 'http://www.fundoamazonia.gov.br/pt/como-apresentar-projetos/focos-de-apoio/', 'http://www.fundoamazonia.gov.br/pt/fundo-amazonia/politicas-publicas-orientadoras/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fundoamazonia_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h2').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', id = 'conteudo').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['fundoamazonia']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'fundoamazonia_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em fundoamazonia3')


def fundoamazonia4(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fundoamazonia_04.csv'
        titulos = []
        converter = CurrencyConverter()
        links = []
        values = []
        instituicoes = []
        links_base = getInfoBase(path, filename, 'link')
        instituicoes_base = getInfoBase(path, filename, 'prj_instituicao')
        page = requests.get('http://www.fundoamazonia.gov.br/en/library/projects/').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for card in soup.find_all('td', style = 'width: 327px;'):
            if(card.find('a') is not None):
                link = card.find('a')['href']
                if(link[:4] != 'http'):
                    link = 'http://www.fundoamazonia.gov.br/' + link
                links.append(link)
        for inst in soup.find_all('td', style = 'width: 313px;'):
            if(inst.find('p') is not None):
                instituicao = inst.find('p').text
                instituicoes.append(instituicao)
        new_links = getNewInfo(links_base, links)
        new_inst = getNewInfo(instituicoes_base, instituicoes)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = page_soup.find('h2').text
                titulos.append(titulo.strip())
                valor = page_soup.find_all('ul', class_='filtro')[5].text
                valor = re.sub('(R\$|\\n|\\t)', '', valor)
                valor_dol = ''
                for i in range(len(valor)):
                    if valor[i] == ',':
                        valor_dol +=''
                    else:
                        valor_dol+= valor[i]
                valor = float(valor_dol)
                valor = converter.convert(valor, 'BRL', 'USD')
                valor = truncate(valor, 2)
                values.append(valor)
            df = pd.DataFrame()
            df['prj_titulo'] = titulos 
            df['link'] = new_links 
            df['prj_instituicao'] = new_inst 
            df['prj_valor'] = values
            df['prj_brazil'] = ['Y']*len(df.index)
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'fundoamazonia_')
            df.to_csv(path+filename, index=False)

    except Exception as e:
        print(e)
        print('Erro em fundoamazonia4')


def fundoamazonia2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fundoamazonia_02.csv'
        titulos = []
        links = []
        textos = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_page = 'http://www.fundoamazonia.gov.br/en/news/'
        for i in range(3):
            page = requests.get(link_page).content.decode('utf-8')
            page_soup = BeautifulSoup(page, 'lxml')
            for proj in page_soup.find('div', class_='news-search').find_all('div', class_='news-search-item block-link'):
                link = proj.find('a')['href']
                links.append('http://www.fundoamazonia.gov.br' + link)
                linkpagenew = page_soup.find('div', class_= 'news-search').find('div', class_="pagination").find('a', class_="pagination-next")['href']
                link_page = 'http://www.fundoamazonia.gov.br' + linkpagenew
                
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                title = page_soup.find('div', class_ = 'wrapper clearfix').find('h2').text
                titulos.append(title)
                texto = page_soup.find('div', class_='row').get_text()
                textos.append(clean(texto))
                #print(textos)

                #valor = page_soup.find('div', class_= 'project-information project-section').find('span', class_ = 'project-field-data').text
                #valor = re.sub(' ', '', valor)
                #values.append(valor)                
            df = pd.DataFrame()

            df['not_titulo'] = pd.Series(titulos)
            df['link'] = pd.Series(new_links)
            df['not_texto'] = pd.Series(textos)
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'fundoamazonia_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)

    except Exception as e:
        print(e)
        print('Erro em fundoamazonia2')
