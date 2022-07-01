from celery import shared_task
import dateti


@shared_task
def main_bongah_task():
    """   1- get all new home
       2-save the new ones (not existing)
       3-get all users
       4-send each user the home with the keyword or neighborhood they want with telegram bot"""
    pass