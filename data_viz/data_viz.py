import sys
print(sys.executable)
from clean import clean
import pathlib
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc


# dataframe stuff here

fox_json = pathlib.Path(__file__).parent / "data/fox_articles.json"
df_fox = read_json(fox_json)

cnn_json = pathlib.Path(__file__).parent / "data/fox_articles.json"
df_cnn = read_json(fox_json)

# text analysis stuff here

cnn_text = 