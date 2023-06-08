# Wikidata ID Finder

This project contains code that will read a CSV file containing author names (or the name of anything on Wikipedia) and then scrape Wikipedia for their Wikidata IDs.


## Running locally

This project relies on [Poetry](https://python-poetry.org/docs/) to execute scripts and manage dependencies in a python virtual environment.

1. Clone or download this repo.
2. Inside the project root, run `poetry install` to install dependencies
3. Run 
   ```bash
   CSV_DATA=path/to/author/name/csv poetry run fetch-wikipedia-pages
   ```
   to download the wikipedia pages for all authors. It's a good idea to not run this more than once so that wikipedia doesn't get upset with all your rapid-fire requests.
4. Run
   ```bash
   CSV_DATA=path/to/author/name/csv poetry run get-wikidata-ids
   ```
   This will create a new CSV file called `sandbox-results.csv` in the project root containing the author names, the URL for the page downloaded by `fetch-wikipedia-pages`, and the Wikidata ID found on that page (if present) _and_ the Wikidata URL (again, if ID was found).


> **The code looks for author names in a column called "author_names". If it can't find that column, it won't work.**