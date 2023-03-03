import sys
import json
import pandas as pd
#Download stopwords and punkt if you haven't already
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime


def clean(json_file_name):
    """
    Preprocesses and cleans the article text from JSON and saves it into a text 
    file for analysis. 

    Parameters:
            json_file_name: JSON file with the scraped articles
            
    Returns:
            Saves output to text file in data folder

    """
    # Load scraped articles from publication
    with open(json_file_name, 'r') as f:
        data = json.load(f)

    # Load data into dataframe
    df = pd.DataFrame(data)

    # Transform dates into useable format
    df[['clean_date','time']] = df['date'].str.split("T",expand=True)
    df['clean_date'] = df['clean_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))

    # Strip spaces in text and make lowercase
    df.text = df.text.str.strip()
    df.text = df.text.str.lower()

    # Set language for stop words
    stop_words = set(stopwords.words('english'))

    # Transform text into tokens
    df['clean_text'] = df.text.apply(lambda x: word_tokenize(x))

    # Remove stop words and all punctuation
    df['clean_text'] = df['clean_text'].apply(lambda x: [word for word in x if word not in stop_words and word.isalpha()])
    
    # Save cleaned text to file
    source_name = df['source'][0]
    df['clean_text'].to_csv(f'data/{source_name}_corpus.txt', header=None, index=None, sep=' ', mode='a')

    return df


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    clean(sys.argv[1])
