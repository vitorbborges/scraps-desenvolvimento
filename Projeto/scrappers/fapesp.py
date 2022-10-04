# AB#62
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from re import findall
from utilidadesppf import getCodList, getNewInfo, clean, getInfoBase
import requests
from datetime import datetime
from itertools import compress
import shutil
from googletrans import Translator
from urllib.request import Request, urlopen
#utilizada uma versão mais antiga (versão atual fora de funcionamento)

#TODO LIST
#opo_titulo --
#link --
#opo_deadline --
#opo_texto --
#opo_tipo --
#opo_brazil --
#codigo --
#atualizacao --

def getLinksBase(path, filename):
    links_base = []
    path = path + filename
    try:
        dfbase = pd.read_csv(path)
        links_base=(dfbase['link'].tolist())
    except:
        pass
    return links_base
def fapesp1(path, keywords = '(brazil|latin america region)'):
    try:
        filename = '\\fapesp_01.csv'
        titles = []
        links = []
        deadlines = []
        texts = []
        dia = datetime.today().strftime("%y%m%d")        
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        links_base = getLinksBase(pathbase, filename)
        page_link = 'https://fapesp.br/oportunidades/'
        page = requests.get(page_link).content.decode('utf-8')
        page_soup = BeautifulSoup(page, 'lxml')
        toggle = True
        pre_soup = page_soup.find('ul', class_ = 'list')
        for widget in pre_soup.find_all('li'):
            if toggle and widget['class'] != ['wrap_actions']:
            #------------TITULOS-------------------
                title = widget.find('strong').text
                titles.append(title)
                #----------LINKS----------------------
                link = widget.find('a')['href']
                links.append('http://fapesp.br' + link)
                #---------DEADLINES-------------------
                deadline = widget.find('span', class_ = 'text-principal').text
                deadline = deadline.split('\n')[3].split(':')[1]
                deadlines.append(deadline)
            toggle = not toggle
        
        boleano =[i in links_base for i in links] #links que estão no df da base
        link_add = [not bool for bool in boleano] #inverte a lista para os links que nao estao
        links=(list(compress(links,link_add))) #links à serem adicionados ao CSV da base principal (novoglinks)
        titles = (list(compress(titles,link_add))) # fazendo o mesmo para o título
        deadlines = (list(compress(deadlines, link_add))) #faz o mesmo com as deadlines
        if(links):
            for link in links:
                text = ''
                link_request = requests.get(link).content.decode('utf-8')
                link_soup = BeautifulSoup(link_request, 'lxml')
                #-------------------TEXTOS-------------------
                resumo = link_soup.find('div', class_= 'resumo pt')
                for p in resumo.find_all('p'):
                    text += p.text
                texts.append(text)
            df = pd.DataFrame()
            df['opo_titulo'] = titles
            df['link'] = links
            df['opo_texto'] = texts
            df['opo_texto_ele'] = texts
            df['opo_brazil'] = ['Y']* len(df.index)
            df['opo_tipo'] = ['scholarship'] * len(links)
            df['opo_deadline'] = deadlines
            df['codigo'] = getCodList(dia, len(links), '_1_', 'fapesp_')
            df['atualizacao'] = [dia]* len(links)
            
            
            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em fapespR1')


def fapesp2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\fapesp_02.csv'
        titulos = []
        textos = []
        links = []
        links_base = getInfoBase(pathbase, filename, 'link')
        page = requests.get('https://fapesp.br/noticias').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('ul', class_='newsList')
        for new in soup.find_all('li'):
            link = new.find('a')['href']
            links.append(link)
        new_links = getNewInfo(links_base, links)
        if(new_links):
            for link in new_links:
                page = requests.get(link).content.decode('utf-8')
                page_soup = BeautifulSoup(page, 'lxml')
                titulo = clean(page_soup.find('h2', class_='b').get_text())
                texto = clean(page_soup.find('div', class_='page-body').get_text())
                titulos.append(titulo)
                textos.append(texto)
            df = pd.DataFrame()
            df['not_titulo'] = titulos
            df['link'] = new_links
            df['not_texto'] = textos
            df['codigo'] = getCodList(dia, len(df.index), '_2_', 'fapesp_')
            df['atualizacao'] = [dia]*len(df.index)

            df.to_csv(path+filename, index=False)
        else:
            #print('Não há alteração em novas oportunidades')
            shutil.copy(pathbase+filename, '.\\'+dia)
    except Exception as e:
        print(e)
        print('Erro em fapesp2')




def fapesp3(path):
    try:
        titulos = []
        textos = []
        dia = datetime.today().strftime('%y%m%d')
        links = ['https://fapesp.br/sobre/', 'https://fapesp.br/6/estrategias-de-fomento-a-pesquisa']
        filename = '\\fapesp_03.csv'
        for link in links:
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h1').find('span').text)
            titulos.append(titulo)
            texto = clean(soup.find('div', class_='page-body').get_text())
            #translator = Translator()
            #texto = translator.translate(texto).text
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['fapesp']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'fapesp_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em fapesp3')

