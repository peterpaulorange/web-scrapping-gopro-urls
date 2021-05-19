#Carregando bibliotecas
import pandas as pd 
import requests 
import time 
import requests
from urllib.request import urlopen
from requests_html import HTML 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

#Configurando o driver 
options = Options()
options.add_argument('--headless')

#Pegandoo arquivo do driver para a amazon 
driver = webdriver.Chrome(executable_path='C:\Program Files\chromedriver\chromedriver.exe',options=options)

#FUNÇÕES 
def soup_magalu(url):
    #Criando o tempo 
    time.sleep(0.2)

    #Fazendo o request 
    response = urlopen(url)
    html = response.read()

    #Criando o soup 
    bs = BeautifulSoup(html, 'html.parser')

    #Pegando os links 
    for link in bs.find_all('a', href=True):
        Links_magalu.append(link['href'])

def soup_americanas(url):
    #Pegando o tempo 
    time.sleep(0.5)

    #Fazendo os headers 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.218'}

    #Fazendo o request 
    response = requests.get(url, headers=headers)
    html = response.text

    #Criando o soup 
    bs = BeautifulSoup(html, 'html.parser')

    #Pegando os links 
    for link in bs.find_all('a', href=True):
        Links_americanas.append('https://www.americanas.com.br' + link['href'])

def soup_extra(url):
    #Pegando o tempo 
    time.sleep(0.3)

    #Criando os headers 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.218'}

    #Fazendo o response 
    response = requests.get(url, headers=headers)
    html = response.text

    #Criando o soup 
    bs = BeautifulSoup(html, 'html.parser')

    #Achando os os links 
    for link in bs.find_all('a', href=True):
        Links_extra.append(link['href'])

#DATA 
Links_americanas = []
Links_magalu = []
Links_extra = []
Urls = []
Store = []

#Criando o DataFrame 
Dataset = pd.DataFrame() 

# MAGALU 
#Pegando as urls 
urls_base_magalu = ['https://www.magazineluiza.com.br/busca/gopro%20hero%208/?ordem=maior-preco',
             'https://www.magazineluiza.com.br/busca/gopro%20hero%209/?ordem=maior-preco',
             'https://www.magazineluiza.com.br/busca/gopro%20max%20360/?ordem=maior-preco']

#Fazendo a função com as urls 
for url in urls_base_magalu:
    soup_magalu(url)

#Limpando os links
Links_magalu = [s for s in Links_magalu if '/p/' in s]
Links_magalu = [s for s in Links_magalu if 'gopro' in s]
Links_magalu = [s for s in Links_magalu if not 'carregador' in s]
Links_magalu = [s for s in Links_magalu if not 'suporte' in s]
Links_magalu = [s for s in Links_magalu if not 'caixa' in s]
Links_magalu = [s for s in Links_magalu if not 'bateria' in s]
Links_magalu = [s for s in Links_magalu if not 'controle' in s]
Links_magalu = [s for s in Links_magalu if not 'filtros' in s]
Links_magalu = [s for s in Links_magalu if not 'capa' in s]
Links_magalu = [s for s in Links_magalu if not 'kit' in s]
Links_magalu = [s for s in Links_magalu if not 'moldura' in s]
Links_magalu = [s for s in Links_magalu if not 'haste' in s]
Links_magalu = [s for s in Links_magalu if not 'modulo' in s]
Links_magalu = [s for s in Links_magalu if not 'modulo' in s]
Links_magalu = [s for s in Links_magalu if not 'floaty' in s]
Links_magalu = [s for s in Links_magalu if not 'porta' in s]
Links_magalu = [s for s in Links_magalu if not 'case' in s]
Links_magalu = [s for s in Links_magalu if not 'pelicula' in s]
Links_magalu = [s for s in Links_magalu if not 'touch' in s]
Links_magalu = [s for s in Links_magalu if not 'protetora' in s]
Links_magalu = [s for s in Links_magalu if not 'filtro' in s]
Links_magalu = [s for s in Links_magalu if not 'protecao' in s]
Links_magalu = [s for s in Links_magalu if not 'protetores' in s]
Links_magalu = [s for s in Links_magalu if not 'protetora' in s]
Links_magalu = [s for s in Links_magalu if not 'estojo' in s]
Links_magalu = [s for s in Links_magalu if not 'boia' in s]
Links_magalu = [s for s in Links_magalu if not 'bastao' in s]


# B2W (Americanas)
#Pegando as urls 
urls_base_b2w = ['https://www.americanas.com.br/busca/gopro-hero-8?sortBy=higherPrice&limit=24&offset=0',
                 'https://www.americanas.com.br/busca/gopro-hero-9?sortBy=higherPrice&limit=24&offset=0',
                 'https://www.americanas.com.br/busca/gopro-max-360?sortBy=higherPrice&limit=24&offset=0']

#Fazendo a função 
for url in urls_base_b2w:
    soup_americanas(url)

#Limpando os links 
Links_americanas = [s for s in Links_americanas if 'produto' in s]

#EXTRA
#Pegando as urls 
urls_base_extra = ['https://www.extra.com.br/gopro-hero-8/b?sortby=descprice',
                   'https://www.extra.com.br/gopro-hero-9/b?sortby=descprice',
                   'https://www.extra.com.br/gopro-max-360/b?sortby=descprice']

#Fazendo a função 
for url in urls_base_extra:
    soup_extra(url)

#Limpando os links 
Links_extra = [s for s in Links_extra if 'IdSku=' in s]
Links_extra = [s for s in Links_extra if 'gopro' in s]
Links_extra = [s for s in Links_extra if not 'bateria' in s]
Links_extra = [s for s in Links_extra if not 'suporte' in s]
Links_extra = [s for s in Links_extra if not 'capa' in s]
Links_extra = [s for s in Links_extra if not 'porta' in s]
Links_extra = [s for s in Links_extra if not 'bateria' in s]
Links_extra = [s for s in Links_extra if not 'moldura' in s]
Links_extra = [s for s in Links_extra if not 'adaptador' in s]
Links_extra = [s for s in Links_extra if not 'filtro' in s]
Links_extra = [s for s in Links_extra if not 'peliculas' in s]
Links_extra = [s for s in Links_extra if not 'filtro' in s]
Links_extra = [s for s in Links_extra if not 'boia' in s]

#Colocando os nomes da loja na quantidade de produtos 
for item in Links_magalu:
    Store.append('Magalu')

for item in Links_americanas:
    Store.append('Americanas')

for item in Links_extra:
    Store.append('Extra')

#Colocando os dados na lista princiapl 
Urls = Links_magalu + Links_americanas + Links_extra

#Colocando as informações no Dataframe
Dataset['Urls'] = Urls 
Dataset['Store'] = Store

#Exportando 
Dataset.to_excel(r'C:\Users\pedro\Downloads\Gopro_marketplaces_urls.xlsx', index=False)