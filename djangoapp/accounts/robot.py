from calendar import c
import re
import telebot
import requests
from telebot import types

API_TOKEN = '5514637392:AAF1BXO6HGQYR1yuliN6NmAMD2--pfHXd4g'
bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.reply_to(message, """سلام به ربات ما خوش اومدی برای ثبت نام از /register استفاده کن""")
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('/tamdid_eshterak')
    itembtn2 = types.KeyboardButton('/register')
    markup.add(itembtn1, itembtn2)
    bot.send_message(chat_id, "مایل به چه کاری هستید", reply_markup=markup)








@bot.message_handler(commands=['register'])
def register(message):
    # get chat id
    chat_id = message.chat.id
    # get user username
    user_username = message.chat.username
    # register user in django application
    res=requests.post('http://moshaveryar-bot.ir/auth/register/',
                  {'username': chat_id, 'password': chat_id})

    bot.send_message(
        chat_id, f"ثبت نام اولیه شما انجام شد با یوزر نیم {chat_id} لطفا شماره موبایل خود را وارد کنید ")


def is_phone_number(phone_number):
    regex = r'^\+?1?\d{9,15}$'
    return re.match(regex, phone_number.text)
    


@bot.message_handler(commands=['tamdid_eshterak'])
def tamdid_eshterak(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,"لطفا اگر قبلا ثبت نامکرده اید با یوزر نیم و پسورد خود وارد سایت شوید ")
    bot.send_message(chat_id,"http://moshaveryar-bot.ir/auth/login_template")
    bot.send_message(chat_id,f"username:{chat_id} password:{chat_id}") 



@bot.message_handler(func=is_phone_number)
def register_phone(message):
    # get chat id
    chat_id = message.chat.id
    # get user username
    user_username = message.chat.username

    requests.patch('http://moshaveryar-bot.ir/auth/set_phone_number/',{
        "username":chat_id,
        "phone_number":message.text
    })

    bot.send_message(chat_id, """شماره موبایل شما ثبت شد""")
    # send the link for final register for the user
    link_for_final_register = f'http://moshaveryar-bot.ir/auth/login_template/'
    bot.send_message(chat_id, f" یوزر نیم و پسورد شما: {chat_id} لطفا به لینک زیر رفته و ثبت نام خود را کامل کنید")
    bot.send_message(chat_id, link_for_final_register)


def send_homes(chat_id,text):
    try:

        bot.send_message(chat_id, text)
    except :
        print("error in sending home")


if __name__ == "__main__":
    bot.infinity_polling()
