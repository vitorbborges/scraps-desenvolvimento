# AB#151
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re
from utilidadesppf import getCodList, clean
from re import findall
import requests
from urllib.request import Request, urlopen
def rapidresponse1(path, keywords = '(brazil|latin america region|oecd)'):
    try:
        filename = '\\rapidresponse_01.csv'
        titles = [] 
        links = [] 
        texts = [] 
        hasBrazil = [] 
        types = [] 
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime("%y")) 
        request = requests.get('https://www.rapid-response.org/apply-2/').content.decode('UTF-8')
        soup = BeautifulSoup(request, 'lxml')
        titulo = soup.find('h1', class_='sow-headline').text + ' RPF'
        titles.append(titulo)

        links.append('https://www.rapid-response.org/apply-2/')

        deadline = '31 de dezembro de ' + ano

        text = soup.find('div', class_='siteorigin-widget-tinymce textwidget').get_text()
        text = re.sub('\n', ' ', text)
        text = ' '.join(text.split())
        texts.append(text)
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
        df['opo_deadline'] = [deadline]
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'rapidresponse_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em rapidresponse1')


def rapidresponse3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.rapid-response.org/about/', 'https://www.rapid-response.org/our-impact/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\rapidresponse_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='sow-headline').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='so-widget-sow-editor so-widget-sow-editor-base').get_text())
            textos.append(texto)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['rapidresponse']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'rapidresponse_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em rapidresponse3')
