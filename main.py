import telebot
from extensions import CryptoConverter, ConvertionException
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Для начала работы введите команду в следующем формате:\n\
<имя крипто валюты> <имя валюты> <количество валюты>\n\
Cписок доступных крипто символов /source\n\
Cписок валют /currency')


@bot.message_handler(commands=['source', 'currency'])
def help(message: telebot.types.Message):
    text = f'Список доступных символов:\n'
    text += CryptoConverter.get_source() if message.text == '/source' else CryptoConverter.get_currency()
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.upper().split(' ')
        if len(value) != 3:
            raise ConvertionException(f'Не верное количество параметров.\nПример использования: btc rub 1.5')
        source, base, amount = value
        total_base = CryptoConverter.convert(source, base, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации.\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Общая ошибка.\n{e}')
    else:
        text = f'Цена {amount} {base} в {source} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
