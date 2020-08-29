import xlrd
from typing import Dict, List, Union


def load_xl_data(filename: str) -> Union[Dict[str, List[str]], bool]:
    try:
        in_wb = xlrd.open_workbook(filename)
        in_sh = in_wb.sheet_by_index(0)

        answers_kw_dict = {}

        for i in range(3, in_sh.nrows):
            answer = in_sh.cell_value(i, 1)
            key_words = in_sh.cell_value(i, 2).split()
            answers_kw_dict[answer] = key_words
            
        return answers_kw_dict
    except:
        return False