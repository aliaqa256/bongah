from math import dist
from this import d
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import etree

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

cookies = {
    # 'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDkzMzg3ODc1MTAiLCJpc3MiOiJhdXRoIiwiaWF0IjoxNjU2NzUxNTUzLCJleHAiOjE2NTgwNDc1NTMsInZlcmlmaWVkX3RpbWUiOjE2NTY3NTE1NTMsInVzZXItdHlwZSI6InBlcnNvbmFsIiwidXNlci10eXBlLWZhIjoiXHUwNjdlXHUwNjQ2XHUwNjQ0IFx1MDYzNFx1MDYyZVx1MDYzNVx1MDZjYyIsInNpZCI6ImYyYzc0ODJmLTljNzUtNGY1Mi1iODRiLTRlOTE0NzAyNmM1OSJ9.f39EMcoDdKeqyq3q5H408zrQilZCBpHA_bmrf2QwXBg',
}

url_of_all_new_personal_home_in_tehran = 'https://divar.ir/s/tehran/real-estate?user_type=personal'



def get_url_with_bs4(url,cookies=None):
    if cookies is None:
        page = requests.get(url, headers=HEADERS)
    else:
        page = requests.get(url, cookies=cookies, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_url_with_lxml(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    dom = etree.HTML(str(soup))
    return dom


cards=get_url_with_lxml(url_of_all_new_personal_home_in_tehran).xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "kt-post-card--has-action", " " ))]')

for card in cards:
    try:
        title = card.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "kt-post-card__title", " " ))]/text()')[0]
    except:
        title = ''

    try:
        price = card.xpath('.//*[contains(concat( " ", @class, " " ), concat( " ", "kt-post-card__description", " " ))]/text()')[0]
    except:
        price = ''
    
    try:
        address = card.xpath(
            './/*[contains(concat( " ", @class, " " ), concat( " ", "kt-post-card__bottom-description", " " ))]/text()')[0].split(' ')
        #get index of 'در'
        index_of_dar = address.index('در')+1
        # join the word that index is index_of_dar
        address = ' '.join(address[index_of_dar:])
    except:
        address = ''

    # try:
    # get the href of the card
    link = card.xpath(
        '//*[@id="app"]/div[1]/main/div[2]/div/div/div[1]/div/a')[0].get('href')
            
    # except:
    #     link = ''

    print(link)
