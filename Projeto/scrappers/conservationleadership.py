# AB#114
from utilidadesppf import getCodList, clean, getNewInfo, getInfoBase
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
import requests
from datetime import datetime, date
import shutil
from urllib.request import Request, urlopen

def conservationleadership1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\conservationleadership_01.csv'
        titles = [] #
        deadlines = [] #
        texts = [] #
        hasBrazil = [] #
        types = [] #
        dia = datetime.today().strftime("%y%m%d")
        ano = date.today().year
        hoje = datetime.now()
        data_base = "30/4/" + str(ano)
        data_base = datetime.strptime(data_base, "%d/%m/%Y")

        page_request = requests.get('https://www.conservationleadershipprogramme.org/grants/grant-overview/future-conservationist-award/').content.decode('utf-8')
        page_soup = BeautifulSoup(page_request, 'lxml')
        titulo = page_soup.find('h1', class_='entry-title').text
        titles.append(titulo)
        text = clean(page_soup.find('article', class_='page-left').get_text())
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

        if(hoje > data_base):
            deadline = '31 de dezembro de ' + str(int(ano) + 1)
        else:
            deadline = '31 de dezembro de ' + str(ano)
        deadlines.append(deadline)
        df = pd.DataFrame()          
        df['opo_titulo'] = titles  
        df['link'] = ['https://conservationleadership.si.edu/opportunities/grants-program']    
        df['opo_texto'] = texts   
        df['opo_texto_ele'] = texts
        df['opo_brazil'] = hasBrazil   
        df['opo_tipo'] = types      
        df['opo_deadline'] = deadlines   
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'conservationleadership_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + filename, index = False)
    except Exception as e:
        print(e)
        print('Erro em conservationleadership1')






def conservationleadership2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\conservationleadership_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.conservationleadershipprogramme.org/media-centre/news/').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', class_='page-left')
        for new in soup.find_all('div', class_='listing-item-wrapper'):
            link = new.find('a')['href']
            if link not in links:
                links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('h2', class_='entry-title').get_text())
                texto = clean(page_soup.find('div', class_='entry-content').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['atualizacao'] = [dia]*len(df.index)
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'conservationleadership_')
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em conservationleadership2')


def conservationleadership3(path):
    try:
        titulos = []
        textos = []
        links = ['https://www.conservationleadershipprogramme.org/about-us/clp-partners/', 'https://www.conservationleadershipprogramme.org/about-us/who-we-are/']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\conservationleadership_03.csv'
        for link in links:
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1', class_='entry-title').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='page-wide').get_text())
            textos.append(texto)
        
        links.append('https://www.conservationleadershipprogramme.org/grants/grant-overview/')
        page = requests.get('https://www.conservationleadershipprogramme.org/grants/grant-overview/').text
        soup = BeautifulSoup(page, 'lxml')
        titulo = clean(soup.find('h1', class_='entry-title').text)
        titulos.append(titulo)
        texto = clean(soup.find('article', class_='page-left').get_text())
        textos.append(texto)

        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['conservationleadership']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'conservationleadership_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em conservationleadership3')


def conservationleadership4(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\conservationleadership_04.csv'
        titles = [] 
        links = []
        instituicoes = []
        hasBrazil = []
        values = []
        taxas = []
        dia = datetime.today().strftime("%y%m%d")
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://www.conservationleadershipprogramme.org/our-projects/awards-provided/').text
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('table', id = 'grants-by-taxa').find('tbody')
        for taxa in soup.find_all('td', class_='stats-figure'):
            taxa = taxa.text
            taxas.append(taxa)
        page = requests.get('https://www.conservationleadershipprogramme.org/our-projects/supported-projects/').text
        soup = BeautifulSoup(page, 'lxml')
        for prj in soup.find_all('a', class_='read-more'):
            link = prj['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                request = requests.get(link).content.decode('utf-8')
                soup = BeautifulSoup(request, 'lxml')
                titulo = clean(soup.find('h1', class_='entry-title').text)
                titles.append(titulo)
                category = clean(soup.find('div', id = 'taxa-icon').text.split(':')[1])
                category = category.lower()
                if(category == 'amphibian'):
                    values.append(taxas[0])
                elif(category == 'bird'):
                    values.append(taxas[1])
                elif(category == 'fish'):
                    values.append(taxas[2])
                elif(category == 'invertebrate'):
                    values.append(taxas[3])
                elif(category == 'mammal'):
                    values.append(taxas[4])
                elif(category == 'multiple taxa'):
                    values.append(taxas[5])
                elif(category == 'plant'):
                    values.append(taxas[6])
                elif(category == 'reptile'):
                    values.append(taxas[7])
                location = clean(soup.find('div', id = 'project-data').get_text())
                if(findall(keywords, location.lower())):
                    hasBrazil.append('Y')
                else:
                    hasBrazil.append('N')   
            df = pd.DataFrame()       
            df['prj_titulo'] = titles #
            df['link'] = new_links#
            df['prj_brazil'] = hasBrazil   #
            df['prj_instituicao'] = ['ConservationLeadership']*len(df.index)
            df['prj_valor'] = values   
            df['codigo'] = getCodList(dia, len(df.index), '_4_', 'conservationleadership_')
            df['atualizacao'] = [dia]*len(df.index)
            df.to_csv(path + filename, index = False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em conservationleadership4')

