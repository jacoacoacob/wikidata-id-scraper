import os
import csv
import requests
import re
from typing import List


HTML_DIR = os.path.abspath("html")


def get_author_html_path(author: dict):
    return f"{HTML_DIR}/{author.get('author_name')}.html"


def get_author_names_and_urls() -> List[dict]:
    data_file_path = os.getenv("CSV_DATA")

    if not data_file_path:
        raise Exception("CSV_DATA environent variable not defined!")
    
    data_file_path = os.path.abspath(data_file_path)

    with open(data_file_path, "r") as csv_file:
        urls = []
        for row in csv.DictReader(csv_file):
            author_name = row.get("author_name")
            formatted_name = author_name.replace(" ", "_")
            urls.append({
                "author_name": author_name,
                "url": f"https://en.wikipedia.org/wiki/{formatted_name}"
            })
            
    return urls


def fetch_wikipedia_pages():
    if not os.path.exists(HTML_DIR):
        os.mkdir(HTML_DIR)

    authors = get_author_names_and_urls()

    for index, author in enumerate(authors):
        print(f"fetching {index + 1} of {len(authors)}")
        url = author.get("url")
        response = requests.get(url)
        with open(get_author_html_path(author), "w") as f:
            f.write(response.text)


def get_wikidata_ids():
    authors = get_author_names_and_urls()

    authors_and_wikidata_ids = []

    for author in authors:
        with open(get_author_html_path(author), "r") as f:
            html = f.read()

        match = re.search(r"Special:EntityPage/(Q\d+)\"", html)

        if match:
            wikidata_id = match.group(1)
            author.update({
                "wikidata_id": wikidata_id,
                "wikidata_url": f"https://www.wikidata.org/wiki/{wikidata_id}"
            })
        else:
            author.update({
                "wikidata_id": None,
                "wikidata_url": None,
            })
        authors_and_wikidata_ids.append(author)
    
    with open("sandbox-results.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=authors_and_wikidata_ids[0].keys())
        writer.writeheader()
        writer.writerows(authors_and_wikidata_ids)
        
    