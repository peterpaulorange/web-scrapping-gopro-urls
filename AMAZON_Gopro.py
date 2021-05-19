#Carregando bibliotecas 
import pandas as pd 
import requests 
import time 
from requests_html import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Configurando as options do selenium
options = Options()
options.add_argument("--headless")

#Configurando o driver 
driver = webdriver.Chrome(executable_path='C:\Program Files\chromedriver\chromedriver.exe',options=options)

#FUNÇÕES 
def soup(url):
    #Criando tempo
    time.sleep(0.3)

    #Criando o processo de pegar as informações do site 
    driver.get(url)
    body_el = driver.find_element_by_css_selector('body')
    html_str = body_el.get_attribute('innerHTML')
    html_obj = HTML(html=html_str)

    #Pegar os links da página
    links = [x for x in html_obj.links]

    #Criando os links dos produtos 
    products_links = [f'https://www.amazon.com.br{x}' for x in links]
    
    #Fazendo o append dos links 
    for link in products_links:
        Links.append(link)

    #Vendo se tem próxima página 
    try: 
        prox = driver.find_element_by_class_name('a-last')
        prox_text = prox.text
        prox_link = prox.find_element_by_css_selector('a').get_attribute('href')
        print(prox_link)
        #Usar a função de novo 
        soup(prox_link)
    except:
        print('Acabou')

def search_attributes(urls):
    #Criando o tempo 
    time.sleep(0.3)

    #Criando o processo de pegar as informações do site para cada url
    for url in urls:
        driver.get(url)
        body_el = driver.find_element_by_css_selector('body')
        html_str = body_el.get_attribute('innerHTML')
        html_obj = HTML(html=html_str)

        #Achando o preço 
        try:
            product_price = html_obj.find('#priceblock_ourprice', first=True).text

            #Fazendo o appends 
            Price.append(product_price)
        except:
            print('Errado')
            Price.append('Errado')

        #Pegando os links 
        page_link = [x for x in html_obj.links]

        #Pegando apenas os links de sellers
        page_link = [f'https://www.amazon.com.br{x}' for x in page_link]
        page_link = [s for s in page_link if 'seller=' in s]

        
        for link in page_link:
            #Pegando um tempo 
            time.sleep(0.2)
            
            #Entrando no link
            try:
                driver.get(link)
                body_el = driver.find_element_by_css_selector('body')
                html_str = body_el.get_attribute('innerHTML')
                html_obj = HTML(html=html_str)

                #Pegando o nome do Seller
                seller_name = html_obj.find('#sellerName',first=True).text

                #Fazendo o apend com o nome do Seller 
                Sellers.append(seller_name)
            except:
                print("Erro Seller")
                Sellers.append("Erro Seller")
  

#DATA
Links = []
Sellers = []
Price = []

#Pegando a url mãe 
url_base = 'https://www.amazon.com.br/s?k=estabilizador+zhiyun&rh=p_n_condition-type%3A13862762011&s=price-desc-rank&dc&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2QE7XW1M1WBN7&qid=1619112029&rnid=13862761011&sprefix=estabilizador+z%2Caps%2C295&ref=sr_nr_p_n_condition-type_1'


#Utilizando a função para pegar todas as urls e links de páginas
soup(url_base)

#Limpando os links 
Links = [s for s in Links if "/dp/" in s]

#Criando o DataFrame
Dataset = pd.DataFrame()

#Colocando os links no DataFrame
Dataset['Urls'] = Links

#Dropando duplicatas 
Dataset = Dataset.drop_duplicates()

#Exportando o Dataset
Dataset.to_excel(r'C:\Users\pedro\Desktop\amazon.xlsx', index=False)