import sys
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import re
import os

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
#driver = webdriver.Chrome(options=chrome_options)

try:
    chrome_options.binary_location = os.environ["GOOGLE_CHROME_BIN"]
except:
    pass

#driver = webdriver.Chrome()
start_url = "https://www2.correios.com.br/sistemas/rastreamento/default.cfm"


def procurar_encomendas(encomenda):
    try:
        caminho_chrome = os.environ["GOOGLE_CHROME_BIN"]
        driver = webdriver.Chrome(options=chrome_options, executable_path=caminho_chrome)
    except:
         driver = webdriver.Chrome(options=chrome_options)
         
    driver.get(start_url)
    try:
        textbox = driver.find_element_by_xpath('//*[@id="objetos"]')
        textbox.send_keys(encomenda)

        okButton = driver.find_element_by_xpath('//*[@id="btnPesq"]')
        okButton.click()
        return processar_info(driver)

    except Exception as e:
        return e
    finally:
        driver.quit()

def processar_info(driver):

    tables = driver.find_elements_by_class_name('sroLbEvent')
    texto = ""

    for element in tables:
        html = element.get_attribute('innerHTML')
        cabecalho = re.search("(?<=<strong>)(.+)(?=</strong>)", html)
        if cabecalho != None:
            cabecalho = cabecalho.group()
        else:
            cabecalho = "Sei nao parça"

        texto += cabecalho + "\n\n"

    return texto


