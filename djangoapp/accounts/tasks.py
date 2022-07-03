from celery import shared_task
from .utils import divar_scraper
from .models import Home,User

@shared_task
def main_bongah_task():
   # 1- get all new home
   array_of_homes = divar_scraper()
   # 2-save the new ones (not existing)
   for home in array_of_homes:
      if not Home.objects.filter(title=home['title']).exists():
            new_home=Home(**home)
            new_home.save()
      # 3-get all users
      users = User.objects.all()
      # 4-send each user the home with the keyword or neighborhood they want with telegram bot
      for user in users:
         homes = Home.objects.filter(
             title__icontains=user.keywords, address__icontains=user.address)

         print(homes, user)


   return 'done'   


