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

        users = User.objects.filter(is_active=True, has_day_left=True)
        for user in users:
            user_searchwords = user.search_words.all()
            for word in user_searchwords:
                  if home['title'] in word.word or home['address'] in word.word:
                        send_homes(
                        int(user.username), f" {home['title']} \n #{home['address']} \n \
                        {home['description']} \n{home['price']} \n {home['year']}\n  {home['rooms']} \n  \
                              {home['floor']} \n {home['parking']} \n {home['elevator']} \n \
                              {home['price_per_meter']}  \n {home['total_price']} \n {home['contact']}  \n #{home['type_of_sell']} \
                              #{home['main_type']} #{home['sub_type']}  {home['link']} ")

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
    users = User.objects.filter(has_day_left=True)
    for user in users:
        user.days_left = user.days_left - 1
        user.save()
