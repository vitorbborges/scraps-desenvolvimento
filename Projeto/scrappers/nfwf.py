# AB#99
from utilidadesppf import getCodList, getInfoBase, getNewInfo, clean
from bs4 import BeautifulSoup
import pandas as pd
import re
from re import findall
import requests
from datetime import datetime
import shutil
from urllib.request import Request, urlopen

def nfwf1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\nfwf_01.csv'
        titles = [] #
        links = [] #
        deadlines = [] 
        texts = []
        hasBrazil = [] #
        types = [] #
        dia = datetime.today().strftime("%y%m%d")
        ano = '20' + str(datetime.today().strftime("%y"))
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        page_request = requests.get('https://www.nfwf.org/apply-grant').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        for table in page_soup.find_all('tbody'):
            for opo in table.find_all('tr'):
                link = opo.find('a')['href']
                if(link[0] == '/'):
                    links.append('https://www.nfwf.org' + link)
                else:
                    links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page_request = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page_request, 'lxml')
                titulo = page_soup.find('div', class_='hero__content-container').find('h1').get_text()
                titulo = clean(titulo)
                titles.append(titulo)
                text = clean(page_soup.find('div', class_='p-wrap').get_text())
                texts.append(text)
                if(page_soup.find('td', class_='views-field views-field-field-due-date') is not None):
                    deadline = page_soup.find('td', class_='views-field views-field-field-due-date').get_text()
                else:
                    deadline = '31 de dezembro de ' + ano
                deadlines.append(deadline)

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
            df['link'] = new_links    
            df['opo_texto'] = texts
            df['opo_texto_ele'] = texts
            df['opo_brazil'] = hasBrazil   
            df['opo_tipo'] = types      
            df['opo_deadline'] = deadlines   
            df['codigo'] = getCodList(dia, len(df.index), '_1_', 'nfwf_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em nfwf1')




def nfwf2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\nfwf_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.nfwf.org/media-center/announcements').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        for new in soup.find_all('div', class_='announcements__columns'):
            link = new.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                #print(link)
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                if(page_soup.find('div', class_='sectionnav__li') is not None):
                    titulo = clean(page_soup.find('div', class_='sectionnav__li').get_text())
                    texto = clean(page_soup.find('section', class_='overview').get_text())
                elif(page_soup.find('div', class_='overview__column')is not None):
                    titulo = clean(page_soup.find('div', class_='hero__content-container').find('h1').get_text())
                    texto = clean(page_soup.find('div', class_='overview__column').get_text())
                else:
                    titulo = clean(page_soup.find('div', class_='hero__content-container').find('h1').get_text())
                    texto = clean(page_soup.find('div', class_='standard-content__column').get_text())
                #print(titulo)
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'nfwf_')
            df['atualizacao'] = [dia]*len(df.index)
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em nfwf2')


def nfwf3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.nfwf.org/what-we-do', 'https://www.nfwf.org/strategies-results/conservation-science', 'https://www.nfwf.org/strategies-results/business-plans', 'https://www.nfwf.org/strategies-results/evaluating-our-results']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\nfwf_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1').text)
            #print(titulo)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='standard-content__column').get_text())
            textos.append(texto)
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['nfwf']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'nfwf_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em nfwf3')


def nfwf4(path, keywords = '(brazil|latin america region)'):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\nfwf_04.csv'
        titulos = []
        links = []
        values = []
        hasBrazil = []
        prj_inst = []
        links_base = getInfoBase(pathbase, filename, 'link')
        link_response = requests.get('https://www.nfwf.org/grants/grants-library?field_idyear_value=2021&field_idyear_value_1=2021').content.decode('utf-8')
        soup = BeautifulSoup(link_response, 'lxml')
        for prj in soup.find('tbody').find_all('tr'):
            link = prj.find('a')['href']
            links.append('https://www.nfwf.org/' + link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                title = page_soup.find('div', class_ = 'views-field views-field-title').find('span', class_= 'field-content').text
                titulos.append(title)
                valor = page_soup.find('div', class_ = 'views-field views-field-field-awdamt').find('div', class_= 'field-content').text
                values.append(valor)   
                location = page_soup.find('div', class_ = 'views-field views-field-field-pldesc').find('div', class_= 'field-content').text 
                if(findall(keywords, location.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')
                instituicao = page_soup.find('div', class_ = 'views-field views-field-field-orglegal').find('div', class_= 'field-content').text 
                prj_inst.append(instituicao)
            df = pd.DataFrame()
            df['prj_titulo'] = titulos 
            df['link'] = new_links 
            df['prj_instituicao'] = prj_inst
            df['prj_valor'] = values
            df['prj_brazil'] = hasBrazil
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'nfwf_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em nfwf4')
