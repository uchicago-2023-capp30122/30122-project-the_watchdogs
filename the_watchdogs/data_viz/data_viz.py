import sys
import pathlib
import pandas as pd
import numpy as np
from collections import Counter

# Below are the some functions that take the pre-process data, and turn the
# csvs into pandas series to be used in "" to visualize the data:

# Loading in csv files as global variables and saving them as global
# dataframes:
cnn_data = pathlib.Path(__file__).parent / "../data/CNN_clean_df.csv"
fox_data = pathlib.Path(__file__).parent / "../data/FOX_clean_df.csv"

df_cnn = pd.read_csv(cnn_data)
df_fox = pd.read_csv(fox_data)


def word_count():
    """
    docstring
    """
    # text_cnn = df_cnn.clean_text.str.replace('[','').str.replace(']','').str.replace("'",'')
    # text_fox = df_fox.clean_text.str.replace('[','').str.replace(']','').str.replace("'",'')
    # text_cnn = text_cnn.apply(lambda x: x.split(', '))
    # text_fox = text_fox.apply(lambda x: x.split(', '))

    cnn_count = []
    for i in df_cnn.clean_text.values:
        cnn_count += eval(i)
    fox_count = []
    for i in df_fox.clean_text.values:
        fox_count += eval(i)

    cnn_count = pd.Series(Counter(cnn_count)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(fox_count)).sort_values(ascending = False)

    return cnn_count, fox_count


def create_date():
    """
    docstring
    """

    text_cnn = df_cnn.date.apply(lambda x: x.split(','))
    text_fox = df_fox.date.apply(lambda x: x.split(','))

    text_cnn = text_cnn.apply(lambda x: (x[0].split(' ')[0], int(x[1][1:5])))
    text_fox = text_fox.apply(lambda x: (x[0].split(' ')[0], int(x[1][1:5])))
    cnn_count = pd.Series(Counter(text_cnn)).reset_index().set_index('level_0')
    fox_count = pd.Series(Counter(text_fox)).reset_index().set_index('level_0')

    months = ['January','February','March','April','May','July','August','September','October','November','December']
    ind_cnn = cnn_count.level_1
    ind_fox = fox_count.level_1
    cnn_count = cnn_count[0]
    fox_count = fox_count[0]
    years = np.union1d(ind_cnn.unique(), ind_fox.unique())

    res = []
    for y in years:
        temp_cnn = cnn_count[ind_cnn == y].rename(f"CNN {y}")
        if len(temp_cnn) != 0:
            temp_cnn = temp_cnn.reindex(index = months)
            res.append(temp_cnn)

    for y in years:
        temp_fox = fox_count[ind_fox == y].rename(f"FOX {y}")
        if len(temp_fox) != 0:
            temp_fox = temp_fox.reindex(index = months)
            res.append(temp_fox)

    result = pd.concat(res, axis=1)
    result.index.name = 'Date'
    result.reset_index()
    return result

def create_sentiment():
    """
    docstring
    """

    text_cnn = df_cnn.sentiment_category.values
    text_fox = df_fox.sentiment_category.values

    cnn_count = pd.Series(Counter(text_cnn)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(text_fox)).sort_values(ascending = False)

    return cnn_count, fox_count