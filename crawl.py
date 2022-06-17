import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd
from pprint import pprint


def make_link(href):
    return 'https://www.mashreghnews.ir' + href


def crawl(year: int):

    scraped_data = []

    for month in range(12, 13):
        for day in range(31, 32):
            url_list = []
            page = 1
            while True:
                page += 1

                page_url = f"https://www.mashreghnews.ir/page/archive.xhtml?mn={month}&wide=0&dy={day}&ms=0&pi={page}&yr={year}"

                html = requests.get(page_url).text

                soup = BeautifulSoup(html, features='lxml')

                headers = soup.find_all('h3')

                if len(headers) == 0:
                    break
                if len(url_list) and make_link(headers[0].a['href']) in url_list:
                    break

                for link in tqdm(headers):
                    inner_url = make_link(link.a['href'])

                    url_list.append(inner_url)

                    article = Article(inner_url)
                    try:
                        article.download()
                        article.parse()
                        scraped_data.append({
                            'year': year,
                            'month': month,
                            'day': day,
                            'url': inner_url,
                            'title': article.title,
                            'text': article.text,
                        })
                    except:
                        print(f"failed at {year}/{month}/{day}")

    print(f"{year} finished")

    df = pd.DataFrame(scraped_data)
    df.to_csv(f'records/record.csv')
