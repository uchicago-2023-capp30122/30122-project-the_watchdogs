import sys
from cnn.scrape_cnn import cnn_articles_to_json
from fox.scrape_fox import fox_articles_to_json

if __name__ == "__main__":
    """
    Scrape FOX and CNN articles 
    """
    if len(sys.argv) != 1:
        print("Usage: python -m the_watchdogs.scrape_sources")
        sys.exit(1)
    print("Scraping articles...this will take a few minutes.")
    fox_articles_to_json()
    cnn_articles_to_json()
    print("Articles successfully scraped. Output written to data/fox_articles.json and data/cnn_articles.json")
