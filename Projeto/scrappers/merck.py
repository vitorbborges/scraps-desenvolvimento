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

#java
from bs4 import BeautifulSoup
from selenium import webdriver #importa o simulador de navegador
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options #importa as opções para paramtrizar o navegador
import requests
from bs4 import BeautifulSoup
from time import sleep

def merck1(path, keywords = '(brazil|latin america region)'): 
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = []
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\merck_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = Request('https://www.merckgroup.com/en/research/open-innovation/research-grants.html', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        sopa = soup.find('div', class_='par parsys')

        keywords = 'brazil'

        link = 'https://www.merckgroup.com/en/research/open-innovation/research-grants.html'

        


        for i in sopa.find_all('div', class_='text-image section'): 
            titulo = i.find('h2', class_='text-image-block-content-title').text
            titulos.append(clean(titulo))
            texto = i.find('p', class_ = 'text-image-block-content-text flush-bottom').find('span').text
            textos.append(clean(texto))
            #print(titulos)
            #print(textos)
            links.append('https://www.merckgroup.com/en/research/open-innovation/research-grants.html')
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
        df['opo_titulo'] = pd.Series(titulos)
        df['link'] = pd.Series(links)
        df['opo_texto'] = pd.Series(textos) 
        df['opo_texto_ele'] = pd.Series(textos)
        df['opo_tipo'] = pd.Series(tipos)
        df['codigo'] = getCodList(dia, len(df.index), '1', 'merck_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        #print(df)
        
    except Exception as e:
        print(e)
        print('Erro em merck1')



def merck2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = []
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\merck_02.csv'
        dia = datetime.today().strftime('%y%m%d') 
        options = Options() #adiciona argumentos
        options.add_argument('--headless')  #essa option quando ativada esconde o processo visivel do navegador. desativar apenas quando tiver finalizado os ajustes.
        options.add_argument("disable-blink-features=AutomationControlled") #tem sites que bloqueiam o selenium. essa option serve pra isso
        options.add_argument('window-size=400,800') #parametriza o tamanho da janela
        drivepath=Service(r'C:\Users\vitor\Desktop\Education\LAMFO\Projetos\#mcti_datascience\Github\Testes de Código\geckodriver.exe')
        navegador = webdriver.Firefox(service=drivepath, options=options) #escolha do navegador que será usado
        navegador.get('https://www.merckgroup.com/en/news.html') #acesso ao site
        sleep(2) #esse sleep da tempo para o navegador carregar a página
        soup = BeautifulSoup(navegador.page_source, 'lxml') #esse é o novo soup com o selenium. a partir daqui não tem nada novo. 
        sopa = soup.find('ol', class_="archive-list-template__results-list")

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
            info = info
            links.append(info)

            
        for i in links: 
            page2 = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request2 = urlopen(page2).read()
            soup3 = BeautifulSoup(page_request2, 'lxml')
            pretitulo = soup3.find('div', class_='ns-header-content')
            titulo = pretitulo.find('h1').get_text()
            titulos.append(clean(titulo))
            #print(titulos)
            texto = soup3.find('div', class_ = 'ns-text__body').text
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
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'merck_')
        df.to_csv(path + filename, index = False)

    except Exception as e:
        print(e)
        print('Erro em agropolis2')

def merck3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\merck_03.csv'
        titulos = []
        textos = []
        links = ['https://www.merckgroup.com/en/company.html']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('div', class_ = 'sm-col-6 md-col-10 lg-col-10 xl-col-12').find('h1').get_text()
            #print(titulo)
            texto = soup.find('div', class_ = 'text-block-content').get_text()
            #print(texto)
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['merck']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'merck_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em merck3')   


