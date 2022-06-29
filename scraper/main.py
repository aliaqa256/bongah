from math import dist
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import requests




url_of_all_new_personal_home_in_tehran='https://divar.ir/s/tehran/real-estate?user_type=personal'

# get the url with bs4
def get_url_with_bs4(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

response = get_url_with_bs4(url_of_all_new_personal_home_in_tehran)


# select all items with .kt-post-card--outlined class
cards = response.select('.kt-post-card--outlined')

for card in cards:
    array_of_data=[]
    # select the title of the card
    title = card.select('.kt-post-card__title')[0].getText()
    # select the price of the card
    try:
        price = card.select('.kt-post-card__description')[0].getText()
    except:
        price = '0'

    # select the address of the card
    address = card.select('.kt-post-card__bottom-description')[0].getText().split(' ')[-1]

    # select link of the card
    link = 'https://divar.ir'+card.get('href')

    # get the page of link with bs4
    detail_page = get_url_with_bs4(link)

    try:
        description = detail_page.select('.kt-description-row .kt-base-row__start')[0].getText()
    except:
        description = ''

    try:
        year = detail_page.select(
            '.kt-group-row-item--info-row:nth-child(2) .kt-group-row-item__value')[0].getText()
        if len(year) == 4:
            year = year
        else:
            year = ''
    except:
        year = ''
    
    try:
        rooms = detail_page.select(
            '.kt-group-row-item--info-row~ .kt-group-row-item--info-row+ .kt-group-row-item--info-row .kt-group-row-item__value')[0].getText()

        if int(rooms) > 5:
            rooms = ''

    except:
        rooms = ''
    
  
   
    try:
        area = detail_page.select(
            '.kt-group-row-item--info-row:nth-child(1) .kt-group-row-item__value')[0].getText()
        if int(area) > 1300 or int(area) < 10:
            area = ''
    except:
        area = ''

 




























