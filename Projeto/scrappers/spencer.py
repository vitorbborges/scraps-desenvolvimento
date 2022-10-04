# AB#40
# AB#148
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList
from re import findall
from utilidadesppf import getInfoBase, getNewInfo, clean
import shutil
from urllib.request import Request, urlopen

def spencer1(path, keywords = '(brazil|latin america region)'): 
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = ['https://www.spencer.org/research-grants']
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\spencer_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://www.spencer.org/research-grants', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        keywords = 'brazil'


        for i in soup.find_all('a', class_=re.compile("^bg")):
            info = i['href']
            #print(info)
            info = 'https://www.spencer.org/' + info
            links.append(info)  
            #print(links)
        links.remove('https://www.spencer.org//subscribers/new')
        links.pop(0)
   
        for i in links: 
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            titulo = soup3.find('h1', class_='h4 h1-md tape sky-blue text-white').get_text()
            titulos.append(clean(titulo))
            texto = soup3.find('div', class_ = 'col-lg-7 offset-lg-1 post-body').get_text()
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
        df['codigo'] = getCodList(dia, len(df.index), '1', 'spencer_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em spencer1')



def spencer2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\spencer_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.spencer.org/news').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup2 = soup.find('div', class_="row", id="articles")
        sopa = soup2.find_all('div', class_='col-md-4 d-flex flex-column')

        for new in sopa:
            link = new.find('a')['href']
            link = 'https://www.spencer.org' + link
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('h1').get_text())
                texto = clean(page_soup.find('div', class_= 'row mb-5').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'spencer_')
            df.to_csv(path + filename, index = False)
        else:
            print('Não há alteração em novas oportunidades')

    except Exception as e:
        print(e)
        print('Erro em spencer2')

def spencer3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\spencer_03.csv'
        titulos = []
        textos = []
        links = ['https://www.spencer.org/about-us', 'https://www.spencer.org/opportunities', 'https://www.spencer.org/financial-reports']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'container mb-3 mb-md-5').find('h1').get_text()
            texto = soup.find('div', class_ = 'row mb-5').get_text()
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['rockefellerfoundation']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'rockefellerfoundation_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em rockefellerfoundation3')   

def spencer4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0] + '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\spencer_4.csv'
        titulos = []
        links = []
        hasBrazil = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_response = requests.get('https://www.rufford.org/projects/?continent=central_and_latin_america&q=&sort_by=-created').content.decode('utf-8')
        soup = BeautifulSoup(link_response, 'lxml')
        for prj in soup.find_all('article', class_='project-listing-item'):
            link = 'https://www.rufford.org' + prj.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if (new_links):
            for link in new_links:
                req = Request(link, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page = urlopen(req).read()
                page_soup = BeautifulSoup(page, 'lxml')
                title = clean(page_soup.find('h2').text)
                titulos.append(title)
                text = clean(page_soup.find('div', class_='column is-8').get_text())
                if (findall(keywords, text.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
            df = pd.DataFrame()
            df['prj_titulo'] = titulos
            df['link'] = new_links
            df['prj_instituicao'] = ['Spencer'] * len(df.index)
            df['prj_valor'] = ['NA'] * len(df.index)
            df['prj_brazil'] = hasBrazil
            df['atualizacao'] = [dia] * len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'spencer_')
            df.to_csv(path + filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em spencer4')
