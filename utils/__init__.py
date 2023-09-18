from bs4 import BeautifulSoup

def get_purchase_options(soup, **kwargs):
    items = []
    prices = []

    purchase_options = soup.find_all('div', class_ = 'purchase-option')

    for option in purchase_options:
        item = option.find_all('span', class_='item')[0].text.strip()
        items.append(item)

        price = option.find_all('span', class_='item-price')[0].text.strip()
        prices.append(price)
    
    return {'items': items,
            'prices': prices}

def get_collections(soup, **kwargs):
    collectors_sets = soup.find_all('div', class_ = 'collector-set-options-meta')
    cset_names = []
    cset_prices = []
    cset_stock = []
    if collectors_sets:
        for cset in collectors_sets:
            name = cset.find('p', class_='cso-title').text.strip()
            price = cset.find('p', class_='csa-price').text.strip()
            availability_target = cset.find(['span', 'button'])
            if availability_target.text.strip() in ['Add To Cart']:
                availability = 'Available'
            elif availability_target.text.strip() in ['Out Of Print']:
                availability = 'Out of Print'
            else:
                availability = 'Availability Unsure'

            if name:
                cset_names.append(name)
            if price:
                cset_prices.append(price)
            if availability:
                cset_stock.append(availability)

    return {'cset_names': cset_names, 
            'cset_prices': cset_prices, 
            'cset_stock': cset_stock}

def get_streaming(soup):
    on_channel = False
    digital_options = soup.find('div', class_='watchBut_contain')
    if digital_options:
        links = digital_options.find_all('img')
        if links:
            for link in links:
                if 'Criterion Channel' in link.get('alt'):
                    on_channel = True
    
    return {'on_channel': on_channel}

def MergeDicts(*dicts):
    out = {}
    for d in dicts:
        out.update(d)
    return out


def scrape_main_page(soup, **kwargs):
    table_elements = soup.find_all("tr")
    header_elements = table_elements[0]
    headers = [header.get('class')[0] for header in header_elements.find_all('th')]
    headers.append('child-link')

    entries = []

    for i, element in enumerate(table_elements):
        
        entry_data = []
        child_link = element.get('data-href')

        entry = element.find_all('td')
        
        if entry:
            for feature in entry:
                if feature.get('class')[0] in headers:
                    name = feature.text.strip()
                    entry_data.append(name)
                else:
                    continue
            entry_data.append(child_link)
        
        if len(entry_data) != len(headers):
            print(f'Unable to make data at {i}')
            continue
        else:
            entries.append(entry_data)
    
    return entries