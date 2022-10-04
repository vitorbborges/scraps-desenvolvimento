# AB#65
import bs4
from bs4 import BeautifulSoup
import re
from re import findall
import pandas as pd
from urllib.request import Request, urlopen
from datetime import datetime, date
import requests
from utilidadesppf import clean, getCodList
import shutil


def philanthropynewsdigest1(path, keywords = '(brazil|latin america region)'):
    try:
        #------------------------------------------
        titles = []
        links = []
        deadlines = []
        texts = []
        types = []
        hasBrazil = []
        dia = datetime.today().strftime('%y%m%d')
        #----------------------------------------------
        req = Request('https://philanthropynewsdigest.org/rfps', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(req).read()
        page_soup = BeautifulSoup(page_request, 'lxml')
        pre_soup = page_soup.find('section', class_ = 'listing listing-rfp') #section class="listing listing-rfp
        # opo_list = pre_soup.find('div', class_ = 'list-group')
        for raw_link in pre_soup.find_all('a'):
            link = raw_link['href']
            links.append('https://philanthropynewsdigest.org' +link)

        for i in links:

            req = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(req).read()
            soup = BeautifulSoup(page_request, 'lxml')

            title = soup.find('h1').text
            titles.append(title)
            dead = soup.find('div', class_="attribute-deadline_date").text
            dead = re.sub(r'(\n|\t)','',dead)
            deadlines.append(dead)

            text = clean(soup.find('div', class_="attribute-body ezoe", itemprop="text").text)
            texts.append(text)

            if len(findall('grant', text.lower())):         
                types.append('grant')                
            elif len(findall('fellowship', text.lower())):  
                types.append('fellowship')          
            elif len(findall('scholarship', text.lower())): 
                types.append('scholarship')   
            elif len(findall('award', text.lower())): 
                types.append('award')                  
            else:
                types.append('other')

            if(findall(keywords, text.lower())):
                hasBrazil.append('Y')
            else:
                hasBrazil.append('N')
            
        df = pd.DataFrame()
        df['opo_titulo'] = titles
        df['link'] = links
        df['opo_texto'] = texts
        df['opo_texto_ele'] = texts
        df['opo_deadline'] = deadlines
        df['opo_brazil'] = hasBrazil
        df['opo_tipo'] = types
        df['codigo'] = getCodList(dia, len(df.index), '_1_', 'roddenberry_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path + '\\philanthropynewsdigest_01.csv', index=False)
    except Exception as e:
        print(e)
        print('Erro em philanthropynewsdigest1')

# philanthropynewsdigest1('.')

def philanthropynewsdigest2(path):
    try:
        ###pathbase = path.rsplit('\\', 1)[0]+ '\\baseprincipal'
        dia = datetime.today().strftime('%y%m%d')
        filename = '/philanthropynewsdigest_02.csv'
        titulos = []
        textos = []
        links = []
        page = Request('https://philanthropynewsdigest.org/news', headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
        page_request = urlopen(page).read()
        soup = BeautifulSoup(page_request, 'lxml')
        soup2 = soup.find('article', class_ = 'content-view-full full-pnd_landing_page class-pnd_landing_page')
        soup3 = BeautifulSoup(str(soup.find_all('div', class_ = "multiview-item-listing headline-listing")), 'lxml')

        for i in soup3.find_all('a'):
            #print("https://philanthropynewsdigest.org" + i['href'])
            links.append("https://philanthropynewsdigest.org" + i['href'])
            page = Request("https://philanthropynewsdigest.org/news/gates-pledges-1.5-billion-for-climate-projects-in-infrastructure-bill", headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request,'lxml')
            texto = soup.find('div', class_ = "attribute-body ezoe").get_text()
            titulo = soup.find('h1', class_ = "page-title").get_text()
            #rint('findall')

        for i in links:
            page = Request(i, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page_request = urlopen(page).read()
            soup = BeautifulSoup(page_request, 'lxml')
            texto = soup.find('div', class_ = "attribute-body ezoe").get_text()
            titulo = soup.find('h1', class_ = "page-title").get_text()
            textos.append(clean(texto))
            titulos.append(clean(titulo))
            #print('links')
        df = pd.DataFrame()
        df['not_titulo'] = titulos
        df['link'] = links
        df['not_texto'] = textos
        df['atualizacao'] = [dia]*len(df.index)
        df['codigo'] = getCodList(dia, len(df.index), '_2_', 'philantropynewsdigest_')
        df.to_csv(path+filename, index=False)
            
    except Exception as e:

        print(e)
        print('Erro em philantropynewsdigest2')


# philantropynewsdigest2('.')

def philanthropynewsdigest3(path):
   try:
        dia = datetime.today().strftime('%y%m%d')
        titulos = []
        textos = [] 
        links = ['https://candid.org/privacy-policy?fcref=pg','https://philanthropynewsdigest.org/about-pnd']
        filename = '/philantropynewsdigest_03.csv'

        for link in links:  
            req = Request(link, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
            page = urlopen(req).read()
            soup = BeautifulSoup(page, 'lxml')
            #print(soup)
            titulo = soup.find('h1', class_ = "page-title").get_text()
            #print(titulo)
            titulos.append(clean(titulo))
            texto = soup.find('div', class_ = "attribute-body ezoe").get_text()
            #print(texto)
            textos.append(clean(texto))
        df = pd.DataFrame()
        df['pol_titulo'] = titulos
        df['pol_instituicao'] = ['philantropynewsdigest']*len(df.index)
        df['pol_texto'] = textos
        df['link'] = links
        df['codigo'] = getCodList(dia, len(df.index), '_3_', 'philantropynewsdigest_')
        df['atualizacao'] = [dia]*len(df.index)
        df.to_csv(path+filename, index=False)
        
   except Exception as e:
       
        print(e)
        print('Erro em philantropynewsdigest3')

