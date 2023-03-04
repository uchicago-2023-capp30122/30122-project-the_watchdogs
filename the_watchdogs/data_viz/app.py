import sys
from the_watchdogs.preprocess import preprocess
from data_viz import create_sentiment
import pathlib
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# SENTIMENT STACKED BAR CHART:

def plot_sentiment():
    """
    docstring
    """

    cnn_count, fox_count = create_sentiment()
    df = pd.concat([cnn_count, fox_count], axis=1)
    df.columns = ["CNN", "FOX"]

    # Defining the order of x-axis:
    category_order = ["Very Negative", "Slightly Negative", "Neutral", "Slightly Positive", "Very Positive"]

    fig = px.bar(df, x=df.index, y=["CNN", "FOX"],
                 barmode='group', labels={'value': 'Frequency'},
                 category_orders={'index': category_order})
    fig.update_layout(title='Sentiment Analysis by News Source', xaxis_title='Sentiment',
                      yaxis_title='Number of Articles')

    return fig

if __name__ == '__main__':
    fig = plot_sentiment()
    fig.show()


# MONTH/YEAR LINE GRAPH

def plot_month_year():
    """
    docstring
    """
    
    pass