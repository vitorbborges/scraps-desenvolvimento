#AB61
import bs4
from bs4 import BeautifulSoup
import re
import requests
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime
from utilidadesppf import clean

def moore1(path, keywords = '(latin american region|brazil)'):
    try:
        link = 'https://www.moore.org/article-detail?newsUrlName=upcoming-funding-opportunities-in-health-care'

        hasBrazil = []
        status =[]
        dia = datetime.today().strftime('%y%m%d')
        ano = datetime.today().strftime('%y')

        page = requests.get(link) # Request para extrair a página html
        soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
        #titulo
        titulo = [soup.find('h1').text]
        #deadline
        tag_close_date = soup.find('p', text = re.compile('Request'))
        deadline = [tag_close_date.next_sibling.text]
        #texto
        texto = clean(soup.find('div',class_='col-md-8 col-sm-12 user-content').text)
        texto = clean(re.sub("\n+"," ",texto))
        #tipo
        tipo=[]
        if len(findall('grant', texto.lower())):         
            tipo.append('grant')                
        elif len(findall('fellowship', texto.lower())):  
            tipo.append('fellowship')          
        elif len(findall('scholarship', texto.lower())): 
            tipo.append('scholarship')                   
        else:
            tipo.append('other')
        
        brazil=[]
        a = findall(keywords, texto) #procurando as keywords definidas
        if len(a) != 0: #Se encontrar alguma keyword salva Y, caso contrário salva N
            brazil.append("Y")
        else:
            brazil.append("N")

        codigo = ('moore_'+dia+'_01_'+str("{0:0=3d}".format(0)))
        atualizacao = [dia]

        df = pd.DataFrame({'opo_titulo':titulo,'link':link,'opo_brazil':brazil,
        'opo_deadline':deadline,'codigo':codigo,'opo_texto':texto,'opo_texto_ele':texto,'opo_tipo':tipo,'atualizacao':atualizacao}) 
        path = path+'''\\moore_01.csv''' #padrão de saída do arquivo: nomedosite_numeral.csv
        df.to_csv(path,index=False,sep=",") # salvando o csv

    except Exception as e:
        print(e)
        print('Erro em moore1')


# moore1('.')