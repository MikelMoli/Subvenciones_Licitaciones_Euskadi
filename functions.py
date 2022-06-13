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

DEBUG = False


class WebDataExtraction:

    def __init__(self):
        self.driver = self.get_driver()
        self.filename = './data/licitacion_data.json'

    def get_driver(self):
        options = options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path='./geckodriver-v0.31.0-linux64/geckodriver', options=options)
        return driver

    def get_top_box_information(self):
        main_top_information_splitted = self.driver.find_element(By.CLASS_NAME, 'r01gInfoAdicional').text
        return main_top_information_splitted

    def create_empty_register(self):
        # Creates empty register taking into account all the 
        pass

    def scrape_web_data(self, url, driver):
        self.driver.get(url)
        r = requests.get(url) 
        if r.status_code == 200:
            top_box_information = self.get_top_box_information(driver)

            text_data = driver.find_elements(By.CLASS_NAME, 'r01SeccionTexto')

            texts_to_strip = [x.text for x in text_data if 'Razón social' in x.text]
            licitation_companies = texts_to_strip[0]
            adjudication_data= texts_to_strip[1]

            driver.find_element(By.ID, 'aorganismos').click() # Select Organismos tab

            # adjudication_information_box = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[8]/div[2]/p').text # Check and correct

            number_of_bidders = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[1]/div[2]').text
            offers_from_pymes = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[2]/div[2]').text
            offers_from_ue_countries = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[3]/div[2]').text
            offers_from_third_countries = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[4]/div[2]').text
            electronic_offers = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[5]/div[2]').text
            # adjudication_date = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/div[7]/div[4]/div[7]/div[2]').text # Check and correct, date in top box

            adjudication_item = {'Datos de Adjudicación': adjudication_data}
            adjudication_item['Resumen Adjudicación'] =  top_box_information
            adjudication_item['Empresas Licitadoras'] = licitation_companies
            adjudication_item['Num. licitadores presentados'] = number_of_bidders
            adjudication_item['Ofertas realizadas por PYMEs'] = offers_from_pymes
            adjudication_item['Ofertas de países Union Europea'] = offers_from_ue_countries
            adjudication_item['Ofertas terceros paises'] = offers_from_third_countries
            adjudication_item['Ofertas electronicas'] = electronic_offers
            # adjudication_item['Fecha adjudicacion'] = [adjudication_date]


            # elif r.status_code == 404:
            #     print(f'EMPTY BECAUSE 404 {url}')
            #     adjudication_item = {
            #                             'Fecha inicio plazo': '-',
            #                             'Plazo': '-',
            #                             'Razón social': '-',
            #                             'Precio sin IVA': '-',
            #                             'Precio con IVA': '-', 
            #                             'Es probable que el contrato sea objeto de subcontratación': '-', 
            #                             'Num. licitadores presentados': '-', 
            #                             'Ofertas realizadas por PYMEs': '-', 
            #                             'Ofertas de países Union Europea': '-', 
            #                             'Ofertas terceros paises': '-', 
            #                             'Ofertas electronicas': '-', 
            #                             'Fecha adjudicacion': '-'
            #                         }

            

            return adjudication_item
    
        else:
            self.create_empty_register()

if __name__ == "__main__":
    json_file_data = []
    data = pd.read_csv('./data/full_data.csv').loc[0:10]
    web_data = pd.DataFrame()
    driver = get_driver()
    if not DEBUG:
        total = data.shape[0]
        for i, row in data.iterrows():
            print(f'{i}/{total-1}')
            url = row['urlEs']
            print(url)
            try:
                item = scrape_web_data(url, driver)
            except Exception:
                print(url)
                traceback.print_exc()
                empty_item = {'Fecha inicio plazo': '-',
                            'Plazo': '-',
                            'Razón social': '-',
                            'Precio sin IVA': '-',
                            'Precio con IVA': '-', 
                            'Es probable que el contrato sea objeto de subcontratación': '-', 
                            'Num. licitadores presentados': '-', 
                            'Ofertas realizadas por PYMEs': '-', 
                            'Ofertas de países Union Europea': '-', 
                            'Ofertas terceros paises': '-', 
                            'Ofertas electronicas': '-', 
                            'Fecha adjudicacion': '-'
                            }
                item = empty_item

            item['url'] = url
            json_file_data.append(item)
        driver.close()    
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_file_data, json_file, 
                                indent=4,  
                                separators=(',',': '), ensure_ascii=False)
            # web_data = pd.concat([web_data, item], axis=0)

        # web_data.to_csv('./data/scrapped_data.csv', index=False)
    
    # driver.close()