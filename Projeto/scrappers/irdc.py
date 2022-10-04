# AB#82

import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os
import unicodedata
from itertools import compress
from utilidadesppf import clean

def irdc1(path, keywords = 'brazil'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py e as palavras-chaves
  try:
    page = requests.get('https://www.idrc.ca/en/funding') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    #---------------------------------------------------------------------------------------
    mydivs = soup.findAll("span", class_="field-content") #definindo aonde queremos extrair
    soup2 = BeautifulSoup(str(mydivs),'html.parser') 
    #print(soup2)
    glinks=[] #lista de links vazia para ser preenchida
    for lk in soup2.find_all('a'):
      glinks.append('https://www.idrc.ca' + (lk.get('href'))) #preenchendo cada link 'href'

    #---------------------------------------------------------------------------------------
    # criando as listas vazias que se tornarão colunas do dataframe
    brazil=[]
    deadline = []
    cod=[]
    texto=[]
    texto_ele=[]
    tipo=[]
    titulo=[]
    dia = datetime.today().strftime('%y%m%d') #formatação do dia padronizado
    #---------------------------------------------------------------------------------------
    # looping para entrar em cada link e buscar as informações
    for i in range(0,len(glinks)): # len(glinks)
      #---------------------------------------------------------------------------------------
      cod.append('irdc_'+dia+'_01_'+str("{0:0=3d}".format(i))) #formato de código padronizado
      r = requests.get(glinks[i])
      soup = BeautifulSoup(r.content, 'html.parser') #soup de cada oportunidade
      soup.prettify(formatter="minimal")
      
      # TIPO
      tag_tipo = soup.find('div', class_="field__label", text = re.compile('Type')) 
      tipo.append(clean(tag_tipo.find_next_sibling("div").text))
      # DEADLINE
      tag_deadline = soup.find('div', class_="field__label", text = re.compile('Deadline')) 
      deadline.append(clean(tag_deadline.find_next_sibling("div").text))

     # TEXTO ELEGIVEL
      try:
        tag_texto_ele = soup.find('div', class_="field field--name-field-award-eligibility field--type-text-long field--label-above") 
        tag_texto_ele = tag_texto_ele.text
        tag_texto_ele = unicodedata.normalize("NFKD", tag_texto_ele)
        tag_texto_ele = re.sub("\n", ' ', tag_texto_ele)
        textoelegivel = tag_texto_ele
        texto_ele.append(clean(tag_texto_ele))
        type(tag_texto_ele)
      except:
        texto_ele.append("")


     # TEXT OPADRAO
      tag_texto = soup.find('article') 
      tag_texto = tag_texto.text
      tag_texto = unicodedata.normalize("NFKD", tag_texto)
      tag_texto = re.sub("\n+", ' ', tag_texto)
      texto.append(clean(tag_texto))

      #titulo
      titulo.append(clean(soup.find("h1").text))

            # elegibilidade
      point = textoelegivel.lower() #deixando tudo minuscula
      a = findall(keywords, point) #procurando as keywords definidas
      if len(a) != 0: #Se encontrar alguma keyword salva Y, caso contrário salva N
         brazil.append("Y")
      else:
         brazil.append("N")


     #-------------------------------------------------------------------------------------------------

    # Criação do dataframe com as listas feitas
    df = pd.DataFrame({'opo_titulo':titulo,'link':glinks,'opo_brazil':brazil,
    'opo_deadline':deadline,'codigo':cod,'opo_texto':texto,'opo_texto_ele':texto_ele,'opo_tipo':tipo}) 
    df['atualizacao']=[dia]*len(glinks) #criando a variável atualizacao (dia que foi extraido do tamanho dos links)

    # Definindo o path que o arquivo será salvo
    path = path+'''\\irdc_01.csv''' #padrão de saída do arquivo: nomedosite_numeral.csv
    df.to_csv(path,index=False,sep=",") # salvando o csv
    return()
    print('Fim função das oportunidades irdc')
  except Exception as e:
    print(e) 
    print("Erro na função irdc1")


# irdc1('.','brazil')