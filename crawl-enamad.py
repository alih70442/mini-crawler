import json
import requests
from db import init, insert, fetch, clear_type, DB_TYPE_ENAMAD_SITE, DB_TYPE_TAPIN_PODRO_SITE, fetch_custom_sql, export_xlsx, clear_type
from bs4 import BeautifulSoup

# is_wp -> contains wp-
# tapin plugin -> site_url/wp-content/plugins/persian-woocommerce-shipping/assets/js/pws.js
# podro plugin -> site_url/wp-content/plugins/podro-wp/assets/js/disable-podro.js
# PWA -> contains rel="manifest"

init()

def crawl():

    def find_last_page():
        return int(len(fetch(0)) / 30 + 1);

    page_number = find_last_page()
    
    print(f"start page:  {page_number}")
    
    while (1):
        page_number += 1

        page_url = f"https://enamad.ir/DomainListForMIMT/Index/{page_number}"

        html = requests.get(page_url, timeout=10).text

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

            insert(json.dumps(site_data), DB_TYPE_ENAMAD_SITE)
            
        print(f"page {page_number} crawled")

def crawl_site_types():
    
    def find_last_site_index():
        last_record = fetch_custom_sql(f"select * from crawls where type = {DB_TYPE_TAPIN_PODRO_SITE} order by id desc limit 1");
        
        if not len(last_record):
            return fetch_custom_sql(f"select * from crawls where type = {DB_TYPE_ENAMAD_SITE} limit 1")[0][0]
        
        last_site_url = json.loads(last_record[0][1])[0]
        last_site_url = last_site_url.replace('http://', '')
        last_site_url = last_site_url.replace('https://', '')

        enamad_record = fetch_custom_sql(f"select * from crawls where type = {DB_TYPE_ENAMAD_SITE} and value like '%{last_site_url}%' limit 1")
        
        return enamad_record[0][0];
    
    sites = fetch_custom_sql(f"select * from crawls where type = {DB_TYPE_ENAMAD_SITE} and id > {find_last_site_index()}")
    sites_count = len(sites)
    counter = 1;
    
    for site_obj in sites:
        site_url = json.loads(site_obj[1])[0].replace('http://', 'https://')
        
        # [site_url, is_wp, is_tapin, is_podro, is_pwa]
        result = [site_url, False, False, False, False]
        
        # check wp
        try:
            response = requests.get(site_url, timeout=10)
            response.raise_for_status() 
            
            if response.status_code == 200:
                
                # check pwa
                soup = BeautifulSoup(response.text, features='lxml')
                manifest_link = soup.select_one('link[rel="manifest"]')
                if manifest_link:
                    result[4] = True
                    
                # check wp
                if "wp-" in response.text:
                    result[1] = True
                    
                    # check tapin
                    page_url = f"{site_url}/wp-content/plugins/persian-woocommerce-shipping/assets/js/pws.js"

                    try:
                        response = requests.get(page_url, timeout=10)
                        response.raise_for_status() 
                        
                        if response.status_code == 200 and "pws_selectWoo" in response.text:
                            result[2] = True
                    except requests.exceptions.RequestException as e:
                        print(F"{counter}/{sites_count} => Tapin Failed")

                        
                    # check podro
                    page_url = f"{site_url}/wp-content/plugins/podro-wp/assets/js/disable-podro.js"

                    try:
                        response = requests.get(page_url, timeout=10)
                        response.raise_for_status() 
                        
                        if response.status_code == 200 and "is_this_podro_city" in response.text:
                            result[3] = True
                    except requests.exceptions.RequestException as e:
                        print(F"{counter}/{sites_count} => Podro Failed")
                    
        except requests.exceptions.RequestException as e:
            print(F"{counter}/{sites_count} => WP Failed")

        insert(json.dumps(result), DB_TYPE_TAPIN_PODRO_SITE)
            
        print(F"{counter}/{sites_count} => {result}")
        
        counter += 1

# crawl_site_types()
export_xlsx(DB_TYPE_TAPIN_PODRO_SITE)
# clear_type(1)