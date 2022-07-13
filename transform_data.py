import os
from typing import final
import pandas as pd
import utils

class TransformAndMergeData:

    def __init__(self):
        self.raw_data_path = './data/raw_data/'
        

    def get_complete_df(self):
        file_list = os.listdir(self.raw_data_path)
        full_df = pd.DataFrame()
        for file in file_list:
            df = pd.read_json(f'{self.raw_data_path}{file}')
            full_df = pd.concat([full_df, df], axis=0)

        return full_df

    def add_empty_register_to_dict(self, final_dict):
        for key in final_dict.keys():
            final_dict[key].append('-')
        return final_dict

    def handle_adjudication_summary(self, text, final_dict):
        # url = row['URL']
        splitted_text = text.split("\n")
        splitted_dict = {}
        for x in splitted_text:
            if ':' not in x:
                continue
            splitted = x.split(':')
            if '/' in x:
                final_dict[splitted[0].lstrip()].append(':'.join(splitted[1:]).lstrip())
            else: 
                final_dict[splitted[0].lstrip()].append(splitted[1].lstrip())
        
        return final_dict

    def fix_dictionary_dimensions(self, final_dict, url, i):
        for key, item in final_dict.items():
            if len(item) < i+1:
                # Check if the logic of adding an empty record here is correct or not
                final_dict[key].append('-')
                # print(f'CHECK IF {key} exists in the next adjudication: {url}')
                # raise Exception
        return final_dict

    def check_dictionary_dimensions(self, final_dict, url, empty):
        item_len = -1
        for key, item in final_dict.items():
            if item_len == -1:
                item_len = len(item)
                continue
            elif len(item) != item_len:
                # Check if the logic of adding an empty record here is correct or not
                final_dict[key].append('-')
                print(f'CHECK IF {key} exists in the next adjudication: {url}')
                print(f'Empty register: {empty}')
                raise Exception
        return final_dict

    def splitted_lines_to_columns(self, df):
        
        final_dict = {key: [] for key in utils.new_columns}
        for i, row in df.iterrows():

            text = row['Resumen Adjudicación']
            url = row['URL']
            empty = False
            if text != '-':
                final_dict = self.handle_adjudication_summary(text, final_dict)
            else:
                final_dict = self.add_empty_register_to_dict(final_dict)
                empty = True
            final_dict = self.fix_dictionary_dimensions(final_dict, url, i) # Do it with the assert

            assert self.check_dictionary_dimensions(final_dict, url, empty)
        
        df = pd.concat([df, pd.DataFrame.from_dict(final_dict)], axis=1)
        return df

    def run(self):
        
        if 'scrapped_data_sample.csv' in os.listdir('./data/'):
            df = pd.read_csv('./data/scrapped_data_sample.csv')
        else:
            df = self.get_complete_df()
        
        KEYS_TO_SPLIT = ['Resumen Adjudicación', 'Empresas Licitadoras', 'Datos de Adjudicación', 'Otro tipo de poder']
        df = self.splitted_lines_to_columns(df)
        df.drop(KEYS_TO_SPLIT, axis=1, inplace=True)
        df.to_csv('dict_sample.csv', index=False)

if __name__ == '__main__':
    run_class = TransformAndMergeData()
    run_class.run()
    #df = run_class.run()
    #df.to_csv(f'./data/scrapped_data_sample.csv', index=False)
