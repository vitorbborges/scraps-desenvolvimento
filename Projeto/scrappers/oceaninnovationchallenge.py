# AB#135
from utilidadesppf import getNewInfo, getInfoBase, getCodList, clean
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime
from urllib.request import Request, urlopen
def oceaninnovationchallenge1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\oceaninnovationchallenge_01.csv'
        titles = [] 
        links = ['https://oceaninnovationchallenge.org/call-for-innovations/1st-call-marine-pollution-reduction', 'https://oceaninnovationchallenge.org/call-for-innovations/2nd-call-sustainable-fisheries', 'https://oceaninnovationchallenge.org/call-for-innovations/3rdcall'] #
        texts = [] 
        hasBrazil = [] 
        types = [] 
        dia = datetime.today().strftime("%y%m%d")
        for link in links:
            page_request = requests.get(link).content.decode('utf-8')
            page_soup = BeautifulSoup(page_request, 'lxml')
            titulo = page_soup.find('h3', class_='c-font-sbold').text
            titles.append(titulo)

            text = ''
            text_area = page_soup.find('article', role = 'article').find('div', class_= 'field field--name-body field--type-text-with-summary field--label-hidden field__item')
            for p in text_area.find_all('p'):
                text +=p.text
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
        df['opo_deadline'] = ['deadline nao encontrada']*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'oceaninnovationchallenge_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em oceaninnovationchallenge1')
        

def oceaninnovationchallenge3(path):
    try:
        titulos = []
        textos = []
        i = 0
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\oceaninnovationchallenge_03.csv'
        page = requests.get('https://oceaninnovationchallenge.org/#what-it-does') # Request para extrair a página html
        soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
        for pol in soup.find_all('div', class_='c-body'):
            titulo = clean(pol.find('h3').text)
            titulos.append(titulo)
            texto = clean(pol.get_text())
            textos.append(texto)
            i+=1
            if i == 3:
                break
        titulos.append(clean(soup.find('h3').text))
        textos.append(clean(soup.find('div', class_='fadeIn what-it-is-text wow').get_text()))
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['oceaninnovationchallenge']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = ['https://oceaninnovationchallenge.org/#what-it-does']*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'oceaninnovationchallenge_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em oceaninnovationchallenge3')
