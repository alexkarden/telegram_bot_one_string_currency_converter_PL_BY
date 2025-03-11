import configparser
import telebot
import requests
import json

config = configparser.ConfigParser()
config.read("settings.ini")
url_cur = config["telegrambot"]["urlcur"]
bot = telebot.TeleBot(config["telegrambot"]["token"])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Однострочный конвертер валют 🇵🇱PLN/BYN🇧🇾.\nВведите сумму.')

@bot.message_handler(content_types=['animation', 'audio', 'document', 'photo', 'sticker', 'story', 'video', 'video_note', 'voice', 'contact', 'dice', 'game', 'poll', 'venue', 'location', 'invoice', 'successful_payment', 'connected_website', 'passport_data', 'web_app_data'])
def start(message):
    bot.send_message(message.chat.id, 'Бот работает только с текстовыми сообщениями.\nВведите сумму.')

@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.from_user.id, ' <b>Скрипт написал Alex Karden -</b> github.com/alexkarden\n\nВведите сумму.', parse_mode='html')

@bot.message_handler(commands=['help'])
def about(message):
    bot.send_message(message.from_user.id, ' <b>Помощь</b>\nЧасто бывает, находясь за границей, при просмотре цен на товары, которые хотите привезти к себе домой, непонятно выгодная ли цена или нет. Для понимания люди начинают открывать конвертеры валют и расчитывать цену в своей валюте, тратя на это время и мобильный трафик. Этот бот сразу же готов к работе и потребляем минимум трафика.\n\nБот забирает данные с сайта nbrb.by по api сразу же как вы введете сумму. Для работы необходимо подключение к сети интернет.\n\nПросто введите сумму в польских злотых и бот сразу же сконвертирует её в белорусские рубли.', parse_mode='html')



@bot.message_handler(content_types=['text'])
def summa(message):
    try:
        amount = float(message.text.strip().replace(',', '.'))
    except Exception:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму.')
        return

    if amount > 0:
        try:
            r_cur = requests.get(url_cur)
            obj_cur = json.loads(r_cur.text)
            s = round(amount * obj_cur["Cur_OfficialRate"] / 10, 2)
        except Exception:
            bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз. Введите сумму')
            return
        bot.send_message(message.chat.id, f'<b>{s} BYN</b>\nМожете заново ввести сумму.', parse_mode='html')

    else:
        bot.send_message(message.chat.id, 'Число должно быть больше за 0. Введите сумму.')

bot.polling(none_stop=True)
