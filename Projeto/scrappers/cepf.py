# AB#29

import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os
from itertools import compress

def cepf1(path, keywords = "(brazil|latin america region)"): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py e as palavras-chaves
  try:
    page = requests.get('https://www.cepf.net/grants/open-calls-for-proposals') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    #---------------------------------------------------------------------------------------
    # mydivs = soup.findAll("div", {"role": "main","class": "mobile-full-width"}) #definindo aonde queremos extrair
    glinks=[] #lista de links vazia para ser preenchida
    for lk in soup.find_all('a'):
      glinks.append('https://cepf.org' + (lk.get('href'))) #preenchendo cada link 'href'

    # Tratamento do glinks:
    boleano = [('open-calls-for-proposals'in i) for i in glinks]
    glinks = list(compress(glinks, boleano))
    glinks = [re.sub('^https://cepf.org',"",i) for i in glinks] #  ^//grants//open-calls-for-proposals$
    glinks = [re.sub('^/grants/open-calls-for-proposals$',"",i) for i in glinks]
    glinks = list(filter(None, glinks)) # Apenas as oportunidades abertas
    #---------------------------------------------------------------------------------------
    # criando as listas vazias que se tornarão colunas do dataframe
    brazil=[]
    deadline = []
    cod=[]
    texto=[]
    tipo=[]
    titulo=[]
    dia = datetime.today().strftime('%y%m%d') #formatação do dia padronizado
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    # looping para entrar em cada link e buscar as informações
    for i in range(0,len(glinks)):
      #---------------------------------------------------------------------------------------
      cod.append('cepf_'+dia+'_01_'+str("{0:0=3d}".format(i))) #formato de código padronizado
      r = requests.get(glinks[i])
      soup = BeautifulSoup(r.content, 'lxml') #soup de cada oportunidade
      #titulo
      titulo.append(soup.find("h1").text)
  
      # texto
      txt = soup.find('div', class_="content").text #procurando o breve texto
      txt = re.sub("(\n+)"," ",txt) #excluindo o 'pular linha' extra
      texto.append(txt) # salvando na lista texto

      # tipo
      gtit = texto[i].lower() # Deixar tudo minúscula
      if ('grant' in gtit):         #busca a palavra 'grant' no título
        tipo.append('grant')                #salva a palavra 'grant' no tipo de oportunidade
      elif ('fellowship'in gtit):  #busca a palavra 'fellowship' no título
        tipo.append('fellowship')           #salva a palavra 'fellowship' no tipo de oportunidade
      elif ('scholarship' in gtit): #busca a palavra 'scholarship' no título
        tipo.append('scholarship')          #salva a palavra 'scholarship'' no tipo de oportunidade           
      else:
        tipo.append('other') # caso não encontre o tipo, retorna 'other

      #deadline
      tag_close_date = soup.find('strong', text = re.compile('Closing'))
      deadline.append(tag_close_date.next_sibling)

      # elegibilidade
      point = txt.lower() #deixando tudo minuscula
      a = findall(keywords, point) #procurando as keywords definidas
      if len(a) != 0: #Se encontrar alguma keyword salva Y, caso contrário salva N
        brazil.append("Y")
      else:
        brazil.append("N")
      #-------------------------------------------------------------------------------------------------

    # Criação do dataframe com as listas feitas
    df = pd.DataFrame({'opo_titulo':titulo,'link':glinks,'opo_brazil':brazil,
    'opo_deadline':deadline,'codigo':cod,'opo_texto':texto,'opo_texto_ele':texto,'opo_tipo':tipo}) 
    df['atualizacao']=[dia]*len(glinks) #criando a variável atualizacao (dia que foi extraido do tamanho dos links)

    # Definindo o path que o arquivo será salvo
    path = path+'''\\cepf_01.csv''' #padrão de saída do arquivo: nomedosite_numeral.csv
    df.to_csv(path,index=False,sep=",") # salvando o csv
    return()
    print('Fim função das oportunidades  cepf')
  except Exception as e:
    print(e) 
    print("Erro na função cepf1")


# cepf1('.','brazil')