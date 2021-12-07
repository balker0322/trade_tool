from abc import ABC, abstractmethod
from binance import Client


class IExchange(ABC):
    pass


class BinanceExchange(IExchange):

    def __init__(self, api_key:str, api_secret:str):
        self.client = Client(api_key, api_secret)

    def get_symbol_info(self, pair:str):
        return self.client.get_symbol_info(pair)