import sys
from the_watchdogs.preprocess import preprocess
import pathlib
from wordcloud import WordCloud
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from collections import Counter

# GENERAL HELPER FUNCTIONS:

# Loading in csv files as global variables and saving them as global
# dataframes:
cnn_data = pathlib.Path(__file__).parent / "../data/CNN_clean_df.csv"
fox_data = pathlib.Path(__file__).parent / "../data/FOX_clean_df.csv"

df_cnn = pd.read_csv(cnn_data)
df_fox = pd.read_csv(fox_data)

def create_dataframe():
    """
    docstring
    """

    cnn_data = pathlib.Path(__file__).parent / "../data/CNN_clean_df.csv"
    fox_data = pathlib.Path(__file__).parent / "../data/FOX_clean_df.csv"

    df_cnn = pd.read_csv(cnn_data).clean_text.str.replace('[','').str.replace(']','').str.replace("'",'')
    df_fox = pd.read_csv(fox_data).clean_text.str.replace('[','').str.replace(']','').str.replace("'",'')

    df_cnn = df_cnn.apply(lambda x: x.split(', '))
    df_fox = df_fox.apply(lambda x: x.split(', '))

    cnn_count = []
    for i in df_cnn.values:
        cnn_count += i
    fox_count = []
    for i in df_fox.values:
        fox_count += i

    cnn_count = pd.Series(Counter(cnn_count)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(fox_count)).sort_values(ascending = False)
    return cnn_count, fox_count


def word_count():
    """
    docstring
    """

    text_cnn = df_cnn.clean_text.str.replace('[','').str.replace(']','').str.replace("'",'')
    text_fox = df_fox.clean_text.str.replace('[','').str.replace(']','').str.replace("'",'')

    text_cnn = text_cnn.apply(lambda x: x.split(', '))
    text_fox = text_fox.apply(lambda x: x.split(', '))

    cnn_count = []
    for i in text_cnn.values:
        cnn_count += i
    fox_count = []
    for i in text_fox.values:
        fox_count += i

    cnn_count = pd.Series(Counter(cnn_count)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(fox_count)).sort_values(ascending = False)
    return cnn_count, fox_count


def create_date():
    """
    docstring
    """

    text_cnn = df_cnn.date.apply(lambda x: x.split(','))
    text_fox = df_fox.date.apply(lambda x: x.split(','))

    text_cnn = text_cnn.apply(lambda x: (x[0].split(' ')[0], x[1][:5]))
    text_fox = text_fox.apply(lambda x: (x[0].split(' ')[0], x[1][:5]))

    cnn_count = pd.Series(Counter(text_cnn)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(text_fox)).sort_values(ascending = False)
    #  pd.concat([cnn_count, fox_count], axis=1).dropna()
    #  cnn_count, fox_count.loc[cnn_count.index]
    return cnn_count, fox_count


def create_sentiment():
    """
    docstring
    """

    text_cnn = df_cnn.sentiment_category.values
    text_fox = df_fox.sentiment_category.values

    cnn_count = pd.Series(Counter(text_cnn)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(text_fox)).sort_values(ascending = False)
    
    return cnn_count, fox_count