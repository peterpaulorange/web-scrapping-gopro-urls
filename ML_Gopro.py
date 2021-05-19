#Carregando as bibliotecas 
import pandas as pd 
import requests
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


###FUNÇÕES##
def soup(url):
    #Criando tempo 
    time.sleep(0.2)

    #Criando response e fazendo o Soup 
    response = urlopen(url)
    html = response.read()

    bs = BeautifulSoup(html, 'html.parser')

    #Pegando os links de todas as páginas e armazenando 
    for link in bs.find_all("a", href=True):
        Urls.append(link['href'])

    #Pegando o botão caso haja outra página 
    next_page_find = bs.find(class_="andes-pagination__button andes-pagination__button--next")

    #Testando para ver se existe o botão 
    try:
        next_page_text = next_page_find.find(class_='andes-pagination__link ui-search-link')['title']

        #Fazendo condição caso haja próxima página
        if next_page_text == 'Seguinte':
            next_url = next_page_find.find(class_='andes-pagination__link ui-search-link')['href']

            #Refazendo a função
            soup(next_url)
        else:
            print("Acabou")
    except:
        print('Acabou')

def categorizacao(a):
    if 'hero-9' in a:
        return 'HERO 9'
    elif 'hero9' in a:
        return "HERO 9"
    elif 'hero-8' in a:
        return 'HERO 8'
    elif 'hero8' in a:
        return 'HERO 8'
    elif 'max' in a:
        return 'MAX 360'    

#### DATA #####
Urls = []
Check = []

#Entrando na planilha do Google Drive
ads = pd.read_excel('G:/.shortcut-targets-by-id/1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp/BRAND PROTECTION/Ads - ML.xlsm', sheet_name='Cadastrado')

### SCRIPT ######

#Salvando todos as urls dentro do Mercado Livre 
Urls_base = ['https://cameras.mercadolivre.com.br/filmadoras/novo/gopro-hero-8_OrderId_PRICE*DESC_BRAND_30559_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D9%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D46',
'https://cameras.mercadolivre.com.br/filmadoras/novo/gopro-hero-9_OrderId_PRICE*DESC_BRAND_30559_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D7%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D80',
'https://cameras.mercadolivre.com.br/filmadoras/novo/gopro-max-360_OrderId_PRICE*DESC_BRAND_30559_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D6%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D11',
'https://cameras.mercadolivre.com.br/filmadoras/novo/gopro-hero-8-black_OrderId_PRICE*DESC_BRAND_30559_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D9%26applied_value_id%3D2230284%26applied_value_name%3DNovo%26applied_value_order%3D1%26applied_value_results%3D43']

#Loop para realizar função com todas as urls 
for url in Urls_base:
    soup(url)


#Limpando todas as urls 
#Pegando apenas produto 
Urls = [s for s in Urls if 'tracking_id' in s]

#Limpando heros antigas
Urls = [s for s in Urls if not 'hero7' in s]
Urls = [s for s in Urls if not 'hero-7' in s]
Urls = [s for s in Urls if not 'hero6' in s]
Urls = [s for s in Urls if not 'hero-7' in s]
Urls = [s for s in Urls if not 'hero-fusion' in s]
Urls = [s for s in Urls if not 'bateria' in s]
Urls = [s for s in Urls if not '-bat-' in s]
Urls = [s for s in Urls if not '-bat-' in s]

#Criando DataFrame para enviar como anexo no e-mail 
Dataset = pd.DataFrame()

#Colocando todos os links dentro do Dataset 
Dataset['urls'] = Urls

#Deletando duplicatas 
Dataset = Dataset.drop_duplicates()

#Colocando os MLB
Dataset['MLB'] = Dataset['urls'].str[40:50]

#Colocando os itens 
Dataset['Item'] = Dataset['urls'].apply(categorizacao)

#Checkando quais itens estão e não estão na planilha do drive 
Dataset = Dataset.assign(Check=Dataset['MLB'].isin(ads['Code']).astype(int))

#Baixando os dados 
Dataset.to_excel(r'C:\Users\pedro\Documents\FIVE-C\Automation\Urls\Gopro\Download\Gopro_urls.xlsx')

#Enviando por e-mail e notificando para fazer a ação
#Configurando o e-mail e entregando arquivo 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login('pedrocdellazzari@gmail.com', 'kovzzveoqsjzfmcv')

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Urls da GoPro Mercado Livre'
msg['From'] = 'pedrocdellazzari@gmail.com'
msg['body'] = 'Os dados foram adquiridos no dia de hoje. Faça a limpeza final e suba na WebPrice\nNão se esqueça de colocar os MLB no banco de dados após a importação'

part1 = MIMEBase('application','octet-stream')
part1.set_payload(open('/Users/pedro/Documents/FIVE-C/Automation/Urls/Gopro/Download/Gopro_urls.xlsx','rb').read())
encoders.encode_base64(part1)
part1.add_header('Content-Disposition','attachment;filename="Urls.xlsx"')

msg.attach(part1)

server.sendmail('pedrocdellazzari@gmail.com', 'brandprotection@goprobr.com', msg.as_string())
server.quit()