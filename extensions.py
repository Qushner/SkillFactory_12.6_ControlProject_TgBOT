import requests
import json
from config import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, symbol: str, amount: str):
        if base == symbol:
            raise APIException(f'Невозможно перевести одинаковые валюты ({base}).')

        try:
            base_ticker = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}".')

        try:
            symbol_ticker = exchanges[symbol.lower()]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {symbol}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты "{amount}"')

        url = f'https://api.apilayer.com/exchangerates_data/convert?to={symbol_ticker}&from={base_ticker}&amount={amount}'
        headers = {"apikey": "Tg7fmWA7OiiAtyMOHOw8HPao1fC6UKUH"}
        r = requests.get(url, headers=headers)
        result = json.loads(r.content)
        price = round(result['result'], 4)
        sms = f'{amount} {base} = {price} {symbol}'

        return sms
