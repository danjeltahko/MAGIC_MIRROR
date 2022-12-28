import requests 
import json
from API.api_keys import COINMARKET_KEY

class CoinMarketCap:

    def __init__(self) -> None:
        self.url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COINMARKET_KEY,
            "Accept-Encoding": "deflate, gzip"
            }

    def get_data(self):
        parameters = {
            "symbol": "ETH",
            "convert": "SEK"
        }

        response = requests.get(self.url, headers=self.headers, params=parameters)
        #data = json.dumps(response.text)
        print(response.text)

# https://coinmarketcap.com/api/documentation/v1/#operation/getV1CryptocurrencyTrendingMostvisited

