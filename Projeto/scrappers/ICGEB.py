# AB#20
# -------------------------- Atualização em 06/01/2020
# Comentário da PO:
# ICGEB - o que foi capturado esta aderente com OPORTUNIDADES ABERTAS, mas nao é suficiente.
# Falta deadline e falta alguma informacao que ajude a alimentar o campo de Subtitulo.

# REUNIÃO:
# Esse site também possui uma página de grants para ser verificada, o que foi extraído foi de fellowships 
# Parte das posições em /category/news

#-------- Bibliotecas utilizadas
import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os

def icgeb1(path,keywords = 'brazil'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
  try:
    page = requests.get('https://www.icgeb.org/fellowships/')
    soup = BeautifulSoup(page.text,'html.parser')
    dia = datetime.today().strftime('%y%m%d')
    soupheader = soup.find_all('header')
    
    links = []
    nomes=[]
    brazil=[]
    deadlines=[]
    infos=[]
    eligibilities=[]
    cod=[]
    tipo=[]
    #------------------------------------------------------------------------------------------
    # Encontra o título de todas as fellowships, deadlines e procurar se tem 'brazil' em cada uma:
    #------------------------------------------------------------------------------------------
    for i in range(1,len(soupheader)):
      cod.append('ICGEB_'+dia+'_01_'+str("{0:0=3d}".format(i)))
      link = soupheader[i].find('a')['href']
      links.append(link)
      title = soupheader[i].find('a').text
      nomes.append(title)
      tipo.append('fellowship')
    
      deadline = soupheader[i].next_sibling.find_all('p')[0].text[32:]
      if len(deadline)<=2:
        deadlines.append('NA')
      else:
        deadlines.append(deadline)
    
      info = soupheader[i].next_sibling.find_all('p')[1].text
      infos.append(info)
    
      eligibility = ''
      for i in BeautifulSoup(requests.get(link).text,'html.parser').find('h4', id="eligibility").next_siblings:
         if str(i)[:3] == '<p>':
            eligibility += i.text
         else:
            break
      eligibilities.append(eligibility)
    
      a = findall(keywords, eligibility.lower())
      if len(a) != 0:
        brazil.append("Y")
      else:
        brazil.append("N")
    
    df = pd.DataFrame({'opo_titulo':nomes,'link':links,'opo_brazil':brazil,'opo_texto':infos, 'opo_texto_ele':eligibilities,'opo_deadline':deadlines,'opo_tipo':tipo}) 
    df['atualizacao']=[dia]*len(links)
    df['codigo']=cod
    path = path+'''\\icgeb_01.csv'''
    df.to_csv(path,index=False,sep=",")

  except Exception as e:
   print(e) 
   print("Erro na função icegeb1")
   
#icgeb1(os.getcwd())

def icgeb2(path):
    
    try:
      #print('Início função das noticias  icgeb')
      page = requests.get('https://www.icgeb.org/category/news/') # Request para extrair a página html
      soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
      # texto=[]
      # for c in soup.find_all('p',class_='tile__description'):
      #   texto.append(c.text)

      a = soup.find_all('h3', class_="h2 entry-title")
      soup = BeautifulSoup(str(a),'html.parser')
      titulo=[]
      for c in soup.find_all('a',title=True):
          titulo.append(c.text)  
      # print(len(titulo))

      nlink=[]
      for a in soup.find_all('a', href=True):
          if len(a['href'])>=10: # número arbitrário, só pra identificar algum links
              nlink.append(a['href'])   
      # print(len(nlink))

      texto=[]
      cod=[]
      dia = datetime.today().strftime('%y%m%d')
      for i in range(0,len(nlink)):
          cod.append('icgeb_'+dia+'_02_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
          page = requests.get(nlink[i]) 
          soup = BeautifulSoup(page.text,'html.parser') # parser que lê o HTML
          b = soup.find('section',class_="entry-content cf").text # procura o título que está na tag <h1>
          texto.append(b) 
     # print(len(texto))

      df = pd.DataFrame({'not_titulo':titulo,'link':nlink,'not_texto':texto,'codigo':cod}) #criando o dataframe
      df['atualizacao']=[dia]*len(nlink)
      path = path+'''\\icgeb_02.csv'''
      df.to_csv(path,index=False,sep=",")  
      # print(df)
      #print('Fim função das notícias icgeb')


    except Exception as e:
        print(e) 
        print("Erro na função icgeb2")
        


def icgeb3(path):

  try:
    #print('Início função de política  ICGEB')
    def soups(paginas):
      page = requests.get(paginas) # Request para extrair a página html
      soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
      a = soup.find('h1',class_="page-title")
      b = soup.find('main')
      return(a.text,b.text)
    pags=['https://www.icgeb.org/about-us/what-we-do/','https://www.icgeb.org/about-us/who-we-are/']
    nomes=[]
    texto=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(pags)):
      elementos = soups(pags[i])
      nomes.append(elementos[0])
      texto.append(elementos[1])
      cod.append('icgeb_'+dia+'_03_'+str("{0:0=3d}".format(i)))
    instituto = ['icgeb']*len(pags)
    atualizacao = [dia]*len(pags)

    df = pd.DataFrame({'pol_titulo':nomes,'link':pags,'pol_texto':texto,'codigo':cod,'atualizacao':atualizacao,'pol_instituicao':instituto}) 
    path = path+'''\\icgeb_03.csv'''
    df.to_csv(path,index=False,sep=",")  
    #print('Fim função de política icgeb')
  except Exception as e:
   print(e) 
   print("Erro na função icgeb3")

#icgeb3(os.getcwd())



