from math import dist
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import requests

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

cookies = {
    'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMDkzMzg3ODc1MTAiLCJpc3MiOiJhdXRoIiwiaWF0IjoxNjU2NzUxNTUzLCJleHAiOjE2NTgwNDc1NTMsInZlcmlmaWVkX3RpbWUiOjE2NTY3NTE1NTMsInVzZXItdHlwZSI6InBlcnNvbmFsIiwidXNlci10eXBlLWZhIjoiXHUwNjdlXHUwNjQ2XHUwNjQ0IFx1MDYzNFx1MDYyZVx1MDYzNVx1MDZjYyIsInNpZCI6ImYyYzc0ODJmLTljNzUtNGY1Mi1iODRiLTRlOTE0NzAyNmM1OSJ9.f39EMcoDdKeqyq3q5H408zrQilZCBpHA_bmrf2QwXBg',
}

url_of_all_new_personal_home_in_tehran = 'https://divar.ir/s/tehran/real-estate?user_type=personal'


def get_url_with_bs4(url,cookies=None):
    if cookies is None:
        page = requests.get(url, headers=HEADERS)
    else:
        page = requests.get(url, cookies=cookies, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup



response = get_url_with_bs4(url_of_all_new_personal_home_in_tehran)

cards = response.select('.kt-col-xxl-4')

main_array = []

for card in cards:
    array_of_data = []
    # select the title of the card
    title = card.select('.kt-post-card__title')[0].getText()
    # select the price of the card
    try:
        price = card.select('.kt-post-card__description')[0].getText()
    except:
        price = '0'

    # select the address of the card
    address = card.select(
        '.kt-post-card__bottom-description')[0].getText().split(' ')
    index_of_dar = address.index('در')+1
    # join the word that index is index_of_dar
    address = ' '.join(address[index_of_dar:])

    # select link of the card
    link = 'https://divar.ir'+ card.select('a')[0].get('href')

    # get the page of link with bs4
    detail_page = get_url_with_bs4(link)

    try:
        description = detail_page.select(
            '.kt-description-row .kt-base-row__start')[0].getText()
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

    try:
        floor = detail_page.select(
            '.kt-unexpandable-row:nth-child(13)')[0].getText()

        if not 'طبقه' in floor:
            floor = ''

    except:
        floor = ''

    try:
        anbari = detail_page.select(
            '.kt-icon-cabinet+ .kt-body--stable')[0].getText()
        if not 'انبار' in anbari:
            anbari = ''
    except:
        anbari = ''

    try:
        parking = detail_page.select(
            '.kt-icon-parking+ .kt-body--stable')[0].getText()
        if not 'پارکینگ' in parking:
            parking = ''
    except:
        parking = ''

    try:
        elevator = detail_page.select(
            '.kt-icon-elevator+ .kt-body--stable')[0].getText()
        if not 'آسانسور' in elevator:
            elevator = ''
    except:
        elevator = ''

    try:
        price_per_meter = detail_page.select(
            '.kt-unexpandable-row:nth-child(5)')[0].getText()
        if not 'قیمت هر متر' in price_per_meter:
            price_per_meter = ''

    except:
        price_per_meter = ''

    try:
        total_price = detail_page.select(
            '.kt-unexpandable-row:nth-child(3)')[0].getText()
        if not 'قیمت کل' in total_price:
            total_price = ''
    except:
        total_price = ''

    if 'اجاره' in price or 'ودیعه' in price:
        type_of_sell = 'rent'
    else:
        type_of_sell = 'sell'

    try:
        main_type = detail_page.select(
            '.kt-breadcrumbs__item:nth-child(2) .kt-breadcrumbs__link')[0].getText()
    except:
        main_type = ''

    try:
        sub_type = detail_page.select(
            '.kt-breadcrumbs__item~ .kt-breadcrumbs__item+ .kt-breadcrumbs__item a')[0].getText()
    except:
        sub_type = ''

    token_in_the_url = link.split('/')[-1]
    try:
        contact = requests.get(
            f'https://api.divar.ir/v5/posts/{token_in_the_url}/contact/', cookies=cookies).json()['widgets']['contact']['phone']
    except:
        contact = ''
    array_of_data.append(title)
    array_of_data.append(price)
    array_of_data.append(address)
    array_of_data.append(link)
    array_of_data.append(description)
    array_of_data.append(year)
    array_of_data.append(rooms)
    array_of_data.append(area)
    array_of_data.append(floor)
    array_of_data.append(anbari)
    array_of_data.append(parking)
    array_of_data.append(elevator)
    array_of_data.append(price_per_meter)
    array_of_data.append(total_price)
    array_of_data.append(type_of_sell)
    array_of_data.append(main_type)
    array_of_data.append(sub_type)
    array_of_data.append(contact)

    print('.', 'one home is done')

    main_array.append(array_of_data)


print('creating data frame............')
# creaete dataframe from the main array
df = pd.DataFrame(main_array, columns=['title', 'price', 'address', 'link', 'description', 'year', 'rooms', 'area',
                  'floor', 'anbari', 'parking', 'elevator', 'price_per_meter', 'total_price', 'type_of_sell', 'main_type', 'sub_type', 'contact'])

print("creating excel file............")
# create excel file from the dataframe
df.to_excel('divar.xlsx')
