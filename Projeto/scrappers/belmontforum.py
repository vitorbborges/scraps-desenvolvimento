# ----------------------------------------------------------
# Código novo após a mudança do site (21/12/2020)
# ----------------------------------------------------------
#  AB#42
# Comentario da PO:
# O que foi capturado esta aderente com OPORTUNIDADES ABERTAS no ppf, mas nao é suficviente para alimentar o ppf. Falta deadline.
# R: As deadlines estão em documento word anexo baixado de cada oportunidade
#-------- Bibliotecas utilizadas
import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os
import utilidadesppf 
from utilidadesppf import clean

path = os.getcwd()
keywords = 'brazil'
# Problema na certificação do site
#def belmontforum1(path, keywords = 'brazil'):
#    try:
page = requests.get('https://www.belmontforum.org/cras/') # Request para extrair a página html
soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html

# coletando as ids # e os nomes para cada oportunidade
# criando a lista vazia das ids e dos nomes
glinks=[]

table = soup.find("table") # Procurando a tabela que contém as oportunidades

for i in table.find_all('a', href=True): # Para cada oportunidade, capturar o link
    glinks.append('https://www.belmontforum.org/cras/' + i['href']) #salvando os links

# Retirando as duplicatas
glinks = list(dict.fromkeys(glinks))
print(glinks)
#glinks.remove('https://www.belmontforum.org/cras/https://belmontforum.org/archives/news/pre-announcement-human-migration-mobility-rapid-global-change')

#print(glinks)


# Criando o DF com a primeira tabela extraída
df = pd.read_html(str(table))[0]

# criando a lista vazia do Brasil e das infos
brazil=[]
infos=[]
cod=[]
dia = datetime.today().strftime('%y%m%d')
# looping para extrair de cada link
for i in glinks:
    page = requests.get(i, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).content.decode('utf-8')
    page_soup = BeautifulSoup(page, 'lxml')
    ab = page_soup.find('div', class_='vc_tta-panel-body').text
    infos.append(clean(ab)) # adicionar às infos
    #print(infos)
    if(findall(keywords, ab.lower())):
        brazil.append('Y')
    else:
        brazil.append('N')
        #print(brazil)


df= df.rename(columns={'CRA Title': 'opo_titulo'})
df['link']=pd.Series(glinks)
df['opo_brazil']=pd.Series(brazil)
df['opo_texto']=pd.Series(infos)
df['codigo']=pd.Series(cod)
df['atualizacao']=(dia)*len(glinks)
df = df.drop(['CRA ID'], axis=1)
df = df.drop(['Year'], axis=1)
# exportando o data.frame
path = path+'''\\belmontforum_01.csv'''
df.to_csv(path,index=False,sep=",")
    
#    except:
#        print('Erro na função belmont1')


belmontforum1('.')
