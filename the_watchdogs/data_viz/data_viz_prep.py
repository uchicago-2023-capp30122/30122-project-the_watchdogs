# Rohit Kandala (cnet: "rohitk") wrote the code in this file. 

import sys
import pathlib
import pandas as pd
import numpy as np
from collections import Counter

# These functions below take in the csvs that are the csvs that are created
# from "preprocess", and format the csvs so that they're fit to use as Pandas
# data structures in the file "__main__.py" for data visulization. 

# Loading in the data and setting them as global dataframe variables:
cnn_data = pathlib.Path(__file__).parent / "../data/CNN_clean_df.csv"
fox_data = pathlib.Path(__file__).parent / "../data/FOX_clean_df.csv"

df_cnn = pd.read_csv(cnn_data)
df_fox = pd.read_csv(fox_data)


### BELOW ARE THE HELPER FUNCTIONS THAT WILL BE USED FOR DATA VISUALIZATION ###


def word_count():
    """
    Returns:
        This returns the cnn & fox dataframes it as a Pandas series. We have to
        parse through the dataframe in order to count the salient words and
        count the terms. Lastly, it's called when creating the wordcloud 
        visualizations. 
    """

    # Initializing lists to create Pandas dataframes:
    cnn_count = []
    fox_count = []

    # Parsing through the dataframes:
    for val in df_cnn.clean_text.values:
        cnn_count += eval(val)

    for val in df_fox.clean_text.values:
        fox_count += eval(val)

    # Converting the lists to a series, and saving it to a variable:
    cnn_count = pd.Series(Counter(cnn_count)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(fox_count)).sort_values(ascending = False)

    # Return statement:
    return cnn_count, fox_count


def create_date():
    """
    Returns:
        Parses through the dataframe and returns a dataframe that is cleaned,
        parsed, and contains the proper month/year format. This function is
        called in the multiple line chart visualization with the year toggle.
    """

    # Loading in dataframes, spliting up by comma, and saving it to variables:
    text_cnn = df_cnn.date.apply(lambda x: x.split(','))
    text_fox = df_fox.date.apply(lambda x: x.split(','))

    # Parsing through dataframe, and updating the contents of the variables;
    # creating new series based off updated variables: 
    text_cnn = text_cnn.apply(lambda x: (x[0].split(' ')[0], int(x[1][1:5])))
    text_fox = text_fox.apply(lambda x: (x[0].split(' ')[0], int(x[1][1:5])))

    cnn_count = pd.Series(Counter(text_cnn)).reset_index().set_index('level_0')
    fox_count = pd.Series(Counter(text_fox)).reset_index().set_index('level_0')

    # Creating a standerdized months:
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']
    ind_cnn = cnn_count.level_1
    ind_fox = fox_count.level_1
    cnn_count = cnn_count[0]
    fox_count = fox_count[0]
    years = np.union1d(ind_cnn.unique(), ind_fox.unique())

    # Creating year associated with month:
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

    # Updating the list:
    result = pd.concat(res, axis=1)
    result.index.name = 'Date'
    result.reset_index()

    # Return statement:
    return result


def create_sentiment():
    """
    Returns:
        This returns the dataframes as a Pandas series. Like all the other
        helpers, we have to parse through the dataframes. This is called
        when creating the multiple bar chart visualization. 
    """

    # Saving the dataframe values as a variables:
    text_cnn = df_cnn.sentiment_category.values
    text_fox = df_fox.sentiment_category.values

    # Converting dataframe to a series, and saving it as variables:
    cnn_count = pd.Series(Counter(text_cnn)).sort_values(ascending = False)
    fox_count = pd.Series(Counter(text_fox)).sort_values(ascending = False)

    # Return statement:
    return cnn_count, fox_count