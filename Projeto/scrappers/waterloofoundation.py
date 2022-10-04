# AB#155
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
from utilidadesppf import getCodList, clean
from re import findall
from urllib.request import Request, urlopen

def waterloofoundation1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\waterloofoundation_01.csv'
        titles = [] 
        links = ['http://www.waterloofoundation.org.uk/WorldDevelopmentSexualandReproductiveHealth.html', 'http://www.waterloofoundation.org.uk/WorldDevelopmentNutrition.html', 'http://www.waterloofoundation.org.uk/WorldDevelopmentEducation.html', 'http://www.waterloofoundation.org.uk/WorldDevelopmentWaterSanitationHygiene.html', 'http://www.waterloofoundation.org.uk/EnvironmentTropicalRainforests.html', 'http://www.waterloofoundation.org.uk/EnvironmentMarine.html', 'http://www.waterloofoundation.org.uk/ChildDevelopmentAboutTheProgramme.html', 'http://www.waterloofoundation.org.uk/WalesAboutTheProgramme.html'] 
        deadlinelink = 'http://www.waterloofoundation.org.uk/EnvironmentApplications.html'
        request = requests.get(deadlinelink).content.decode('utf-8')
        soup = BeautifulSoup(request, 'lxml')
        deadlines_env = []
        track = soup.find_all('ul', type = 'disc')[:2]
        for data in track:
            deadline = data.get_text()
            deadline = re.sub('\n', '-', deadline)
            deadline = deadline[1:-1]
            deadlines_env.append(deadline)
        deadlines = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        ano = "20" + str(datetime.today().strftime("%y"))
        dia = datetime.today().strftime("%y%m%d")
        for link in links:
            page_response = requests.get(link).content.decode('utf-8')
            soup = BeautifulSoup(page_response, 'lxml')
            if(soup.find('h2') is not None):
                titulo = soup.find('h2').get_text()
            if(titulo.isspace() or titulo == ''):
                titulo = str(soup.find('h1').text)
            titles.append(titulo)
            if(soup.find('td', width = '540') is not None):
                text = soup.find('td', width = '540').get_text()
                text = re.sub('\n', ' ', text)
                text = ' '.join(text.split())
            elif(soup.find('td', width = '535') is not None):
                text = soup.find('td', width = '535').get_text()
                text = re.sub('\n', ' ', text)
                text = ' '.join(text.split())
            else:
                text = soup.find_all('td', valign = 'top')[3].get_text()
                text = re.sub('\n', ' ', text)
                text = ' '.join(text.split())
            texts.append(text)

            if(soup.find('h1').text == 'Environment'):
                deadlines.append(deadlines_env.pop())
            else:
                deadlines.append('31 de dezembro de ' + ano)
            if(findall(keywords, text.lower())):
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
        df['link'] = links  
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'waterloofoundation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em waterloofoundation1')


def waterloofoundation3(path):
    try:
        titulos = []
        textos = []
        links = ['http://www.waterloofoundation.org.uk/AboutUs.html', 'http://www.waterloofoundation.org.uk/History.html']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\waterloofoundation_03.csv'
        req = Request(links[0], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').get_text())
        titulos.append(titulo)
        texto = clean(soup.find_all('td', valign='top')[4].get_text())
        textos.append(texto)
        
        req = Request(links[1], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1').get_text())
        titulos.append(titulo)
        texto = clean(soup.find_all('td', valign='top')[3].get_text())
        textos.append(texto)

        req = Request('http://www.waterloofoundation.org.uk/index.html', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h2').get_text())
        titulos.append(titulo)
        texto = clean(soup.find_all('div', align = 'center')[6].get_text())
        textos.append(texto)
        links.append('http://www.waterloofoundation.org.uk/index.html')
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['waterloofoundation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'waterloofoundation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em waterloofoundation3')

