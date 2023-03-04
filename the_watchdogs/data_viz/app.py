import sys
from the_watchdogs.preprocess import preprocess
from data_viz import create_dataframe, merge_dataframe
import pathlib
from wordcloud import WordCloud
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# WORDCLOUD:

# Load data from helper functions
word_cnn, word_fox = create_dataframe()

# create the wordcloud
wordcloud = WordCloud().generate_from_frequencies(word_frequencies)

# create the Plotly figure
fig = go.Figure(data=go.Image(z=wordcloud.to_array()))

# set the layout
layout = html.Div([
    dcc.Graph(
        id='wordcloud-graph',
        figure=fig
    )
])

# create the app
app = Dash(__name__)
app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
