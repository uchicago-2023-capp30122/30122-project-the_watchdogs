# Rohit Kandala (cnet: "rohitk") wrote the code in this file. 

import sys
from data_viz_prep import create_sentiment, create_date, word_count
from app import app
from wordcloud import WordCloud
import pathlib
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


### BELOW ARE THE DATA VISUALIZATION FUNCTIONS ###


def plot_sentiment():
    """
    Returns:
        This function creates a bar chart with multiple bars per sentiment 
        category (one for CNN & one for FOX) and counts the frequency of 
        articles on the y-axis. 
    """

    # Calling in function from **, and concatinating into a dataframe:
    cnn_count, fox_count = create_sentiment()
    df = pd.concat([cnn_count, fox_count], axis=1)
    df.columns = ["CNN", "FOX"]

    # Setting the order of x-axis:
    category_order = ["Very Negative", "Slightly Negative", "Neutral", "Slightly Positive", "Very Positive"]

    # Creating the bar graph:
    color_discrete_map = {'CNN': 'rgb(204, 0, 0)', 'FOX': 'rgb(0, 51, 102)'}

    fig = px.bar(df, x=df.index, y=["CNN", "FOX"],
                 barmode='group', labels={'value': 'Frequency'},
                 category_orders={'index': category_order}, color_discrete_map=color_discrete_map)
    fig.update_layout(title='Sentiment Analysis by News Source', xaxis_title='Sentiment',
                      yaxis_title='Number of Articles')

    # Return statement:
    return fig


def plot_month_year():
    """
    Returns:
        This function creates a line chart with multiple lines per news source
        (one for CNN & one for FOX) and counts the frequency of articles on the
        y-axis. Moreover, this visualization offers an interactive element where
        users can toggle the year!
    """

    # Calling in function from **, and saving it into a dataframe:
    df = create_date()

    # Creating the line graph:
    fig = px.line(df, title='Article Count by Month')
    fig.update_traces(mode='lines+markers')

    # Adding a toggle by year:
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label = 'All Years',
                        method = 'update',
                        args = [{'visible': [True, True, True, False, True, True, True]},
                                {'title': 'Articles by Year',
                                'showlegend':True}]),
                    dict(label = '2021 Articles',
                        method = 'update',
                        args = [{'visible': [True, False, False, False, True, False, False]},
                                {'title': 'Articles from 2021',
                                'showlegend':True}]),
                    dict(label = '2021 Articles',
                        method = 'update',
                        args = [{'visible': [False, True, False, False, False, True, False]},
                                {'title': 'Articles from 2022',
                                'showlegend':True}]),
                    dict(label = '2021 Articles',
                        method = 'update',
                        args = [{'visible': [False, False, True, False, False, False, True]},
                                {'title': 'Articles from 2023',
                                'showlegend':True}]),
                ])
            )
       ]
    )

    # Return statement:
    return fig


def plot_wordcloud_cnn():
    """
    Returns:
        This function creates a word cloud unique to CNN data, and the larger
        the words are, the more prevalent they are in terms on the frequency.
    """

    # Unpacking the tuple:
    cnn_count, _ = word_count()

    # Creating the word cloud:
    wordcloud_cnn = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(cnn_count)
    fig = px.imshow(wordcloud_cnn, title="CNN Word Cloud")
    fig.update_layout(title_font_size=30)

    # Return statement:
    return fig


def plot_wordcloud_fox():
    """
    Returns:
        This function creates a word cloud unique to FOX data, and the larger
        the words are, the more prevalent they are in terms on the frequency.
    """

    # Unpacking the tuple:
    _ ,fox_count = word_count()

    # Creating the word cloud:
    wordcloud_fox = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(fox_count)
    fig = px.imshow(wordcloud_fox, title="Fox Word Cloud")
    fig.update_layout(title_font_size=30)

    # Return statement:
    return fig


### BELOW IS THE SETUP CODE FOR DASH ###


cnn_wordcloud = plot_wordcloud_cnn()
fox_wordcloud = plot_wordcloud_fox()
plot_month_year = plot_month_year()
plot_sentiment = plot_sentiment()

app.layout = dbc.Container([
    html.Br(),

    dbc.Row(html.H1("Coverage of January 6th by News Source")),
        # style = header_style
        # justify = "center"),

    html.Br(),

    dbc.Row(dcc.Graph(id = "cnn_wordcloud", 
                      figure = cnn_wordcloud)),

    dbc.Row(dcc.Graph(id = "fox_wordcloud", 
                      figure = fox_wordcloud)),

    dbc.Row(dcc.Graph(id = "multiple line chart", 
                      figure = plot_month_year)),

    dbc.Row(dcc.Graph(id = "multiple bar chart", 
                      figure = plot_sentiment))],


fluid = True, style = {'backgroundColor': "#D2E5D0"})

if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = 7991)