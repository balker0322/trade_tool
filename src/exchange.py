from abc import ABC, abstractmethod
# from binance import Client
from src.positionmodel import PositionModel
from src.binance.binance_futures_mod import BinanceFuturesMod


class IExchange(ABC):
    
    @abstractmethod
    def get_market_price(self, pair:str) -> str:
        pass
    
    @abstractmethod
    def open_position(self, pair:str, position_size:str):
        pass

    @abstractmethod
    def eval_sl(self, open_position:PositionModel, sl_price:str):
        pass

    @abstractmethod
    def eval_tp(self, open_position:PositionModel, tp_price:str):
        pass

    @abstractmethod
    def get_all_open_positions(self) -> list[PositionModel]:
        pass

    @abstractmethod
    def close_all_position(self):
        pass

    @abstractmethod
    def get_all_pair_symbol(self) -> list[str]:
        pass

    @abstractmethod
    def get_min_lot_size(self, pair:str):
        pass
    
    @abstractmethod
    def get_min_price_step(self, pair:str):
        pass


class BinanceExchange(IExchange):

    def __init__(self, api_key:str, api_secret:str):
        self.client = BinanceFuturesMod(api_key, api_secret)
        self.__init_pair_info()
    
    def __init_pair_info(self):
        raw_pair_info = self.client.get_futures_exchange_info()['symbols']
        pair_info = dict()
        base_coin = 'USDT'
        for pair in raw_pair_info:
            if pair['symbol'].upper()[-len(base_coin):] == base_coin.upper():
                pair_info[pair['symbol']] = {
                    'min_lot_size' : pair['filters'][1]['minQty'],
                    'min_price_step' : pair['filters'][0]['tickSize'],
                }
        self.pair_info = pair_info
    
    def get_min_lot_size(self, pair:str):
        return self.pair_info[pair]['min_lot_size']
    
    def get_min_price_step(self, pair:str):
        return self.pair_info[pair]['min_price_step']
    
    def get_market_price(self, pair:str) -> str:
        self.client.pair = pair
        return str(self.client.get_market_price())
    
    def open_position(self, pair:str, position_size:str):
        if float(position_size) < 0.0:
            self.__open_short_position(pair,position_size.replace('-', ''))
        else:
            self.__open_long_position(pair,position_size)

    def __open_long_position(self, pair:str, position_size:str):
        # print('__open_long_position')
        self.client.pair = pair
        self.client.entry("Long", True, float(position_size))

    def __open_short_position(self, pair:str, position_size:str):
        # print('__open_short_position')
        self.client.pair = pair
        self.client.entry("Short", False, float(position_size))

    def __get_position(self, pair:str) -> PositionModel:
        '''
        If pair has open position, this function will return details of the open position
        api_response:
        {
            'symbol': 'BTCUSDT',
            'positionAmt': '0.000',
            'entryPrice': '0.0',
            'markPrice': '51271.86262448',
            'unRealizedProfit': '0.00000000',
            'liquidationPrice': '0',
            'leverage': '8',
            'maxNotionalValue': '40000000',
            'marginType': 'isolated',
            'isolatedMargin': '0.00000000',
            'isAutoAddMargin': 'false',
            'positionSide': 'BOTH',
            'notional': '0',
            'isolatedWallet': '0',
            'updateTime': 1638783595325
        }
        '''
        self.client.pair = pair
        position_model = PositionModel()
        api_response = self.client.get_position()
        position_model.pair = api_response['symbol']
        position_model.position_size = api_response['positionAmt']
        if position_model.is_open_position():
            position_model.entry_price = api_response['entryPrice']
        return position_model

    def get_all_open_positions(self) -> list[PositionModel]:
        open_positions = []
        for pair in self.get_all_pair_symbol():
            open_position = self.__get_position(pair)
            if open_position.is_open_position():
                open_positions.append(open_position)
        return open_positions

    def eval_sl(self, open_position:PositionModel, sl_price:str):
        if not open_position.is_open_position():
            return
        self.client.pair = open_position.pair
        self.client.cancel_existing_sl_order()
        # print(f'sl_price: {sl_price}')
        self.client.order("SL", not open_position.is_long(), abs(float(open_position.position_size)), stop=float(sl_price), reduce_only=True)

    def eval_tp(self, open_position:PositionModel, tp_price:str):
        if not open_position.is_open_position():
            return
        self.client.pair = open_position.pair
        self.client.cancel_existing_tp_order()
        self.client.order("TP", not open_position.is_long(), abs(float(open_position.position_size)), limit=float(tp_price), reduce_only=True)

    def close_position(self, pair:str):
        self.client.pair = pair
        self.client.close_all()
        self.client.cancel_existing_sl_order()
        self.client.cancel_existing_tp_order()

    def close_all_position(self):
        for open_position in self.get_all_open_positions():
            self.close_position(open_position.pair)

    def get_all_pair_symbol(self) -> list[str]:
        # return list(self.pair_info.keys())
        return [
            'BTCUSDT',
            'ETHUSDT',
            'ADAUSDT',
            'MANAUSDT'
        ]