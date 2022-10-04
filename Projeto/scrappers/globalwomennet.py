# AB#141

import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
from urllib.request import Request, urlopen
import os
import unicodedata
from itertools import compress
import shutil 
from utilidadesppf import clean, getCodList, getInfoBase, getNewInfo


def globalwomennet1(path,keywords = 'brazil'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py e as palavras-chaves
  try:
    #print('Início função das oportunidades globalwomennet')
    glinks=['https://www.globalwomennet.org/energising-women-call-for-applications/']
    page = requests.get(glinks[0]) # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    #---------------------------------------------------------------------------------------
    mydivs = soup.findAll("small", class_="meta-category") #definindo aonde queremos extrair
    soup2 = BeautifulSoup(str(mydivs),'html.parser') 
    #print(soup2)
    titulo=[]
    for lk in soup2.find(rel="category tag"):
      titulo.append(lk)
    #---------------------------------------------------------------------------------------
    # criando as listas vazias que se tornarão colunas do dataframe
    brazil=[]
    deadline = []
    cod=[]
    texto=[]
    texto_ele=[]
    tipo=[]
    
    dia = datetime.today().strftime('%y%m%d') #formatação do dia padronizado
    #---------------------------------------------------------------------------------------
    # looping para entrar em cada link e buscar as informações
    for i in range(0,len(glinks)): # len(glinks)
      #---------------------------------------------------------------------------------------
      cod.append('globalwomennet_'+dia+'_01_'+str("{0:0=3d}".format(i))) #formato de código padronizado
      r = requests.get(glinks[i])
      soup = BeautifulSoup(r.content, 'html.parser') #soup de cada oportunidade

      # TEXT OPADRAO
      tag_texto_u = soup.find('div',class_="article-content") 
      tag_texto = tag_texto_u.text
      tag_texto = unicodedata.normalize("NFKD", tag_texto)
      tag_texto = re.sub("\n+", ' ', tag_texto)
      texto.append(tag_texto)     
      # DEADLINE
      tag_deadline = tag_texto_u.find('p', text = re.compile('deadline')) 
      tag_deadline = (tag_deadline.text)
      deadline.append(tag_deadline)

     # TEXTO ELEGIVEL
      tag_texto_ele = tag_texto_u.find('ul')
      tag_texto_ele = (tag_texto_ele.find_next_sibling("ul").text)
      tag_texto_ele = unicodedata.normalize("NFKD", tag_texto_ele)
      tag_texto_ele = re.sub("\n", ' ', tag_texto_ele)
      texto_ele.append(tag_texto_ele)



      # TIPO
      if ('grant' in tag_texto):         #busca a palavra 'grant' no título
        tipo.append('grant')                #salva a palavra 'grant' no tipo de oportunidade
      elif ('fellowship'in tag_texto):  #busca a palavra 'fellowship' no título
        tipo.append('fellowship')           #salva a palavra 'fellowship' no tipo de oportunidade
      elif ('scholarship' in tag_texto): #busca a palavra 'scholarship' no título
        tipo.append('scholarship')          #salva a palavra 'scholarship'' no tipo de oportunidade   
      elif ('award' in tag_texto): #busca a palavra 'scholarship' no título
        tipo.append('award')         #salva a palavra 'scholarship'' no tipo de oportunidade               
      else:
        tipo.append('other') # caso não encontre o tipo, retorna 'other


      # elegibilidade
      point = tag_texto_ele.lower() #deixando tudo minuscula
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
    path = path+'''\\globalwomennet_01.csv''' #padrão de saída do arquivo: nomedosite_numeral.csv
    df.to_csv(path,index=False,sep=",") # salvando o csv
    return()
    #print('Fim função das oportunidades globalwomennet')
  except Exception as e:
    print(e) 
    print("Erro na função globalwomennet1")


#globalwomennet1('.')

def globalwomennet2(path):
    try:
        pathbase = path.rsplit('\\', 1)[0]+'\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\globalwomennet_02.csv'
        titulos = []
        textos = []
        links = []
        page = requests.get('https://www.globalwomennet.org/news/blog/')
        soup = BeautifulSoup(page.text, 'lxml')
        sites = soup.find_all('a', class_="vc_general vc_btn3 vc_btn3-size-md vc_btn3-shape-rounded vc_btn3-style-flat vc_btn3-color-warning")
        soup2 = BeautifulSoup(str(sites), 'lxml')
        links_base = getInfoBase(pathbase, filename, 'link')
        
        for link in soup2.findAll('a'):
            info = (link['href'])
            links.append(info)
        
        new_links = getNewInfo(links_base, links)
        
        if(new_links):
          for link in new_links:
              page = requests.get(link).text
              soup = BeautifulSoup(page, 'lxml')
              titulo = soup.find('h1', class_ = "page-title").get_text()
              titulo = re.sub(r'#','',titulo)
              texto = BeautifulSoup(str(soup.find('div', class_ = "article-content")), 'lxml').get_text()
              titulos.append(titulo)
              textos.append(clean(texto))
        else:
          #print('Não há alteração em novas notícias')
          shutil.copy(pathbase+filename, '.\\'+dia)
        
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = new_links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'globalwomennet_')
        df.to_csv(path + filename, index = False)
        
    except Exception as e:
        print(e)
        print('Erro em globalwomennet2')

#globalwomennet2(os.getcwd())

def globalwomennet3(path):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\globalwomennet_03.csv'
        titulos = []
        textos = []
        links = ['https://www.globalwomennet.org/about-gwnet/#link_tab-about']
        #page = Request('https://www.globalwomennet.org/about-gwnet/#link_tab-about', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = requests.get('https://www.globalwomennet.org/about-gwnet/#link_tab-about').content.decode('UTF-8')
        soup = BeautifulSoup(page_request, 'lxml')
        titulo = soup.find('h1', class_ = "page-title").get_text()
        texto = clean(BeautifulSoup(str(soup.find('div', class_ = "tab-content")), 'lxml').get_text())
        titulos.append(titulo)
        textos.append(texto)
        
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['globalwomennet']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'globalwomennet_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
    except Exception as e:
        print(e)
        print('Erro em globalwomennet3')
        
#globalwomennet3(os.getcwd())

