import bs4
from bs4 import BeautifulSoup, SoupStrainer
from bs4.dammit import EncodingDetector
import re
from re import findall
import pandas as pd
import requests
from collections import OrderedDict
from urllib.request import Request, urlopen
import urllib
from datetime import datetime
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo
import os

def grupoboticario3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\grupoboticario_03.csv'
        titulos = []
        titulos2 = []
        titulos3 = []
        textos = []
        textos2 = []
        textos3 = []
        links = ['http://www.fundacaogrupoboticario.org.br/pt/quem-somos/Paginas/Inicial.aspx', 'http://www.fundacaogrupoboticario.org.br/pt/solucoes-inovadoras/Paginas/Inicial.aspx', 'http://www.fundacaogrupoboticario.org.br/pt/conservacao-biodiversidade/Paginas/Apoio-a-projetos.aspx']
        
        page = Request(links[0], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('span', class_ = "ms-rteStyle-TituloGrande").get_text()
        texto = soup.find('div', class_ = 'quem-somos-content').get_text()
        titulos.append(titulo)
        textos.append(clean(texto))
        
        page2 = Request(links[1], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})      
        page_request2 = urlopen(page2).read()
        soup2 = BeautifulSoup(page_request2, 'lxml')
        titulo2 = soup2.find('div', class_ = "ms-rtestate-field").get_text()
        texto2 = soup2.find('div', class_ = 'solucoes-content').get_text()
        titulos2.append(titulo2)
        textos2.append(clean(texto2))
        
        page3 = Request(links[2], headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})      
        page_request3 = urlopen(page3).read()
        soup3 = BeautifulSoup(page_request3, 'lxml')
        titulo3 = soup3.find('span', class_ = "ms-rteStyle-TituloGrandeInicial").get_text()
        texto3 = soup3.find('div', class_ = 'conservacao-editais-content').get_text()
        titulos3.append(titulo3)
        textos3.append(clean(texto3))
        
        df = pd.DataFrame()
        df['pol_titulo'] = (titulos + titulos2 + titulos3)
        df['pol_instituicao'] = ['grupoboticario']*len(df.index)
        df['pol_texto'] = (textos + textos2 + textos3)
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'grupoboticario_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
                
    except Exception as e:
        print(e)
        print('Erro em grupoboticario3')
        
#grupoboticario3(os.getcwd())

def grupoboticario4(path, keywords = 'brazil'):
    
    try:

        dia = datetime.today().strftime('%y%m%d')
        filename = '\\grupoboticario_04.csv'
        titulos = []
        valor = []
        hasBrazil = []
        prj_inst = []
        links = ['http://www.fundacaogrupoboticario.org.br/pt/solucoes-inovadoras/Paginas/Rede-Oasis.aspx']
        page = Request('http://www.fundacaogrupoboticario.org.br/pt/solucoes-inovadoras/Paginas/Rede-Oasis.aspx', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('span', class_ = 'ms-rteStyle-TituloGrande').get_text()
        titulos.append(titulo)
        texto = soup.find('section', class_ = 'oasis').text
        
        if(findall(keywords, texto.lower())):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
        instituicao = 'Grupo Boticário'
        prj_inst.append(instituicao)
        valor.append('Valor não encontrado')
        
        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = links
        df['prj_instituicao'] = prj_inst
        df['prj_valor'] = valor
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'grupoboticario_')
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em grupoboticario4')
    
#grupoboticario4(os.getcwd())
