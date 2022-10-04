import bs4
import requests
from bs4 import BeautifulSoup
import re
import io
from re import findall
import pandas as pd
from datetime import datetime
import os
from time import sleep
import os.path
from utilidadesppf import clean

# noticias
def thegef2(path): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
  try:
    #print('[thegef][noticias][start]')
    page = requests.get('https://www.thegef.org/news/news-stories') # Request para extrair a página html 
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página (somente uma página, pois noticia nova vai estar sempre nessa página)
    section = soup.find('section', class_='col')

    h3 = section.find_all('h3')
    soup = BeautifulSoup(str(h3),'html.parser')

    nlink=[]
    for a in soup.find_all('a', href=True):
        if len(a['href'])>=20: # número arbitrário, só pra identificar algum links
            nlink.append('https://www.thegef.org'+a['href']) 

    titulo=[]
    info=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')

    for i in range(0,4): # Pegar apenas as 4 primeiras notícias, pois o site bloqueia mais leituras urllib3.exceptions.MaxRetryError
        cod.append('thegef_'+dia+'_02_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
        page = requests.get(nlink[i]) 
        soup = BeautifulSoup(page.text,'html.parser') # parser que lê o HTML
        b = soup.find('h1',class_="title").text # procura o título que está na tag <h1>
        # b = re.sub("(\n|\r)","",b)
        titulo.append(b) 
        content = soup.find_all('div',class_="inner")
        soup = BeautifulSoup(str(content),'html.parser')    
        info.append(soup.get_text())
        sleep(0.25)

    nlink = (nlink[0:4])
    df = pd.DataFrame({'not_titulo':titulo,'link':nlink,'not_texto':info}) #criando o dataframe
    df['codigo']=cod
    df['atualizacao']=[dia]*len(nlink)



    path = path+'''//thegef_02.csv'''
    df.to_csv(path,index=False,sep=",")    
    
    #print('[thegef][noticias][end]')
    return(df)

  except:
      print("Erro na função thegef2")
      

# Politicas
def thegef3(path):
  try:
    #print('[thegef][politicas][start]')
    def soups(paginas):
      page = requests.get(paginas) # Request para extrair a página html
      soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
      a = soup.find('article')
      # section = BeautifulSoup(a,'html.parser')
      _, b  = os.path.split(paginas)
      # b = soup.find('div',class_='content')
      return(b, a.text)

    pags=['https://www.thegef.org/about-us','https://www.thegef.org/about/funding','https://www.thegef.org/topics/biodiversity',
    'https://www.thegef.org/topics/chemicals-and-waste','https://www.thegef.org/topics/climate-change','https://www.thegef.org/topics/forests',
    'https://www.thegef.org/topics/international-waters','https://www.thegef.org/topics/land-degradation','https://www.thegef.org/topics/amazon',
    'https://www.thegef.org/topics/commodities','https://www.thegef.org/topics/fisheries','https://www.thegef.org/topics/food-security',
    'https://www.thegef.org/topics/sustainable-cities']
    texto=[]
    nomes=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')

    for i in range(0,len(pags)):
      # print(pags[i])
      elementos = soups(pags[i])
      nomes.append(str(elementos[0]))
      texto.append(clean(str(elementos[1])))
      cod.append('thegef_'+dia+'_03_'+str("{0:0=3d}".format(i)))

    instituto = ['The Gef']*len(pags)
    atualizacao = [dia]*len(pags)
    nomes = [re.sub(r'''(b'|\'|\\n)''', "", i) for i in nomes]
    texto = [re.sub(r'''(b'|b"|\'|\\n)''', '', i) for i in texto]

    df = pd.DataFrame({'pol_titulo':nomes,'link':pags,'pol_texto':texto,'codigo':cod,'atualizacao':atualizacao,'pol_instituicao':instituto})

    # print(df)
    path = path+'''//thegef_03.csv'''
    df.to_csv(path,index=False,sep=",")  
    #print('[thegef][politicas][end]')
    return(df)

  except:
    print("Erro na função thegef3")


# OPORTUNIDADES
# def thegef4(path): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
#     try:
#         print('Início função das oportunidades The gef')

#         url="https://www.thegef.org/sites/default/files/projects/gef-projects.csv"
#         s=requests.get(url).content #extração do site
#         df=pd.read_csv(io.StringIO(s.decode('utf-8'))) #leitura e transformação em csv

#         # Filtrando 
#         filtro = df["Countries"].str.contains("Brazil|Global",na=False)
#         df = df.loc[filtro]

#         df = df.rename(columns={'Title': 'prj_titulo', 'Grant and Cofinancing': 'prj_valor', 'Implementing #Agencies': 'prj_instituicao'})
#         df = df.drop(['ID', 'Focal Areas','Countries','Fund Source','Period','Status'], axis=1)

#         lk = df['prj_titulo'].str.lower()    
#         lk = [re.sub("(\(|\))","",a) for a in lk]
#         lk = [re.sub("[0-9]","  ",a) for a in lk]
#         lk = [re.sub(' +', ' ', a) for a in lk]
#         lk = [re.sub(" ","-",a) for a in lk]
#         df['link'] = ([('https://www.thegef.org/projects'+a) for a in lk])
#         df['brazil']=['Y']*len(df['link'])
#         dia = datetime.today().strftime('%y%m%d')
#         df['atualizacao']=[dia]*len(df['link'])
#         cod=[]
#         for i in range(0,len(df['link'])):
#             cod.append('thegef_'+dia+'_04_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: #nomedosite_data_nºgrupoextracao_indexador
#         df['codigo']=cod
#         path = path+'''\\thegef_04.csv'''
#         df.to_csv(path,index=False,sep=",")  
#         print('Fim função das oportunidades The gef')
#     except:
#         print("Erro na função The gef4")