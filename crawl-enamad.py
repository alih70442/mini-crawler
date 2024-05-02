import requests
from db import init, insert, fetch
from bs4 import BeautifulSoup

# type = 0

init()

def find_last_page():
    return int(len(fetch(0)) / 30 + 1);

page_number = find_last_page()

print(f"start page:  {page_number}")
    
while (1):
    page_number += 1
    
    page_url = f"https://enamad.ir/DomainListForMIMT/Index/{page_number}"

    html = requests.get(page_url).text

    soup = BeautifulSoup(html, features='lxml')

    sites_tags = soup.select('#Div_Content>.row div:nth-of-type(2) .exlink')

    if not len(sites_tags):
        print('finished')

    for tag in sites_tags:
        insert(tag['href'], 0)
        
    print(f"page {page_number} crawled")
