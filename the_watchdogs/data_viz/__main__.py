import sys
from the_watchdogs.preprocess import preprocess
from data_viz import create_sentiment, create_date, word_count
from app import app
from wordcloud import WordCloud
import pathlib
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

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


# MONTH/YEAR LINE GRAPH

def plot_month_year():
    """
    docstring
    """

    # cnn_count, fox_count = create_date()

    # df = pd.concat([cnn_count, fox_count], axis=1)
    # df.columns = ["CNN", "FOX"]
    # df.index.names = ["Date", "Time"]
    # df = df.reset_index()
    # fig = px.line(df, x="Date", y=["CNN", "FOX"], title='Article Count by Month')

    df = create_date()
    fig = px.line(df, title='Article Count by Month')
    fig.update_traces(mode='lines+markers')

    return fig


# WORDCLOUD

def plot_wordcloud_cnn():
    """
    docstring
    """

    cnn_count, _ = word_count()

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(cnn_count)
    fig = px.imshow(wordcloud, title="CNN Word Cloud")
    fig.update_layout(title_font_size=30)
    return fig

####SEPERATE DASH WEBSITE SETUP STUFF###

plot_sentiment = plot_sentiment()
plot_month_year = plot_month_year()
cnn_wordcloud = plot_wordcloud_cnn()

app.layout = dbc.Container([
    html.Br(),

    dbc.Row(html.H1("Coverage of January 6th by News Source")),
        # style = header_style
        # justify = "center"),

    html.Br(),

    dbc.Row(dcc.Graph(id = "multiple bar chart", 
                      figure = plot_sentiment)),
    
    dbc.Row(dcc.Graph(id = "multiple line chart", 
                      figure = plot_month_year)),

    dbc.Row(dcc.Graph(id = "wordcloud", 
                      figure = cnn_wordcloud))],


fluid = True, style = {'backgroundColor': "#D2E5D0"})

if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = 7991)
