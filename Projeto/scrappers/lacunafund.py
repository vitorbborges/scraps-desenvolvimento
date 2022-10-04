import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList
from re import findall
from utilidadesppf import getInfoBase, getNewInfo, clean
import shutil
from selenium import webdriver

from urllib.request import Request, urlopen

#imports para sites com javascript
from bs4 import BeautifulSoup
from selenium import webdriver #importa o simulador de navegador
from selenium.webdriver.firefox.options import Options #importa as opções para paramtrizar o navegador
import requests
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.firefox.service import Service


def lacunafund1(path, keywords = '(brazil|latin america region)'): 
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links = ['https://lacunafund.org/apply/']
        titulos = []
        textos = []
        hasBrazil = []
        deadlines = []
        elegibilidade = []
        tipos = []
        scrape = []
        texto_elegivel = []
        filename = '\\lacunafund_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://lacunafund.org/apply/', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sites = soup.find_all('div', class_ = 'col-sm-12 col-md-7 offset-md-1')
        keywords = 'brazil'
            
        for i in links: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            titulo = soup3.find('h3').get_text()
            titulos.append(titulo)
            texto = soup3.find('p').get_text()
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
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'lacunafund_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em lacunafund1')
####
def lacunafund2(path):
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
        filename = '\\lacunafund_02.csv'
        dia = datetime.today().strftime('%y%m%d') 

        #inicio selenium
        options = Options() #adiciona argumentos
        options.add_argument('--headless')
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument('window-size=400,800') #parametriza o tamanho da janela
        drivepath=Service(r'C:\Users\vitor\Desktop\Education\LAMFO\Projetos\#mcti_datascience\Github\Testes de Código\geckodriver.exe')
        navegador = webdriver.Firefox(service=drivepath, options=options) #escolha do navegador que será usado
        navegador.get('https://lacunafund.org/news/') #acesso ao site
        # print(navegador.page_source)
        sleep(2)

        soup = BeautifulSoup(navegador.page_source, 'lxml')

        #fim selenium
        keywords = 'brazil'


        for i in soup.find_all('div', class_='border-flat position-relative listing-item'):
            info = i.find('a')['href']
            if info.startswith('http'):
                links.append(info)

            else:
                info = 'https://www.lacunafund.org/' + info
                links.append(info)  


            
        for i in links: 
            page = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup = BeautifulSoup(page.text, 'lxml')
            titulo = soup.find('h1').text
            texto = soup.find('div', class_='content-text').text
            titulos.append(titulo)
            textos.append(clean(texto))
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'lacunafund_')
        df.to_csv(path + filename, index = False)

    except Exception as e:
        print(e)
        print('Erro em lacunafund2')

def lacunafund3(path):
    try:
        titulos = []
        textos = []
        link = 'https://lacunafund.org/governance-2/'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\lacunafund_03.csv'
        page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')

        for i in soup.find_all('section', class_="accordion py-3"):
            titulo = i.find('span', class_= 'flex-grow-1').text
            titulos.append(clean(titulo))
            texto = i.find('div', class_='py-2 accordion__content').text
            textos.append(clean(texto))

        
        df = pd.DataFrame()
        df['pol_titulo'] = pd.Series(titulos)
        df['pol_instituicao'] = ['lacunafund']*len(df.index)
        df['pol_texto'] = pd.Series(textos)
        df['link'] = (link)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'lacunafund_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em lacunafund3')