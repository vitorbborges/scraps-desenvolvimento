#AB #122

import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
import requests
from urllib.request import Request, urlopen
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo


# news protegido por javascript;

def climateworks3(path):
    try: 
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\climateworks_03.csv'
        titulos = []
        textos = []
        links = ['https://www.climateworks.org/about-us/', 'https://www.climateworks.org/about-us/financial-information/', 'https://www.climateworks.org/about-us/funding-partners/', 'https://www.climateworks.org/about-us/regional-partners/']

        for i in links:
                page = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                soup = BeautifulSoup(page.text, 'lxml')
                titulo = soup.find('div', class_ = 'header-content').get_text()
                texto = soup.find('div', class_ = 'et_pb_code_inner').get_text()
                titulos.append(clean(titulo))
                textos.append(clean(texto))
                
        df = pd.DataFrame()
        df['pol_titulo'] = titulos 
        df['pol_instituicao'] = ['climateworks']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'climateworks_')
        df['atualizacao'] = [dia] * len(df.index)
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em climateworks')
        
#climateworks3('.')

def climateworks4(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\climateworks_04.csv'
        titulos = []
        texto = []
        values = []
        links = []
        acesso = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_page = 'https://www.climateworks.org/grants-database/?sort_by=newest&posts_per_page=0'
        #page_response = requests.get('https://www.climateworks.org/grants-database/').content.decode('UTF-8')
        #soup = BeautifulSoup(page_response, 'lxml')
        
        
        for i in range(20):
            page = requests.get(link_page).content.decode('utf-8')
            page_soup = BeautifulSoup(page, 'lxml')

        for proj in page_soup.find('div', class_="programs-list").find_all('div', class_='program'):    #for proj in page_soup.find('div', class_='col-12 grant-list-item md-pvxs'):
            if len(links) > 9:
                break
            else:
                link = proj.find('a')['href']
                links.append('https://www.climateworks.org' + link)
                title = proj.find('div', class_ = 'program-name').find('h5').text
                titulos.append(title)
                valor = proj.find('div', class_= 'mtxxs').find('strong').text
                valor = re.sub(' ', '', valor)
                values.append(valor)  

                #link_page = page_soup.find('a', class_="next page-numbers").find(href=True)
                #link_page = 'https://www.climateworks.org/grants-database/?json=&sort_by=newest&posts_per_page=20' + page_soup.find('div', class_= 'nav-links').find('a')['href']  

        df = pd.DataFrame()
        df['prj_titulo'] = titulos
        df['link'] = links 
        df['prj_instituicao'] = ['Climateworks']*len(df.index)
        df['prj_valor'] = values
        df['prj_brazil'] = ['Y']*len(df.index)
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'iadb_')
        df.to_csv(path+filename, index=False)
                
                      


            # titulo = i.get_text()
            # titulos.append(titulo)
            
        # for i in soup.find_all('article'):
        #     text = i.text
        #     texto.append(text)
        #     if(findall(keywords, text.lower())):
        #         hasBrazil.append('Y')
        #     else:
        #         hasBrazil.append('N')
            
        # for i in soup.find_all('span', attrs={'class': 'amount grant__content'}):
        #     value = i.get_text()
        #     valor.append(value)
        #     instituicao = 'climateworks'
        #     prj_inst.append(instituicao)

        # df = pd.DataFrame()
        # df['prj_titulo'] = titulos
        # df['link'] = links*len(df.index)
        # df['prj_instituicao'] = prj_inst
        # df['prj_valor'] = valor
        # df['prj_brazil'] = hasBrazil
        # df['atualizacao'] = [dia]*len(df.index)
        # df['codigo'] = getCodList(dia, len(df.index), '_4_', 'climateworks_')
        # df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em climateworks4')   
        
#climateworks4('.')
