from abc import ABC, abstractmethod


class IExchange(ABC):
    
    @abstractmethod
    def get_pair_market_price(self, pair:str) -> float:
        pass

    @abstractmethod
    def open_position(self, pair:str):
        pass

class BinanceExchange(IExchange):

    def __init__(self, api_key:str, api_secret:str):
        self.client = Client(api_key, api_secret)

    def get_symbol_info(self, pair:str):
        return self.client.get_symbol_info(pair)