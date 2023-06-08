import os
import csv
import requests
import re
from typing import List


HTML_DIR = os.path.abspath("html")


def read_author_html(author_name):
    with open(HTML_DIR + "/" + author_name + ".html", "r") as f:
        return f.read()


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
        author_name = author.get("author_name")
        url = author.get("url")
        response = requests.get(url)
        with open(HTML_DIR + "/" + author_name + ".html", "w") as f:
            f.write(response.text)


def get_wikidata_ids():
    authors = get_author_names_and_urls()

    authors_and_wikidata_ids = []

    for author in authors:
        html = read_author_html(author.get("author_name"))
        match = re.search(r"Special:EntityPage/(Q\d+)\"", html)
        if match:
            author.update({ "wikidata_id": match.group(1) })
        else:
            author.update({ "wikidata_id": None })
        authors_and_wikidata_ids.append(author)
    
    with open("sandbox-results.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=authors_and_wikidata_ids[0].keys())
        writer.writeheader()
        writer.writerows(authors_and_wikidata_ids)
        
    