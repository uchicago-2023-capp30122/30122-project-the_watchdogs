import sys
import json
import pandas as pd
#Download stopwords, punkt and vader_lexicon if you haven't already
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dateutil import parser


def preprocess(json_file_name):
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
    df['clean_date'] = df['date'].apply(lambda x: parser.parse(x).date())

    # Strip spaces in text and make lowercase
    df.text = df.text.str.strip()
    df.text = df.text.str.lower()

    # Set language for stop words
    stop_words = set(stopwords.words('english'))
    stop_words.extend(['said', 'going', 'would'])

    # Get raw sentiment analysis score
    sid = SentimentIntensityAnalyzer()
    df['sentiment_score'] = df['text'].apply(lambda x: sid.polarity_scores(x)['compound'])

    #Transform score into category based on value
    df['sentiment_category'] = pd.cut(df['sentiment_score'], [-1, -0.6, -0.2, 0.2, 0.6, 1],
                                   labels=['Very Negative', 'Slightly Negative', 
                                           'Neutral','Slightly Positive', 'Very Positive'],
                                            right=True, include_lowest=True)

    # Transform text into tokens
    df['clean_text'] = df.text.apply(lambda x: word_tokenize(x))

    # Remove stop words and all punctuation
    df['clean_text'] = df['clean_text'].apply(lambda x: [word for word in x if word not in stop_words and word.isalpha()])
    
    # Save cleaned text and dataframe to separate files
    source_name = df['source'][0]
    df['clean_text'].to_csv(f'data/{source_name}_corpus.txt', header=None, index=None, sep=' ', mode='a')
    df.to_csv(f'data/{source_name}_clean_df.csv', index=False)

    

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    preprocess(sys.argv[1])
