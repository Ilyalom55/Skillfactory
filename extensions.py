import requests
import json
from config import keys


class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.\nСписок доступных валют:/values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.\nСписок доступных валют:/values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException (f'Не удалось обработать количество {amount}')

        url = (f'https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}&from={quote_ticker}&amount={amount}')
        payload = {}
        headers = {
            'apikey':'nOMyBUcpY6QcOLSd9c9G5ve812xWuiMW'
        }
        response = requests.request('GET', url, headers=headers, data=payload)
        result = response.content
        total_base = json.loads(result)
        last_price = total_base.get('result')

        return last_price