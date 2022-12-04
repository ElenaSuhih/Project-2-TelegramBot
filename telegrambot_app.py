import telebot

from config import keys, TOKEN
from utils import CryptoConverter, ConvExceptions
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = """Для начала работы введите команду в следующем формате: \n <Имя валюты> 
    <В какую валюту перевести> <Кол-во валюты> \n Увидеть список всех доступных валют Вы можете по команде /values"""
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text='\n'.join((text, key, ))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert (message: telebot.types.Message):
   try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvExceptions("Слишком много паремтров")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote,base,amount)
        total_base_num=float(total_base)*float(amount)
   except ConvExceptions as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
   except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
   else:
        text = f'Цена {amount} {quote} в {base} - {total_base_num}'
        bot.send_message(message.chat.id, text)



bot.polling()
