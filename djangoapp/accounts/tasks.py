from celery import shared_task
from .utils import divar_scraper
from .models import Home,User

@shared_task
def main_bongah_task():
   # 1- get all new home
   array_of_homes = divar_scraper()
   print("all the homes are taken")
   # 2-save the new ones (not existing)
   for home in array_of_homes:
      if not Home.objects.filter(title=home['title']).exists():
            new_home=Home(**home)
            new_home.save()
            print("one home is saved in db")
      # 3-get all users
      users = User.objects.all()
      # 4-send each user the home with the keyword or neighborhood they want with telegram bot
      for user in users:
            # check if this homes title or address is in the user searchwords.word
            user_searchwords = user.search_words.all()
            for word in user_searchwords:
                  if home['title'] in word.word or home['address'] in word.word:
                        # send the home to the user
                        print(home,user)
   return 'done'   


@shared_task
def home_deleter():
      """ delete 4 oldest home in database if exists """
      if Home.objects.all().count() > 4:
            homes=Home.objects.order_by('id')[:4]
            for home in homes:
                  home.delete()


      else:
            return 'not done'

