import telebot
from extensions import ConvertionException, CurrencyConverter
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы вычислить сумму, введите команду боту в следующем формате(через пробел): \n<наименование валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидить список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) > 3 or len(values) < 3:
            raise ConvertionException('Неверное количество параметров. Помощь:/help')
        quote, base, amount = message.text.split(' ')
        total_base = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')


    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()