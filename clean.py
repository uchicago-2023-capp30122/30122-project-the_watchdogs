import sys
import json
import pandas as pd
#Download stopwords and punkt if you haven't already
# nltk.download('stopwords')
# nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    clean(sys.argv[1])
