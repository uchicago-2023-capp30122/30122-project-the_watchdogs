[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9910330&assignment_repo_type=AssignmentRepo)

<h1>the_watchdogs</h1>

Critical to a functioning democracy, the job of the free press is to force the government to be accountable to whom it governs; a role commonly referred to as, watchdogs. However, as the modes of media consumption evolve, and American citizens become as polarized as ever, trust in national news media is declining. Coverage of the January 6th insurrection at the capitol and the events to follow made this issue glaring. There is even disagreement among the use of the word “insurrection” itself. Through the process of data scraping, we will gather articles that discuss the attack at the Capitol, the January 6th House Committee, and the trials of rioters, from the two of the most visited national news websites: CNN and FOX News. We will then use token analysis to inspect the language used to describe this polarizing topic, and compare it across media sources, and over time. Finally, a data visualization component will be implemented allowing users to further examine our data, through the option of isolating variables, times, and topics.

## Getting Started with the Virtual Environment

1. Clone this repository.
2. From the root directory, ``the_watchdogs``, run ``poetry install``.
3. Run ``poetry shell``.

## Part 1: Gathering the Data

In order to analyze coverage of the January 6th insurrection at the Capitol, article data from NYT, CNN, and FOX must be gathered through the use of web scraping and/or an API. This process can take several minutes to run, so we have saved the json files down in the ``data`` directory. 

If you would like to run the scraper yourself, the code for completeing this can be found in each source's respective directory: ``the_watchdogs/cnn/scrape_cnn.py``, and ``the_watchdogs/fox/scrape_fox.py``, and each of these sources can be scraped individually in the interpreter by running the following:

``$ python3 -m the_watchdogs.cnn.scrape_cnn``

``$ python3 -m the_watchdogs.fox.scrape_fox``

or all at once:

``$ python3 -m the_watchdogs.scrape_sources``


## Part 2: Token and Sentiment Analysis

To transform the raw data scraped from articles on Fox and CNN into a useable cleaned format run the following:

``$ python3 the_watchdogs/preprocess.py data/fox_articles.json``


``$ python3 the_watchdogs/preprocess.py data/cnn_articles.json``

This creates two respective dataframes of cleaned data for each news source in the the data folder in the_watchdogs folder.

## Part 3: Data Visualization

To visualize the analyzed data, please run the following command:

``$ python3 -m the_watchdogs.data_viz.plot``

This will open a port (7991) on the Flask app, and you will be able to see three plots:

1. Two word clouds, one with CNN data, and one with FOX data. 
2. A line graph showing the number of articles by source, and you can toggle the year.
3. A bar graph showing the sentiments (5 categories) by news source. 
