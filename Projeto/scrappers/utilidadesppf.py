from itertools import compress
import pandas as pd
import re
def getCodList(dia, tamanho, num, filename):
    lista = []
    for i in range(tamanho):
        lista.append(filename + dia + num +str("{0:0=3d}".format(i)))
    return lista
def getInfoBase(path, filename, infotype): #extrai informações da base principal
    links_base = []
    path = path + filename
    try:
        dfbase = pd.read_csv(path)
        links_base=(dfbase[infotype].tolist())
    except:
        pass    
    return links_base
def getNewInfo(info_base, info): #pega a diferença entre duas listas
    track =[i in info_base for i in info] 
    new_info_bool = [not bool for bool in track] 
    new_info=(list(compress(info,new_info_bool)))
    return new_info
def truncate(f, n): #função para truncar o float
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def clean(string):
    string = re.sub('\n', ' ', string)
    string = ' '.join(string.split())
    return string