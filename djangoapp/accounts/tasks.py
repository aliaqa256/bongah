from celery import shared_task

from .utils import divar_scraper

from .models import Home, User
from .robot import send_homes


@shared_task
def main_bongah_task():

    # 1- get all new home
    array_of_homes = divar_scraper()
    print("all the homes are taken")

    for home in array_of_homes:
        if not Home.objects.filter(title=home['title']).exists():
            new_home = Home(**home)
            new_home.save()
            print("one home is saved in db")
                                                    # days left > 0
        users = User.objects.filter(active=True, days_left__gt=0)
        for user in users:
            user_searchwords = user.search_words.all()
            for word in user_searchwords:
                  if  word.word in home['title'] or word.word  in home['address'] :
                        send_homes(
                        int(user.username), 
f"""
{home['title']}
{home['description']}
{home['price']}  
address: #{home['address']}
sale sakht :  #{home['year']} 
otagh:   #{home['rooms']}    
tabaqe: #{home['floor']}   
parking : #{home['parking']} 
asansor: #{home['elevator']}  
qeymat har metr: {home['price_per_meter']}  
qyemat kol: {home['total_price']} 
shomare tamas:{home['contact']}   
#{home['type_of_sell']}
#{home['main_type']}
#{home['sub_type']} 
link divar :{home['link']}
"""


                               )

        return 'done'


@shared_task
def home_deleter():
    """ delete 4 oldest home in database if exists """
    if Home.objects.all().count() > 4:
        homes = Home.objects.order_by('id')[:4]
        for home in homes:
            home.delete()

    else:
        return 'not done'


@shared_task
def reduceUserDaysLeft():
    users = User.objects.filter(days_left__gt=0)
    for user in users:
        user.days_left = user.days_left - 1
        user.save()
