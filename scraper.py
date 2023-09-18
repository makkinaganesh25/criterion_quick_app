from bs4 import BeautifulSoup
import requests
import pandas as pd
from utils import *
import re

HOME_URL = "https://www.criterion.com/shop/browse/list?sort=spine_number"
EXPORT_FILE_NAME = "criterion_export.csv"

def main():
    response = requests.get(HOME_URL)

    soup = BeautifulSoup(response.content)
    entries = scrape_main_page(soup)


    headers = []
    table = soup.find('thead')
    for header in table.find_all('th'):
        headers.append(header.get('class')[0])

    movie_data = pd.DataFrame(entries, columns=headers + ['child-link'])

    urls = movie_data['child-link'].tolist()
    feature_set = []
    for i, url in enumerate(urls):
        print(i)
        response = requests.get(url)
        soup = BeautifulSoup(response.content)

        media = get_purchase_options(soup)
        collections = get_collections(soup)
        streaming = get_streaming(soup)

        Dict = MergeDicts(media, collections, streaming)
        feature_set.append(Dict)

    availability_data = pd.DataFrame(feature_set)
    availability_data.reset_index(inplace=True, drop=True)

    joined = movie_data.join(availability_data)
    joined['collections'] = [[ai + f' ({bi})' for ai,bi in zip(a,b)] for a,b in joined[['cset_names', 'cset_stock']].to_numpy()]
    joined['formats'] = [[ai + f' ({bi})' for ai,bi in zip(a,b)] for a,b in joined[['items', 'prices']].to_numpy()]

    joined = joined[['g-spine', 'g-title', 'g-director', 'g-year', 'formats', 'collections', 'on_channel', 'items', 'prices']]

    all_items = joined['items'].drop_duplicates().tolist()
    formats = set([item for sublist in all_items for item in sublist])

    for format in formats:
        joined[format] = joined.apply(lambda row: row['prices'][row['items'].index(format)] if format in row['items'] else None, axis = 1)

    final = joined[['g-spine', 'g-title', 'g-director', 'g-year'] + list(formats) + ['collections', 'on_channel']]

    final = final.rename(columns={
        'g-spine': 'Spine #',
        'g-title': 'Title',
        'g-director': 'Director',
        'g-year': 'Year',
        'on_channel': 'On Criterion Channel',
        'collections': 'Collectors Sets'
    })

    final.to_csv(EXPORT_FILE_NAME, index=False)

    return None


if __name__ == "__main__":
    main()

