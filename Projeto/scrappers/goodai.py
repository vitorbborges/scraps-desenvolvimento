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
import requests
#Análise da estrutura do site https://www.ifad.org/en/; Desenvolvimento de código em python para a raspagem de dados, criando um branch para o pesquisador no https://github.com/mcti-sefip/mcti-sefip-ppfcd2020 e compartilhando o código desenvolvido.

def goodai1(path, keywords = '(brazil|latin america region)'): 
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = ['https://www.goodai.com/goodai-grants/']
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\goodai_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://www.goodai.com/goodai-grants/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sites = soup.find_all('div', class_ = 'col-sm-6 col-lg-4')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        keywords = 'brazil'

        for i in soup2.findAll('a'):
            info = i['href']
            links.append(info)   
            
        for i in links: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            titulo = soup3.find('h1').get_text()
            titulos.append(titulo)
            texto = soup3.find('div', class_ = 'entry-content').get_text()
            textos.append(clean(texto))
            if(findall(keywords, texto.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            if(findall('grant', texto.lower())):         
                tipos.append('grant')                
            elif(findall('fellowship', texto.lower())):  
                tipos.append('fellowship')          
            elif(findall('scholarship', texto.lower())): 
                tipos.append('scholarship')                   
            else:
                tipos.append('other')
            scrape.append(str(soup))
       
        df = pd.DataFrame()
        df['opo_titulo'] = titulos
        df['link'] = links
        df['opo_texto'] = textos 
        df['opo_texto_ele'] = textos
        df['opo_tipo'] = tipos
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'goodai_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em goodai1')
####

def goodai2(path):
    try: 
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\ goodai_02.csv'
        titulos = []
        textos = []
        links = []
        page = requests.get('https://www.goodai.com/blog/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sites = soup.find_all('article', class_ = 'new-item')
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')

        for i in soup2.find_all('a', class_= 'btn'):
            info = i['href']
            if info.startswith('https://www.goodai.com/'):
                new_info = info
                links.append(new_info)
            else:
                links.append(info)
        
        new_links = getNewInfo(links_base, links)

        if(new_links):
            for i in links:
                page = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                soup = BeautifulSoup(page.text, 'lxml')
                titulo = soup.find('h1').get_text()
                texto = soup.find('div', class_='entry-content').get_text()
                titulos.append(titulo)
                textos.append(clean(texto))
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'goodai_')
            df['atualizacao'] = [dia] * len(df.index)
            
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas notícias')
            shutil.copy(pathbase+filename, '.\\'+dia)
        
    except Exception as e:
        print(e)
        print('Erro em goodai2')
## Consertar problema de buscar tags junto com o link do "read more"

def goodai3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.goodai.com/about/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\goodai_03.csv'
        for link in links:
            page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = clean(soup.find('h1').text)
            #print(titulo)
            titulos.append(titulo)
            texto = clean(soup.find('p', class_='p-large').get_text())
            textos.append(texto)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['goodai']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'goodai_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em goodai3')

# def goodai4(path, keywords = '(brazil|latin america region)'):
#     try:
#         pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
#         dia = datetime.today().strftime('%y%m%d')
#         filename = '\\goodai_04.csv'
#         titulos = []
#         links = []
#         values = []
#         hasBrazil = []
#         prj_inst = []
#         links_base = getInfoBase(pathbase, filename, 'link')
#         link_response = requests.get('https://www.goodai.com/careers/').content.decode('utf-8')
#         soup = BeautifulSoup(link_response, 'lxml')
#         for prj in soup.find('article').find_all(class_='positions space-lg'):
#             link = prj.find('a')['href']
#             links.append('https://www.goodai.com/' + link)
#         new_links = getNewInfo(links_base, links)
#         if(new_links):
#             for link in new_links:
#                 page = requests.get(link).content.decode('utf-8')
#                 page_soup = BeautifulSoup(page, 'lxml')
#                 title = page_soup.find('h3', class_ = 'h4').text
#                 titulos.append(title)
#                 valor = page_soup.find('div', class_ = 'views-field views-field-field-awdamt').find('div', class_= 'field-content').text
#                 values.append(valor)   
#                 location = page_soup.find('div', class_ = 'views-field views-field-field-pldesc').find('div', class_= 'field-content').text 
#                 if(findall(keywords, location.lower())):
#                     hasBrazil.append('Y')
#                 else:
#                     hasBrazil.append('N')
#                 instituicao = page_soup.find('div', class_ = 'views-field views-field-field-orglegal').find('div', class_= 'field-content').text 
#                 prj_inst.append(instituicao)
#             df = pd.DataFrame()
#             df['prj_titulo'] = titulos 
#             df['link'] = new_links 
#             df['prj_instituicao'] = prj_inst
#             df['prj_valor'] = values
#             df['prj_brazil'] = hasBrazil
#             df['atualizacao'] = [dia]*len(df.index)
#             df['codigo'] = getCodList(dia, len(df.index), '_4_', 'goodai_')
#             df.to_csv(path+filename, index=False)
#         else:
#             print('Não há alteração em novas oportunidades')
#             shutil.copy(pathbase+filename, '.\\'+dia)
#     except Exception as e:
#         print(e)
#         print('Erro em goodai4')
