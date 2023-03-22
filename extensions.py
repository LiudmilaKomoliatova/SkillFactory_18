import requests
import json
from config import API_TOKEN, API_URL, source_currency, base_currency


class ConvertionException(Exception):
	pass


class CryptoConverter:
	@staticmethod
	def get_source():
		return '\n'.join([f'{i} ({n})' for i, n in source_currency.items()])

	@staticmethod
	def get_currency():
		return '\n'.join(base_currency)

	@staticmethod
	def convert(source: str, base: str,  amount: str):
		if source not in source_currency:
			raise ConvertionException('Данный крипто символ не поддерживается')
		# Condition 1 (Бот возвращает цену на определённое количество валюты (евро, доллар или рубль)
		base = base.replace('ЕВРО', 'EUR').replace('ДОЛЛАР', 'USD').replace('РУБЛЬ', 'RUB')
		if base not in base_currency:
			raise ConvertionException('Данная валюта не поддерживается')
		if source == base:
			raise ConvertionException('R валюта не поддерживается')

		try:
			amount = float(amount)
			response = requests.get(f'{API_URL}/data/price?fsym={source}&tsyms={base}&api_key={API_TOKEN}')
			response_json = json.loads(response.content)
			print(response_json)
			result = amount * response_json[base]
		except Exception as e:
			raise ConvertionException(f'Ошибка {e}')

		return result

