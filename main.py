from crawl import crawl
from query import query
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_list():
    print(f"choose:")
    print(f"1. crawl site")
    print(f"2. query phrase")


while True:
    clear()
    print_list()
    try:
        chosen_view = int(input('Input:'))
        if (chosen_view == 1):
            print("site is crawling")
            crawl(1395)
        elif (chosen_view == 2):
            print("site is crawling")
            phrase = input('enter a phrase to query for:')
            query(phrase)
        else:
            print('not allowed')

        input('to leave enter any...')
    except ValueError:
        print("Not a number")
