# AB#17
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from datetime import datetime
import requests
from currency_converter import CurrencyConverter 
from utilidadesppf import truncate, getCodList, clean




def biocodexmicrobiotafundation3(path):
    try:
        instituicoes = []
        titulos = []
        textos = []
        links = ['https://www.biocodexmicrobiotafoundation.com/foundation', 'https://www.biocodexmicrobiotafoundation.com/international-research-grant']
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\biocodexmicrobiotafundation_03.csv'
        for link in links:
            page = requests.get(link).content.decode('utf-8')
            soup = BeautifulSoup(page, 'lxml')
            titulo = clean(soup.find('h2', class_='Section-title').text)
            titulos.append(titulo)
            if(soup.find('div', class_='col-xs-12 col-sm-12') is not None):
                texto = clean(soup.find('div', class_='col-xs-12 col-sm-12').get_text())
            else:
                texto = clean(soup.find('div', class_='col-xs-12 col-md-10 col-md-offset-1 col-lg-8 col-lg-offset-2').get_text())
            textos.append(texto)
            
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['biocodexmicrobiotafundation']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'biocodexmicrobiotafundation_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em biocodexmicrobiotafundation3')



def biocodexmicrobiotafundation4(path, keywords = '(brazil|latin america region|no geographic limitations)'):
    try:
        dia = datetime.today().strftime('%y%m%d')
        filename = '\\biocodexmicrobiotafundation_04.csv'
        titulos = []
        values = []
        hasBrazil = []
        texts = []
        page = requests.get('https://www.biocodexmicrobiotafoundation.com/international-call-projects-2021').content.decode('utf-8')
        soup = BeautifulSoup(page, 'lxml')
        titulo = soup.find('h2', class_ = 'Section-title').text
        titulos.append(titulo.strip().replace('"', ''))
        text = ''
        text_area = soup.find('div', class_= 'Tabs-wrap is-open')
        for children in text_area.findChildren():
            text += children.text
            text += '\n'
        text = re.sub('Click here to find out more about the information notice.', '', text)
        texts.append(text)
        if(findall(keywords, text.lower())):
            hasBrazil.append('Y')
        else:
            hasBrazil.append('N')
        value_euro = text.split('€')[1].split(' ')[0].replace(',', '')
        value_euro = float(value_euro)
        converter = CurrencyConverter()
        value_euro = converter.convert(value_euro, 'EUR', 'USD')
        value_usd = truncate(value_euro, 2)
        values.append(value_usd)

        df = pd.DataFrame()
        df['prj_titulo'] = titulos 
        df['link'] = ['https://www.biocodexmicrobiotafoundation.com/international-call-projects-2021']
        df['prj_instituicao'] = ['Biocodexmicrobiotafundation']
        df['prj_valor'] = values
        df['prj_brazil'] = hasBrazil
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_4_', 'biocodexmicrobiotafundation_')
        df.to_csv(path+filename, index=False)
    except Exception as e:
        print(e)
        print('Erro em biocodexmicrobiotafundation4')