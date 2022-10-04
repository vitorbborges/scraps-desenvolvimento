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

def agropolis1(path, keywords = '(brazil|latin america region)'): 
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
        filename = '\\agropolis_01.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://www.agropolis-fondation.fr/Calls-for-proposals', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sopa = soup.find('section', style='background-image: url(image/bg_paralax1.jpg)')

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
            info = 'https://www.agropolis-fondation.fr/' + info
            links.append(info)  

        links.remove('https://www.agropolis-fondation.fr/https://oneplanetfellowship.org')

        for i in links: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            titulo = soup3.find('div', class_='bloc fd_8').find('h1').text
            titulos.append(clean(titulo))
            texto = soup3.find('div', class_ = 'col-md-8 col-sm-7').get_text()
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
        df['codigo'] = getCodList(dia, len(df.index), '1', 'agropolis_')
        df['atualizacao'] = [dia]*len(links)
        df.to_csv(path+filename, index=False)
        #print(df)
        
    except Exception as e:
        print(e)
        print('Erro em agropolis1')

#agropolis1('.')

def agropolis2(path):
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
        filename = '\\agropolis_02.csv'
        dia = datetime.today().strftime('%y%m%d') 
        page = requests.get('https://www.agropolis-fondation.fr/News', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        soup = BeautifulSoup(page.text, 'lxml')
        sopa = soup.find('section', style='background-image: url(image/bg_paralax1.jpg)')

        keywords = 'brazil'


        for i in sopa.find_all('a'):
            info = i['href']
            info = 'https://www.agropolis-fondation.fr/' + info
            links.append(info)  

            
        for i in links: 
            page2 = requests.get(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            soup3 = BeautifulSoup(page2.text, 'lxml')
            pretitulo = soup3.find('div', class_='bloc fd_2')
            titulo = pretitulo.find('h1').get_text()
            titulos.append(clean(titulo))
            texto = soup3.find('div', class_ = 'col-md-8 col-sm-7').get_text()
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
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'agropolis_')
        df.to_csv(path + filename, index = False)

    except Exception as e:
        print(e)
        print('Erro em agropolis2')

def agropolis3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\agropolis_03.csv'
        titulos = []
        textos = []
        links = ['https://www.agropolis-fondation.fr/Procedures-and-evaluation', 'https://www.agropolis-fondation.fr/One-off-supports']

        for i in links:
            page_response = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            titulo = soup.find('section', class_ = 'intro').find('h1').get_text()
            #print(titulo)
            texto = soup.find('div', class_ = 'col-md-offset-1 col-md-10').get_text()
            #print(texto)
            titulos.append(clean(titulo))
            #print(titulos)
            textos.append(clean(texto))
            #print(textos)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['agropolis']*len(df.index)
        df['link'] = links
        df['pol_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'agropolis_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em agropolis3')   

def agropolis4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\agropolis_04.csv'
        titulos = []
        links = []
        paginas = []
        values = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_page = 'https://www.agropolis-fondation.fr/Projects'
        link_page2 = []

        page = requests.get(link_page).content.decode('utf-8')
        page_soup = BeautifulSoup(page, 'lxml')
        nume = page_soup.find_all('a', class_="lien_pagination")[-2].text
        numeint = (int(nume))

        for i in range(numeint - 1):
            i = requests.get(link_page).content.decode('utf-8')
            page_soup = BeautifulSoup(i, 'lxml')        
            link_page = 'https://www.agropolis-fondation.fr/' + page_soup.find('span', class_= 'next').find('a')['href']
            paginas.append(link_page)

        link_page2.append('https://www.agropolis-fondation.fr/Projects')
        link_page2 = link_page2 + paginas

        for z in link_page2:
            req = requests.get(z).content.decode('utf-8')
            sopa = BeautifulSoup(req, 'lxml')
            proj = sopa.find('section', style='background-image: url(image/bg_paralax1.jpg)').find_all('div', class_='card-projet my-2')
            for a in proj:
                link = a.find('a')['href']
                links.append('https://www.agropolis-fondation.fr/' + link)

      


        if(links):
            for link in links:
                page = requests.get(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
                page_soup = BeautifulSoup(page.text, 'lxml')
                title = page_soup.find('div', class_='row my-3').find('span', class_="surtitre").text
                titulos.append(clean(title))
                valor = page_soup.find('div', class_= 'info info3').find('p').text
                valor = re.sub(' ', '', valor)
                values.append(clean(valor))             
            df = pd.DataFrame()
            df['prj_titulo'] = titulos 
            df['link'] = links 
            df['prj_instituicao'] = ['agropolis']*len(df.index)
            df['prj_valor'] = values
            df['prj_brazil'] = ['Y']*len(df.index)
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'agropolis_')
            df.to_csv(path+filename, index=False)
        else:
            print('Não há alteração em novas oportunidades')

    except Exception as e:
        print(e)
        print('Erro em agropolis4')
