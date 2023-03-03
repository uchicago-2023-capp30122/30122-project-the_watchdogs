[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9910330&assignment_repo_type=AssignmentRepo)

<h1>the_watchdogs</h1>

Critical to a functioning democracy, the job of the free press is to force the government to be accountable to whom it governs; a role commonly referred to as, watchdogs. However, as the modes of media consumption evolve, and American citizens become as polarized as ever, trust in national news media is declining. Coverage of the January 6th insurrection at the capitol and the events to follow made this issue glaring. There is even disagreement among the use of the word “insurrection” itself. Through the process of data scraping, we will gather articles that discuss the attack at the Capitol, the January 6th House Committee, and the trials of rioters, from the three most visited national news websites: The New York Times (NYT), CNN, and FOX News. We will then use token analysis to inspect the language used to describe this polarizing topic, and compare it across media sources, and over time. Finally, a data visualization component will be implemented allowing users to further examine our data, through the option of isolating variables, times, and topics.

## Getting Started with the Virtual Environment

1. Clone this repository.
2. From the root directory, ``the_watchdogs``, run ``poetry install``.
3. Run ``poetry shell``.

## Part 1: Gathering the Data

In order to analyze coverage of the January 6th insurrection at the Capitol, article data from NYT, CNN, and FOX must be gathered through the use of web scraping and/or an API. The code for completeing this can be found in each source's respective directory: ``cnn/scrape_cnn.py``, ``fox/scrape_fox.py``, and ``nyt/scrape_nyt.py``. Each of these sources can be scraped individually in the interpreter by running the following:

``$ python3 -m cnn/scrape_cnn.py``

``$ python3 -m fox/scrape_fox.py``

``$ python3 -m nyt/scrape_nyt.py`` 

or all at once:

``$ python3 -m scrape_sources.py``

This can take a few minutes to run so we have saved the json files down in the ``data`` directory.

## Part 2: Token and Sentiment Analysis

xx

## Part 3: Data Visualization

xx
