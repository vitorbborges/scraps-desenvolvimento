# AB#18
# Contruibuição Jairo
# Site: https://erefdn.org
# EREFDN - o que foi capturado parece ser uma lista de projetos aprovados. 

from bs4 import BeautifulSoup
import requests
import re
from re import findall
import pandas as pd
from time import sleep
from datetime import datetime
import os

# a parte de noticias termina em 2019, avaliar se é relevante extrair as noticias desse site.

def erefdn3(path):
  try:
    def soups(paginas):
        headers = {'User-Agent': 
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
        page = requests.get(paginas, headers=headers) # Request para extrair a página html
        soup = BeautifulSoup(page.text,'html.parser') # Lendo a página html 
        a = soup.find('h1')
        b = soup.find('div',id='main')
        return(a.text.encode('utf-8'),b.text.encode('utf-8'))

    pags=['https://erefdn.org/about/','https://erefdn.org/research-grants-projects/']
    nomes=[]
    texto=[]
    cod=[]
    dia = datetime.today().strftime('%y%m%d')
    for i in range(0,len(pags)):
        elementos = soups(pags[i])
        nomes.append(str(elementos[0]))
        texto.append(str(elementos[1]))
        cod.append('erefdn_'+dia+'_03_'+str("{0:0=3d}".format(i)))
    instituto = ['EREFDN']*len(pags)
    atualizacao = [dia]*len(pags)


    nomes = [re.sub(r'''(b'|\\n)''', "", i) for i in nomes]
    texto = [re.sub(r'''(b'|\\n)''', '', i) for i in texto]

    df = pd.DataFrame({'pol_titulo':nomes,'link':pags,'pol_texto':texto,'codigo':cod,'atualizacao':atualizacao,'pol_instituicao':instituto}) 
    path = path+'''\\erefdn_03.csv'''
    df.to_csv(path,index=False,sep=",")  
    return(df)
  except:
    print("Erro na função erefdn3")


def erefdn4(path, keywords = 'brazil'): # A entrada é o caminho do arquivo que vai ser definido no arquivo ppfcentral.py
    try:

        url_pag_principal = 'https://erefdn.org/research-grants-projects/currently-funded-projects'
        end_arq_csv_saida = path+'\\erefdn_04.csv'
        tempo_espera_entre_chamadas =  0.25

        def obtem_soup(url):
            """Obtem o objeto Soup para uma URL
            Recebe:
                    url :: str
            Retorna:
                    soup :: bs4.BeautifulSoup
            """
            
            headers = {'User-Agent': 
                    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            html = requests.get(url, headers=headers)
            soup = BeautifulSoup(html.text, 'lxml')
            
            return soup

        def valor_int(str_valor):
            """Converte o valor financeiro da bolsa de string para int.
            Recebe:
                    str_valor_usd :: str
            Retorna:
                    valor_int :: int
            """
            chars_a_remover = ['$', 'U', 'S', ',', ' ']
            valor_inteiro = ''.join([char for char in str_valor if char not in chars_a_remover])
            return valor_inteiro

        def remove_novas_linhas(str_bruta, sep='\n'):
            """Remove novas linhas '\n's em excesso e 
            devolve uma string com separador=sep.
            Recebe:
                    str_bruta :: str
            Retorna:
                    str_proc  :: str
                    
            Exemplo:
                str_bruta = '\n\nCampo 1:\n\n\nValor 1\n\nValor2\n\n\n'
                str_proc = 'Campo 1:\nValor 1\nValor2'
            """
            return re.sub('\n+', sep, str_bruta).strip()

        def gera_csv(lista_bolsas, end_arq_csv_saida):
            """Cria um arquivo de saida no formato CSV.
            Recebe:
                    lista_bolsas :: list(dicts)
            Retorna:
                    arquivo de saida  :: arquivo csv
                    df_bolsas :: Pandas.DataFrame

            """
            
            # Gera um dataframe a partir da lista de bolsas
            df_bolsas = pd.DataFrame(lista_bolsas)
            
            return df_bolsas

        def parse_cabecalho(cabecalho):
            """Parse do cabecalho, Titulo e Investigators
            Recebe: 
                    cabecalho do artigo :: soup
            Retorna:
                    titulo :: str
                    instituicao :: str
            """
            # Obtem o titulo
            try:
                titulo = cabecalho.h1.text
            except:
                print(".. Erro - parse_cabecalho: titulo")
                titulo = 'None'

            # Obtem a instituicao
            try:
                instituicao = cabecalho.p.text.split(':')[1].strip()
            except:
                print(".. Erro - parse_cabecalho: instituicao")
                instituicao = 'None'
            
            return titulo, instituicao

        def parse_data_valor(data_valor):
            """Parse do Data de Inicio, Valor da bolsa
            Recebe: 
                    data_valor :: soup
            Retorna:
                    data_ini :: str
                    valor :: str
            """

            tags_p = data_valor.find_all('p')
            idx = 0
            
            # Obtem a data incial
            try:
                data_ini = tags_p[idx].text.split('Start Date:')[1].strip()
                idx += 1
            except:
                #print(".. Erro - parse_data_valor: data_ini")
                data_ini = 'None'
            
            # Obtem o valor
            try:
                valor = tags_p[idx].text.split('Award Amount:')[1].strip()
            except:
                print(".. Erro - parse_data_valor: valor")
                valor = 'None'
            
            return data_ini, valor

        def parse_descricao(descricao):
            """Parse da descricao detalhada 
            Recebe: 
                    descricao :: soup
            Retorna:
                    descricao_detalhada :: str
            """
            # Obtem a descricao detalhada da bolsa
            try:
                descricao_detalhada = remove_novas_linhas(descricao.text)

            except:
                print(".. Erro - parse_descricao: descricao_detalhada")
                descricao_detalhada = 'None'
            
            return descricao_detalhada

        def parse_links_refs(links_refs):
            """Parse dos links referenciados em um artigo 
            Recebe: 
                    links_refs :: soup
            Retorna:
                    lista_links :: list(str)
            """
            lista_links = []
            for el in links_refs:
                lista_links.append({el.text: el.get('href')})
            
            if len(lista_links) == 0:
                lista_links = 'Nao referencia links.'
            
            return lista_links

        def obtem_sessoes_artigo(soup_artigo):
            """Separa as partes de um artigo, conforme layout do site.
            
            Partes:
                Sessao 1 - Cabecalho, contendo (Titulo, Instituicao)
                Sessao 2 - Data e Valor, contendo (Data de Inicio, Valor concedido (USD))
                Sessao 3 - Descricao Detalhada
                
            Recebe: 
                    soup_artigo :: soup
            Retorna:
                    cabecalho :: soup
                    data_valor :: soup
                    descricao :: soup
            """    
            # Filtra apenas o conteudo de interesse
            conteudo_interesse_artigo = soup_artigo.find(class_="entry-content")
            links_referenciados = conteudo_interesse_artigo.findAll('a')
            elementos = conteudo_interesse_artigo.findAll(class_="vc_row wpb_row vc_row-fluid")
            
            # Divide o objeto soup em setores, conforme layout da pagina
            cabecalho = elementos[0]
            data_valor = elementos[1]
            descricao = elementos[2]
            
            return cabecalho, data_valor, descricao, links_referenciados

        def parse_lista_bolsas(soup_pag_princ):
            """Parse da pagina principal com 
            a lista de bolsas a ser coletada.
            Recebe: 
                    soup da pagina
            Retorna:
                    lista_bolsas:: list(dicts)
                        titulo :: str
                        url_artigo :: str
            """
            # Filtra a regiao de interesse dentro da pagina principal
            conteudo_interesse_pag_princ = soup_pag_princ.find(class_="entry-content")
            
            # Obtem a lista de bolsas disponiveis
            lista_bolsas = []
            tags_a = conteudo_interesse_pag_princ.findAll('a')

            # Para cada tag a, isola o link e o titulo do artigo e adiciona à lista de retorno
            for el in tags_a:
                titulo = el.text.strip()
                url_artigo = el.get('href')

                lista_bolsas.append({'titulo': titulo, 'url_artigo': url_artigo})
        
            return lista_bolsas

        def processa_artigo(url_artigo):
            """Processamento completo de um artigo (bolsa)
            Recebe: 
                    url_artigo :: str
            Retorna:
                    dict contendo:
                        'titulo':: str, 
                        'instituicao':: str,
                        'data_ini':: str,
                        'valor':: str,
                        'descr_detalhada':: str
                        'links':: str,
                        'links_referenciados' :: list(str)
            """
            # Obtem o objeto soup para uma bolsa especifica
            soup_artigo = obtem_soup(url_artigo)

            # Divide o objeto soup em setores, conforme layout da pagina
            cabecalho, data_valor, descricao, links_refs = obtem_sessoes_artigo(soup_artigo)
            
            titulo, instituicao = parse_cabecalho(cabecalho)
            data_ini, valor = parse_data_valor(data_valor)
            descr_detalhada = parse_descricao(descricao)
            links = parse_links_refs(links_refs)
                
            # Monta dicionario de retorno
            dados_bolsa = {'titulo': titulo, 
                        'instituicao': instituicao,
                        'data_ini': data_ini,
                        'valor': valor,
                        'descr_detalhada': descr_detalhada,
                        'url_artigo': url_artigo,
                        'links_referenciados': links
                        }
            
            return dados_bolsa

        def processa_pag_principal(url_pag_principal, log=False):
            """Processamento completo da pagina. 
            Gera a lista de bolsas disponiveis. Para cada bolsa, 
                faz o processamento completo dos dados.
            Recebe: 
                    url da paginas principal :: str
            Retorna:
                    lista_bolsas :: list(dicts) com o parsing completo de cada bolsa.
            """
            # Obtem o objeto soup para a pagina inicial
            soup_pag_princ = obtem_soup(url_pag_principal)
            
            # Obtem a lista de titulo e url de todas as bolsas
            tit_url_bolsas = parse_lista_bolsas(soup_pag_princ)
            lista_bolsas = []
            
            # Para cada bolsa, processa a pagina correspondente
            for i, bolsa in enumerate(tit_url_bolsas):
                # Obtem informacoes basicas de cada bolsa
             #   print(f'---- Processando artigo {i + 1:2d}.. {bolsa["titulo"][:min(60, len(bolsa["titulo"]))]}..')
                
                # Obtem o parsing completo da bolsa, dict com os dados
                dados_bolsa = processa_artigo(bolsa['url_artigo'])
                
                # Salva o resultado na lista de dict
                lista_bolsas.append(dados_bolsa)
                
                # Espera um tempo para evitar sobrecarregar o site        
                sleep(tempo_espera_entre_chamadas)

            return lista_bolsas

        # Obtem a lista de parsings para cada bolsa
        lista_bolsas = processa_pag_principal(url_pag_principal)
    
        # Gera o arquivo CSV de saida
        df = gera_csv(lista_bolsas, end_arq_csv_saida)
        df = df.drop(columns=['links_referenciados', 'data_ini'])
        df = df.rename(columns={"titulo": "prj_titulo","instituicao":"prj_instituicao","valor":"prj_valor","url_artigo":"link","descr_detalhada":"prj_texto"})
        dia = datetime.today().strftime('%y%m%d')
        df['atualizacao']=[dia]*len(df['link'])
        cod=[]
        brazil=[]
        for i in range(0,len(df['link'])):
            cod.append('erefdn_'+dia+'_04_'+str("{0:0=3d}".format(i))) # codigo indexador padrao: nomedosite_data_nºgrupoextracao_indexador
            a = findall('brazil', df['prj_texto'][i].lower()) # Procurando se contém brazil no texto
            if len(a) != 0: # Se o vetor não for vazio contém, se for vazio não contém
                brazil.append("Y") 
                # print('contém BR')
            else:
                brazil.append("N")           
        df['codigo']=cod
        df['brazil']=brazil

        # Gera o CSV
        df.to_csv(end_arq_csv_saida, sep=',', index=False, encoding='utf-8')
            


    except:
        print('Erro na função erefdn4')














