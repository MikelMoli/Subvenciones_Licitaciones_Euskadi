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

    def add_empty_register_to_dict(self, final_dict, i):
        for key in final_dict.keys():
            if len(final_dict[key]) < i+1:
                final_dict[key].append('-')
        return final_dict

    def handle_splitted_lines_text(self, text, final_dict, i):
        splitted_text = text.split("\n")
        for x in splitted_text:
            if ':' not in x:
                continue
            splitted = x.split(':')
            if len(final_dict[splitted[0]]) < i+1:
                if '/' in x:
                    final_dict[splitted[0].lstrip()].append(':'.join(splitted[1:]).lstrip())
                else: 
                    final_dict[splitted[0].lstrip()].append(splitted[1].lstrip())
        
        return final_dict

    def fix_dictionary_dimensions(self, final_dict, i):
        for key, item in final_dict.items():
            if len(item) < i+1:
                # Check if the logic of adding an empty record here is correct or not
                final_dict[key].append('-')
                # print(f'CHECK IF {key} exists in the next adjudication: {url}')
                # raise Exception
        return final_dict

    def check_dictionary_dimensions(self, final_dict, url, empty, i):
        item_len = -1
        for key, item in final_dict.items():
            if item_len == -1:
                item_len = len(item)
                continue
            elif len(item) != item_len:
                # Check if the logic of adding an empty record here is correct or not
                print(i)
                print(f'CHECK IF {key} exists in the next adjudication: {url}')
                print(f'Empty register: {empty}')
                raise Exception
        return final_dict

    def splitted_lines_to_columns(self, df):
        
        final_dict = {key: [] for key in utils.NEW_COLUMNS_TO_ADD} # ADD ALL COLUMNS
        for i, row in df.iterrows():
            if i == 0:
                print('paro')
            url = row['URL']
            for key in utils.KEYS_TO_SPLIT:
                text = row[key]

                empty = False
                if text != '-':
                    final_dict = self.handle_splitted_lines_text(text, final_dict, i)
                else:
                    # HAY QUE CAMBIAR LA LÓGICA DE ESTO PORQUE SI NO VA A AÑADIR 1 EMPTY POR KEY
                    final_dict = self.add_empty_register_to_dict(final_dict, i)
                    empty = True
            
            final_dict = self.fix_dictionary_dimensions(final_dict, i) # Do it with the assert

            assert self.check_dictionary_dimensions(final_dict, url, empty, i)

        return final_dict


    def run(self):
        if 'scrapped_data_sample.csv' in os.listdir('./data/'):
            df = pd.read_csv('./data/scrapped_data_sample.csv')
        else:
            df = self.get_complete_df()
        

        final_dict = self.splitted_lines_to_columns(df)
        df = pd.concat([df, pd.DataFrame.from_dict(final_dict)], axis=1)
        df.drop(utils.KEYS_TO_SPLIT, axis=1, inplace=True)
        df.to_csv('dict_sample.csv', index=False)

if __name__ == '__main__':
    run_class = TransformAndMergeData()
    run_class.run()
    #df = run_class.run()
    #df.to_csv(f'./data/scrapped_data_sample.csv', index=False)
