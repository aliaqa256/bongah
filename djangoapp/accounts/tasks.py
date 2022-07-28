from celery import shared_task

from .utils import divar_scraper,return_telegram_doc

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
                  if  word.word  in home['address'] :
                        send_homes(
                        int(user.username),return_telegram_doc(home))

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
    users = User.objects.all()
    for user in users:
        if user.days_left > 0:
            user.days_left = user.days_left - 1
            user.save()
        else:
            send_homes(int(user.username),"""  مشتری گرامی اشتراک شما به پایان رسیده لطفا وارد سایت شوید و اشتراک خود را تمدید کنید """)

