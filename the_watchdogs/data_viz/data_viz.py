import sys
from the_watchdogs.preprocess import clean
import pathlib
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc


# dataframe stuff here

def a_function():

    fox_json = pathlib.Path(__file__).parent / "../data/fox_articles.json"
    df_fox = pd.read_json(fox_json)
    print(df_fox)
    return None

# text analysis stuff here

# cnn_text = 