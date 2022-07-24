from re import A
from bs4 import BeautifulSoup
import pandas as pd
import requests
from .models import AppTokens
from .models import Home

cookies = {
    'token': AppTokens.objects.all().first().token
}


def get_url_with_bs4(url):
    page = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


url_of_all_new_personal_home_in_tehran = 'https://divar.ir/s/tehran/real-estate?user_type=personal'


def divar_scraper():
    array_of_homes = []
    response = get_url_with_bs4(url_of_all_new_personal_home_in_tehran)

    cards = response.select('.kt-col-xxl-4')

    for card in cards:
        # select the title of the card
        title = card.select('.kt-post-card__title')[0].getText()
        # select the price of the card
        # if home with this title is in database, skip it
        if Home.objects.filter(title=title).exists():
            continue

        try:
            price = card.select('.kt-post-card__description')[0].getText()
        except:
            price = ''

        # select the address of the card
            # select the address of the card

        try:
            address = card.select(
                '.kt-post-card__bottom-description')[0].getText().split(' ')
            index_of_dar = address.index('در')+1
            # join the word that index is index_of_dar
            address = ' '.join(address[index_of_dar:])
        except:
            address = ''

        try:

            # select link of the card
            link = 'https://divar.ir' + card.select('a')[0].get('href')

            # get the page of link with bs4
            detail_page = get_url_with_bs4(link)
        except:
            link = ''
            print('link is not found')
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
        home = {'title': title,
                'price': price,
                'address': address,
                'link': link,
                'description': description,
                'year': year,
                'rooms': rooms,
                'area': area,
                'floor': floor,
                'anbari': anbari,
                'parking': parking,
                'elevator': elevator,
                'price_per_meter': price_per_meter,
                'total_price': total_price,
                'type_of_sell': type_of_sell,
                'main_type': main_type,
                'sub_type': sub_type,
                'contact': contact}
        array_of_homes.append(home)
        print('home is added')
        
    return array_of_homes




def return_telegram_doc(home):
    title=home['title'] + '\n'

    description=home['description']+ '\n'
    
    price=home['price']+ '\n'
    
    address=home['address'] 
    if address is not '':
        address="🏡"+'adress: ' +  '#'+address.replace(' ','_')+ '\n'
    
    link= "link divar: " + home['link'] 
    
    year=home['year']
    if year is not '':
        year="sal sakht: " +year+ '\n'
    
    rooms=home['rooms']
    if rooms is not '':
        rooms="🏠"+"otag: " +rooms.replace(' ','_')+ '\n'
    
    area=home['area']
    if area is not '':
        area="📐"+"masahat: " +area+ '\n'

    floor=home['floor']
    if floor is not '':
        floor="tabaqe: " + '#'+floor.replace(' ','_')+ '\n'

    anbari=home['anbari']
    if anbari is not '':
        anbari="anbari: " + '#'+anbari.replace(' ','_')+ '\n'

    parking=home['parking']
    if parking is not '':
        parking="🅿"+ "parking: " + '#'+parking.replace(' ','_')+ '\n'

    elevator=home['elevator']
    if elevator is not '':
        elevator="asansor: " + '#'+elevator.replace(' ','_')+ '\n'


    price_per_meter=home['price_per_meter']
    if price_per_meter is not '':
        price_per_meter="qeymat har metr: " + price_per_meter+ '\n'
    

    total_price=home['total_price']
    if total_price is not '':
        total_price="💲"+"qeymat kol: " +total_price+ '\n'
    
    
    type_of_sell=home['type_of_sell']
    if type_of_sell is not '':
        type_of_sell= '#'+type_of_sell.replace(' ','_')+ '\n'

    main_type=home['main_type']
    if main_type is not '':
        main_type= '#'+main_type.replace(' ','_')+ '\n'

    sub_type=home['sub_type']
    if sub_type is not '':
        sub_type= '#'+sub_type.replace(' ','_')+ '\n'

    contact=home['contact']
    if contact is not '':
        contact= "📞" +'shomare tamsa: '+contact.replace(' ','_')+ '\n'

    return f"""
{title}{description}{price}{address}{year}{rooms}{area}{floor}{parking}{anbari}{elevator}{price_per_meter}{total_price}{type_of_sell}{main_type}{sub_type}{contact}{link}

    """











