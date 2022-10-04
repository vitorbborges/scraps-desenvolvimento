# AB#4
#-------- Bibliotecas utilizadas
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


def funbio4(path): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
    try:
        filename = '\\funbio_04.csv' 
        glinks=[] #lista de links vazia para ser preenchida
        urls=['https://www.funbio.org.br/en/programs-and-projects/page/1/?t=1','https://www.funbio.org.br/en/programs-and-projects/page/2/?t=1','https://www.funbio.org.br/en/programs-and-projects/page/3/?t=1']
        for i in range(0,len(urls)):
            page = requests.get(urls[i]) # Request para extrair a página html
            soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html
            mydivs = soup.findAll('div',class_="col-md-4 col-sm-6 col-12 ui-card subprojeto") #definindo aonde queremos extrair
            soup2 = BeautifulSoup(str(mydivs),'html.parser') # Extraindo o html só das partes dos links que interessam.
            for lk in soup2.find_all('a'):
                glinks.append((lk.get('href'))) #preenchendo cada link 'href'
       

        brazil=[]
        cod=[]
        titulo=[]
        atualizacao=[]
        dia = datetime.today().strftime('%y%m%d')
        for i in range(0,len(glinks)):   
            cod.append('funbio_'+dia+'_04_'+str("{0:0=3d}".format(i)))
            r = requests.get(glinks[i])
            soup = BeautifulSoup(r.content, 'lxml')
            tit = soup.find('h2').text
            tit = re.sub("\n","",tit)
            titulo.append(tit)
            atualizacao.append(dia)
            for points in soup.find_all('div', class_="row page-content"):
                point = str(points.text)
                point = point.lower()
                a = findall('(brasil|brazil)', point) #PROBLEMA: alguns projetos só falam de estados ou regioes, e nao tem a palavra 'brasil'
                if len(a) != 0:
                    brazil.append("Y")

                else:
                    brazil.append("N")

        df = pd.DataFrame({'prj_titulo':titulo,'link':glinks,'prj_brazil':brazil,'codigo':cod,'atualizacao':atualizacao})
        df.to_csv(path + filename, index=False,sep=",")  

    except:
        print("Erro na função funbio4")



