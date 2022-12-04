import telebot
import json
import requests
from config import keys
class ConvExceptions (Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote:str, base:str, amount: str):
        if quote == base:
            raise ConvExceptions("Нельзя конвертировать одинаковые валюты")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvExceptions (f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvExceptions (f'Не удалось обработать валюту {base}')
        try:
            amount=float(amount)
        except ValueError:
            raise ConvExceptions (f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
