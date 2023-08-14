import pandas as pd
from typing import List
from re import sub
import numpy as np

def snake_case(s:str):
    """to snake_case"""
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


def fill_and_frame(
    data:pd.DataFrame,
    model_names:List[str])->pd.DataFrame:
    """
    fill the dataframe with NA on the columns
    that aren't available (as the model impute them automatically)
    and returns a data frame copy with only the rows needed
    """
    
    col_data_set = {*data.columns}
    names_set = {*model_names}
    missing_names = names_set.difference(col_data_set)

    for nm in missing_names:
        data[nm] = np.NaN        

    return data[model_names]
