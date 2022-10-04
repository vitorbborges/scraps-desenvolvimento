# AB#24
# Definição da função: nomedosite_nº
# 1) Oportunidades, 2) Notícias, 3) Políticas
#-------- Bibliotecas utilizadas
import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os
from utilidadesppf import *

# Aderente à oportunidade abertas 01

def wellcome1(path,keywords='brazil'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py e as palavras-chaves
  try:
    page = requests.get('https://wellcome.org/grant-funding/schemes') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    #---------------------------------------------------------------------------------------
    mydivs = soup.find_all('a', class_='c-text-card__link')
    titulo = [i.text for i in mydivs]
    glinks = []
    for lk in mydivs:
      glinks.append('https://wellcome.org' + (lk.get('href'))) #preenchendo cada link 'href'
      
    #---------------------------------------------------------------------------------------
    # criando as listas vazias que se tornarão colunas do dataframe
    brazil=[]
    cod=[]
    texto=[]
    tipo=[]
    deadlines = []
    dia = datetime.today().strftime('%y%m%d') #formatação do dia padronizado
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    # looping para entrar em cada link e buscar as informações
    for i in range(0,len(glinks)):
          #---------------------------------------------------------------------------------------
          # O titulo já foram extraídos e  tem o mesmo tamanho dos links
        gtit = titulo[i].lower() # Deixar tudo minúscula
        if len(findall('grant', gtit)):         #busca a palavra 'grant' no título
            tipo.append('grant')                #salva a palavra 'grant' no tipo de oportunidade
        elif len(findall('fellowship', gtit)):  #busca a palavra 'fellowship' no título
            tipo.append('fellowship')           #salva a palavra 'fellowship' no tipo de oportunidade
        elif len(findall('scholarship', gtit)): #busca a palavra 'scholarship' no título
            tipo.append('scholarship')          #salva a palavra 'scholarship'' no tipo de oportunidade           
        else:
            tipo.append('other')                # caso não encontre o tipo, retorna 'other'
        
          #---------------------------------------------------------------------------------------
        cod.append('wellcome_'+dia+'_01_'+str("{0:0=3d}".format(i))) #formato de código padronizado, ex de saida: wellcome_210224_01_001
        r = requests.get(glinks[i])
        soup = BeautifulSoup(r.content, 'lxml') #novo soup para cada oportunidade específica
          #---------------------------------------------------------------------------------------
        txt = soup.find('div', class_="cc-rich-text").text
        txt = re.sub("(\n+)","",txt)
        texto.append(txt)
        
        dates = []
        for j in soup.find_all('p', class_='cc-timeline__status'):
            dates.append(j.next_sibling.find('div', class_ = 'cc-timeline__item-date').text)
        dates = [datetime.strptime(j.split(',')[0], '%d %B %Y') for j in dates]
        cloz_dict = {
                date.timestamp() - datetime.today().timestamp() : date
                for date in dates 
                }
        try:
            deadlines.append(cloz_dict[min([k for k in cloz_dict.keys() if k > 0])].strftime('%d %m %y'))
        except:
            deadlines.append('Deadline não encontrada.')
        
        point = ''
        for points in soup.find_all('dd'): # para buscar aonde vai estar o texto da pagina na tag dd
            point += str(points.text) #transformando em texto e em string
        point = point.lower() #deixando tudo minuscula
        a = findall(keywords, point) #procurando as keywords definidas
        if len(a) != 0: #Se encontrar alguma keyword salva Y, caso contrário salva N
            brazil.append("Y")
        else:
            brazil.append("N")
      
    df = pd.DataFrame({'opo_titulo':titulo,'link':glinks,'opo_brazil':brazil,
    'opo_deadline':deadlines,'codigo':cod,'opo_texto':texto,'opo_tipo':tipo}) 
    df['atualizacao']=[dia]*len(glinks)
    # Definindo o path que o arquivo será salvo
    path = path+'''\\wellcome_01.csv''' #padrão de saída do arquivo: nomedosite_numeral.csv
    df.to_csv(path,index=False,sep=",") # salvando o csv
    
  except Exception as e:
    print(e) 
    print("Erro na função wellcome2")

#wellcome1(os.getcwd())


def wellcome2(path):
  try:
    #print('Início função das noticias  wellcome')
    page = requests.get('https://wellcome.org/news/all?&field_article_type[news]=news') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
    texto=[]
    
    a = soup.find_all('h3')
    soup = BeautifulSoup(str(a),'html.parser')
    nlink=[]
    for a in soup.find_all('a', href=True):
      if len(a['href'])>=20: # número arbitrário, só pra identificar algum links
        nlink.append('https://wellcome.org'+a['href'])
        # print('https://wellcome.org'+a['href'])
    titulo=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(nlink)):
      cod.append('wellcome_'+dia+'_02_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
      page = requests.get(nlink[i]) 
      soup = BeautifulSoup(page.text,'html.parser') # parser que lê o HTML
      b = soup.find('h1').text # procura o título que está na tag <h1>
      titulo.append(b) 
      
      txt = ''
      for i in soup.find_all('div', class_ = 'cc-rich-text'):
         txt += i.text
         
      texto.append(clean(txt))
    
    df = pd.DataFrame({'not_titulo':titulo,'link':nlink,'not_texto':texto,'codigo':cod}) #criando o dataframe
    df['atualizacao']=[dia]*len(nlink)
    path = path+'''\\wellcome_02.csv'''
    df.to_csv(path,index=False,sep=",") 
    #print('Fim função das notícias wellcome')
  except Exception as e:
    print(e) 
    print("Erro na função wellcome2")
    
#wellcome2(os.getcwd())

def wellcome3(path):
  try:
    #print('Início função de política  wellcome')
    def soups(paginas):
      page = requests.get(paginas) # Request para extrair a página html
      soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
      a = soup.find('h1',class_="c-page-title")
      b = soup.find('main')
      return(a.text,b.text)
    pags=['https://wellcome.org/who-we-are','https://wellcome.org/grant-funding','https://wellcome.org/how-we-work','https://wellcome.org/about-us/strategy']
    nomes=[]
    texto=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(pags)):
      elementos = soups(pags[i])
      nomes.append(clean(str(elementos[0])))
      texto.append(clean(str(elementos[1])))
      cod.append('wellcome_'+dia+'_03_'+str("{0:0=3d}".format(i)))
    instituto = ['Wellcome']*len(pags)
    atualizacao = [dia]*len(pags)

    df = pd.DataFrame({'pol_titulo':nomes,'link':pags,'pol_texto':texto,'codigo':cod,'atualizacao':atualizacao,'pol_instituicao':instituto}) 
    path = path+'''\\wellcome_03.csv'''
    df.to_csv(path,index=False,sep=",")  
    #print('Fim função de política wellcome')
    #return(df)
  except Exception as e:
    print(e) 
    print("Erro na função wellcome3")



#wellcome3(os.getcwd())

