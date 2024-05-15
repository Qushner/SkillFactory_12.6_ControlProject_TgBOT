"""Кушнер С.В. Группа - PDEVPRO-5. Модуль 12. Итоговый проект по ООП "Телеграм-бот" """

import telebot
from config import exchanges, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start_message(message: telebot.types.Message):
    bot.reply_to(message,
                 f"Привет ✌️, {message.chat.username}, введи команду /help, чтобы узнать о принципе работы БОТа")


@bot.message_handler(commands=['help'])
def handle_help_message(message: telebot.types.Message):
    text = 'Для начала работы введите команду БОТу в виде:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> \nПосмотреть доступные для конвертации валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in exchanges.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введено слишком много параметров.')

        base, symbol, amount = values
        sms = Converter.get_price(base, symbol, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, sms)


@bot.message_handler(content_types=['photo'])
def handle_photo(message: telebot.types.Message):
    bot.reply_to(message, "Мы тут валюту переводим, а не фото разглядываем")


@bot.message_handler(content_types=['voice'])
def handle_voice(message: telebot.types.Message):
    bot.reply_to(message, f"У тебя красивый голос ❤️, {message.chat.username}, но давай по делу")


@bot.message_handler(content_types=['documents', 'audio'])
def handle_docs_audio(message):
    pass


bot.polling(none_stop=True)
print()
