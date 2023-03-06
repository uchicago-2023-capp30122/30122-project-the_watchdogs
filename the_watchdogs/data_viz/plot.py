# Rohit Kandala (cnet: "rohitk") wrote the code in this file. 

import sys
from .data_viz_prep import create_sentiment, create_date, word_count
from .app import app
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

    # Calling in function from data_viz_prep, and concatinating into a dataframe:
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
    fig.update_layout(title={'text': 'Sentiment Analysis by News Source', 'x': 0.5, 'y': 0.9, 'xanchor': 'center', 'yanchor': 'top'},
                      xaxis_title={'text': 'Sentiment', 'standoff': 10},
                      yaxis_title={'text': 'Number of Articles', 'standoff': 10})

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
    fig = px.line(df, x=df.index, y=['CNN 2021', 'CNN 2022', 'CNN 2023', 'FOX 2020', 'FOX 2021', 'FOX 2022', 'FOX 2023'],
                  title='Article Count by Month', line_group="variable", color="variable",
                  color_discrete_map={"CNN 2021": "rgb(204, 0, 0)", "CNN 2022": "rgb(204, 0, 0)", "CNN 2023": "rgb(204, 0, 0)",
                                     "FOX 2021": "rgb(0, 51, 102)", "FOX 2022": "rgb(0, 51, 102)", "FOX 2023": "rgb(0, 51, 102)"})
    fig.update_traces(mode='lines+markers')

    # Adding a toggle by year:
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label='All Years',
                         method='update',
                         args=[{'visible': [True, True, True, False, True, True, True]},
                               {'title': 'Articles by Year',
                                'showlegend': True}]),
                    dict(label='2021',
                         method='update',
                         args=[{'visible': [True, False, False, False, True, False, False]},
                               {'title': 'Articles from 2021',
                                'showlegend': True}]),
                    dict(label='2022',
                         method='update',
                         args=[{'visible': [False, True, False, False, False, True, False]},
                               {'title': 'Articles from 2022',
                                'showlegend': True}]),
                    dict(label='2023',
                         method='update',
                         args=[{'visible': [False, False, True, False, False, False, True]},
                               {'title': 'Articles from 2023',
                                'showlegend': True}]),
                ]),
                direction='left',
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1.0,
                y=1.15
            )
        ]
    )

    # Updating axis labels:
    fig.update_layout(xaxis_title="Month", yaxis_title="Article Count", title_x=0.5)

    # Return statement:
    return fig


def plot_wordcloud_cnn():
    """
    Returns:
        This function creates a word cloud unique to CNN data, and the larger
        the words are, the more prevalent they are in terms on the frequency.
    """

    # Unpacking the tuple from data_viz_prep helper:
    cnn_count, _ = word_count()

    # Creating the word cloud:
    wordcloud_cnn = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(cnn_count)
    fig = px.imshow(wordcloud_cnn, title="CNN Word Cloud")
    fig.update_layout(title_font_size=30, margin=dict(l=0, r=0, t=50, b=0), title=dict(x=0.5, xanchor='center'))

    # Return statement:
    return fig


def plot_wordcloud_fox():
    """
    Returns:
        This function creates a word cloud unique to FOX data, and the larger
        the words are, the more prevalent they are in terms on the frequency.
    """

    # Unpacking the tuple from data_viz_prep helper:
    _ ,fox_count = word_count()

    # Creating the word cloud:
    wordcloud_fox = WordCloud(width=1000, height=500, background_color='white').generate_from_frequencies(fox_count)
    fig = px.imshow(wordcloud_fox, title="FOX Word Cloud")
    fig.update_layout(title_font_size=30, margin=dict(l=0, r=0, t=50, b=0), title=dict(x=0.5, xanchor='center'))

    # Return statement:
    return fig


### BELOW IS THE SETUP CODE FOR DASH ###


cnn_wordcloud = plot_wordcloud_cnn()
fox_wordcloud = plot_wordcloud_fox()
plot_month_year = plot_month_year()
plot_sentiment = plot_sentiment()

app = Dash(external_stylesheets = [dbc.themes.SIMPLEX])
app.layout = dbc.Container([

    html.Br(),

    dbc.Row(html.H1("Coverage of January 6th by News Source"), justify='center'),

    html.Br(),

    dbc.Row([
        dbc.Col(dcc.Graph(id="cnn_wordcloud", figure=cnn_wordcloud)),
        dbc.Col(dcc.Graph(id="fox_wordcloud", figure=fox_wordcloud))
    ]),

    dbc.Row(dcc.Graph(id="multiple line chart", figure=plot_month_year)),

    dbc.Row(dcc.Graph(id="multiple bar chart", figure=plot_sentiment)),

    dbc.Row("Sources: CNN and Fox News Websites"),

], fluid=True, style={'text-align': 'center'})

# Main statement below:

if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = 7991)