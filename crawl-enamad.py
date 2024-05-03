import json
import requests
from db import init, insert, fetch
from bs4 import BeautifulSoup

# type = 0
# persian-woocommerce-shipping
# podro-wp
# site is WP if there is wp- in it
# tapin plugin -> site_url/wp-content/plugins/persian-woocommerce-shipping/assets/js/pws.js
# tapin plugin -> site_url/wp-content/plugins/podro-wp/assets/js/disable-podro.js

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
    
    sites_rows = soup.select('#Div_Content>.row')

    if not len(sites_rows):
        print('finished')

    for row in sites_rows:
        site_link = row.select_one('div:nth-of-type(2) .exlink')['href']
        site_name = row.select_one('div:nth-of-type(3)').decode_contents()
        site_province = row.select_one('div:nth-of-type(4)').decode_contents()
        site_city = row.select_one('div:nth-of-type(5)').decode_contents()
        site_created_at = row.select_one('div:nth-of-type(7)').decode_contents()
        site_expire_at = row.select_one('div:nth-of-type(8)').decode_contents()

        site_data = [
            site_link,
            site_name,
            site_province,
            site_city,
            site_created_at,
            site_expire_at,
        ]

        insert(json.dumps(site_data), 0)
        
    print(f"page {page_number} crawled")
