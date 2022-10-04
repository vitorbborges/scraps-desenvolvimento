import bs4
import requests
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import os
from utilidadesppf import clean

# OPORTUNIDADES
def royal1(path, keywords='brazil'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
  try:
    #print('[royal][oportunidades][start]')
    page = requests.get('https://royalsociety.org/grants-schemes-awards/grants/grants-schedule/') # Request para extrair a página html

    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    table = soup.find( "table") # Coletando a tabela disponibilizada na página
    table_str = str(table) #converter para string

    df  = pd.read_html(table_str)[0] # Criando o dataframe a partir da tabela em HTML
    df = df.drop(['Open date', 'Decision'], axis=1)

    glinks=[] # lista vazia
    for a in table.find_all('a', href=True):
        if 'https:' in a['href']:    
          glinks.append(a['href']) # encontrar o link de cada oportunidade e salvar
        else:
          glinks.append('https://royalsociety.org' + a['href']) # encontrar o link de cada oportunidade e salvar


    df['link'] = glinks #criando a coluna Links no Dataframe
    brazil=[] # lista vazia
    Datainfo=[] # lista vazia
    cod=[]
    tipo=[]
    texto_ele=[]
    dia = datetime.today().strftime('%y%m%d')

    for i in range(0,len(glinks)):
        gtit = df['Scheme'][i].lower()
        if len(findall('grant', gtit)):
            tipo.append('grant')
        elif len(findall('fellowship', gtit)):
            tipo.append('fellowship')
        elif len(findall('scholarship', gtit)):
            tipo.append('scholarship')                
        else:
            tipo.append('other')

        cod.append('royal_'+dia+'_01_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
        r = requests.get(glinks[i]) # Extraindo a página de cada oportunidade
        soup = BeautifulSoup(r.content, 'lxml')  #Lendo a página de cada oportunidade
        agregado=[]
        for points in soup.find_all('div',class_="rteContent"): # Pegando o texto html da página
            point = str(points.text)  # Transformando o html para texto
            point = re.sub("(\n)","",point)
            agregado.append(point)
        Datainfo.append(' '.join(agregado)) #Incluindo o texto no datainfo

        # TEXO ELEGIIBLIDADE:
        html = u""
        for tag in soup.find("h3", text = re.compile('Am I eligible to apply?')).next_siblings:
            if tag.name == "h3":
                break
            else:
                html += str(tag)

        textinho = clean(BeautifulSoup(html,'html.parser').text)
        if 'a' in textinho: # verificando se contem um caractere comum (letra a) para determinar as células vazias
            texto_ele.append(textinho)
        else:
            texto_ele.append(' '.join(agregado))

        # PESQUISANDO AS KEYWORDS
        point = point.lower() #transformando em minúscula
        a = findall(keywords, point) # Procurando se contém brazil no texto
        if len(a) != 0: # Se o vetor não for vazio contém, se for vazio não contém
            brazil.append("Y") 
            # print('contém BR')
        else:
            brazil.append("N")
            # print('não contém BR')
        
    # Incluindo as colunas no DF
    df['opo_brazil'] = brazil 
    df['opo_texto'] = Datainfo
    df['opo_texto_ele'] = texto_ele
    df['opo_tipo'] = tipo
    df['codigo']=cod
    df['atualizacao']=[dia]*len(glinks)
    df = df.rename(columns={'Scheme': 'opo_titulo', 'Close date': 'opo_deadline'})
    
    # arquivo de saída e nome do arquivo
    path = path+'''//royalsociety_01.csv'''
    # print(path)
    df.to_csv(path,index=False,sep=",")

    #print('[royal][oportunidades][end]')
    #return(df)

  except Exception as e:
    print(e) 
    print("Erro na função royal1")


# NEWS
def royal2(path): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
  try:
    #print('[royal][noticias][start]')
    page = requests.get('https://royalsociety.org/search/?collection=website-meta&query=&clive=news') # Request para extrair a página html
    soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
    a = soup.find_all('h4')
    soup = BeautifulSoup(str(a),'html.parser')


    nlink=[]

    for a in soup.find_all('a', href=True):
        if len(a['href'])>=20: # número arbitrário, só pra identificar algum links
            nlink.append(a['href']) 

    titulo=[]
    info=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')

    for i in range(0,len(nlink)):
        cod.append('royal_'+dia+'_02_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
        page = requests.get(nlink[i]) 
        soup = BeautifulSoup(page.text,'html.parser') # parser que lê o HTML
        b = soup.find('h1').text # procura o título que está na tag <h1>
        b = re.sub("(\n|\r)","",b)
        titulo.append(b) 
        c = clean(soup.find('div',class_="twoThirdWidth bottomGap left").text)
        info.append(c)

    df = pd.DataFrame({'not_titulo':titulo,'link':nlink,'not_texto':info}) #criando o dataframe
    df['codigo']=cod
    df['atualizacao']=[dia]*len(nlink)

    path = path+'''//royalsociety_02.csv'''
    # print(path)

    df.to_csv(path,index=False,sep=",")    
    #print('[royal][oportunidades][end]')  
    #return(df)


  except Exception as e:
    print(e) 
    print("Erro na função royal2")
    
    

# POLITICAS
def royal3(path):
  try:
    #print('[royal][politicas][start]')

    def soups(paginas):
      page = requests.get(paginas) # Request para extrair a página html
      soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
      a = soup.find('h1')
      b = soup.find('section')
      return(a.text, b.text)

    pags=['https://royalsociety.org/about-us/mission-priorities/','https://royalsociety.org/about-us/programmes/','https://royalsociety.org/about-us/funding-finances/']
    nomes=[]
    texto=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')

    for i in range(0,len(pags)):
      elementos = soups(pags[i])
      nomes.append(str(elementos[0]))
      texto.append(clean(str(elementos[1])))
      cod.append('royal_'+dia+'_03_'+str("{0:0=3d}".format(i)))

    instituto = ['Royal Society']*len(pags)
    atualizacao = [dia]*len(pags)
    nomes = [re.sub(r'''(b'|\\r|\\n)''', "", i) for i in nomes]
    texto = [re.sub(r'''(b'|\\r|\\n)''', '', i) for i in texto]

    df = pd.DataFrame({'pol_titulo':nomes,'link':pags,'pol_texto':texto,'codigo':cod,'atualizacao':atualizacao,'pol_instituicao':instituto}) 


    path = path+'''//royalsociety_03.csv'''
    df.to_csv(path,index=False,sep=",")  

    #print('[royal][politicas][end]')

  except Exception as e:
      print(e) 
      print("Erro na função royal3")