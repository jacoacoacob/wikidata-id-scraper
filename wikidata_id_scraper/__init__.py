import os
import csv
import requests
import json


def get_wikipedia_urls():
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


def main():
    urls = get_wikipedia_urls()
    print(json.dumps(urls[:10], indent=1))

