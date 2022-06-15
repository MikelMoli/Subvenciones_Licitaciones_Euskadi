from ast import arg
import chunk
from inspect import trace
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import requests
import json
import pandas as pd
import traceback
from selenium.webdriver.common.by import By
from multiprocessing import Pool, Value, Array
import time
import numpy as np
from tqdm import tqdm
DEBUG = False

FILENAME = './raw_data/licitacion_data_{}.json'

class WebDataExtraction:

    def __init__(self):
        self.driver = self.get_driver()


    def get_driver(self):
        options = options = Options()
        if not DEBUG:
            options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='./geckodriver-v0.31.0-linux64/geckodriver', options=options)
        return driver


    def get_line_stripped_data(self):
        all_texts = self.driver.find_elements(By.CLASS_NAME, 'r01SeccionTexto')
        empresa_licitadora = '-'
        datos_adjudicacion = '-'
        for text_element in all_texts:
            text = text_element.text
            if 'CIF/NIF' in text:
                empresa_licitadora = text
            elif 'Precio sin IVA' in text:
                datos_adjudicacion = text
                break

        return empresa_licitadora, datos_adjudicacion

    def get_existing_item(self, id, url):
        item = {}
        item["ID"] = id
        item["Resumen Adjudicación"] = self.driver.find_element(By.CLASS_NAME, 'bgInfoAdicional').text

        item["Num. licitadores presentados"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[1]/div[2]').text
        item["Ofertas realizadas por PYMEs"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[2]/div[2]').text
        item["Ofertas de países Union Europea"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[3]/div[2]').text
        item["Ofertas terceros paises"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[4]/div[2]').text
        item["Ofertas electronicas"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[5]/div[2]').text


        empresa_licitadora, datos_adjudicacion = self.get_line_stripped_data()
        
        item["Empresas Licitadoras"] = empresa_licitadora
        item["Datos de Adjudicación"] = datos_adjudicacion
        item["URL"] = url

        self.driver.find_element(By.ID, 'aorganismos').click() # Select Organismos tab
        try:
            item["Poder Adjudicador"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[2]/div[2]/p').text
        except:
            item["Poder Adjudicador"] = '-'
        try:
            item["Ámbito"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[3]/div[2]').text
        except:
            item["Ámbito"] = '-'
        try:
            item["Entidad Impulsora"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[4]/div[2]/p').text
        except:
            item["Entidad Impulsora"] = '-'
        try:
            item["Órgano de Contratación"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[5]/div[2]').text
        except:
            item["Órgano de Contratación"] = '-'
        try:
            item["Entidad Tramitadora"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[6]/div[2]/p').text
        except:
            item["Entidad Tramitadora"] = '-'
        try:
            item["Mesa de contratación"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[7]/div[2]').text
        except:
            item["Mesa de contratación"] = '-'
        try:
            item["Tipo de poder"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[8]/div[2]').text
        except:
            item["Tipo de poder"] = '-'
        try:
            item["Otro tipo de poder"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[9]/div[2]').text
        except:
            item["Otro tipo de poder"] = '-'
        try:
            item["Actividad Principal"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[10]/div[2]').text
        except:
            item["Actividad Principal"] = '-'
        try:
            item["Otra Actividad Principal"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[11]/div[2]').text
        except:
            item["Otra Actividad Principal"] = '-'
        try:
            item["El contrato es adjudicado por una central de compras"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[13]/div[2]').text
        except:
            item["El contrato es adjudicado por una central de compras"] = '-'
        try:
            item["Obtención de documentación e información"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[14]/div[2]').text
        except:
            item["Obtención de documentación e información"] = '-'
        try:
            item["Órgano de recurso"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[15]/div[2]').text
        except:
            item["Órgano de recurso"] = '-'
        try:
            item["Servicio de información sobre recursos"] = self.driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[1]/div[16]/div[2]').text
        except:
            item["Servicio de información sobre recursos"] = '-'

        item["Code"] = "200"

        return item

    def create_empty_register(self, text):
        item  = {
            "ID": "-",
            "Poder Adjudicador": "-",
            "Ámbito": "-",
            "Entidad Impulsora": "-",
            "Órgano de Contratación": "-",
            "Entidad Tramitadora": "-",
            "Mesa de contratación": "-",
            "Tipo de poder": "-",
            "Otro tipo de poder": "-",
            "Actividad Principal": "-",
            "Otra Actividad Principal": "-",
            "El contrato es adjudicado por una central de compras": "-",
            "Obtención de documentación e información": "-",
            "Órgano de recurso": "-",
            "Servicio de información sobre recursos": "-",
            "Resumen Adjudicación": "-",
            "Num. licitadores presentados": "-",
            "Ofertas realizadas por PYMEs": "-",
            "Ofertas de países Union Europea": "-",
            "Ofertas terceros paises": "-",
            "Ofertas electronicas": "-",
            "Empresas Licitadoras": "-",
            "Datos de Adjudicación": "-",
            "URL": "-",
            "Code": text
        }
        return item

    def scrape_web_data(self, id, url):
        self.driver.get(url)
        r = requests.get(url) 
        if r.status_code == 200:
            adjudication_item = self.get_existing_item(id, url)    
        else:
            adjudication_item = self.create_empty_register("404")
        
        return adjudication_item



def scrape_data_or_fail(data):
    max_index = str(data.index.values.max())
    chunk_bounds = str(data.index.values.min()) + '_' + max_index
    json_file_data = []
    scraper = WebDataExtraction()
    total = data.shape[0]
    for i, row in data.iterrows():
        if i % 10 == 0:
            print(f'{i}/{max_index}', flush=True)
        url = row['urlEs']
        id = row['id']

        try:
            item = scraper.scrape_web_data(id, url)
        except Exception:
            print(url, flush=True)
            traceback.print_exc()
            item = scraper.create_empty_register('Exception')
        json_file_data.append(item)
        
    with open(FILENAME.format(chunk_bounds), 'w', encoding='utf-8') as json_file:
        json.dump(json_file_data, json_file, 
                  indent=4,  
                  separators=(',',': '), ensure_ascii=False)
    
    scraper.driver.close()  


if __name__ == "__main__":
    st = time.time()

    # json_file_data = []
    data = pd.read_csv('./data/full_data.csv').loc[0:100]
    web_data = pd.DataFrame()
    
    if not DEBUG:
        p = Pool(processes=8)
        total = data.shape[0]
        chunk_list = [x.copy() for x in np.array_split(data, 5)]
        print(f'Data splitted into {len(chunk_list)} parts')
        result = p.map(scrape_data_or_fail, chunk_list)
        p.terminate()
        p.join()
        # result.wait()
        print('EXECUTION_TIME:', time.time() - st)

    # Execution time 100 registers no multiprocessing --> 159.23
    # Execution time 100 registers 4 processors --> 100.65
    # Execution time 100 registers 8 processors --> 53.86