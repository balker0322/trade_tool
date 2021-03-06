from abc import ABC, abstractmethod
from src.exchange import IExchange
from src.riskmanager import IRiskManager


class Invoker(ABC):
    pass


class TradeInvoker(Invoker):
    
    def __init__(self, exchange:IExchange, risk_manager:IRiskManager):
        self.exchange = exchange
        self.risk_manager = risk_manager
    
    def open_position(self, pair:str, planned_stop_loss:float):
        market_price = self.exchange.get_market_price(pair)
        min_lot_size = self.exchange.get_min_lot_size(pair=pair)
        position_size = self.risk_manager.calculate_position_size(market_price, planned_stop_loss, min_lot_size)
        self.exchange.open_position(pair, position_size)
    
    def open_position_test(self, pair:str, planned_stop_loss:float):
        market_price = self.exchange.get_market_price(pair)
        min_lot_size = self.exchange.get_min_lot_size(pair=pair)
        position_size = self.risk_manager.calculate_position_size(market_price, planned_stop_loss, min_lot_size)
        side = 'SHORT' if float(position_size) < 0.0 else 'LONG'
        print("==========TEST==========")
        print(f"{pair}: {market_price} USDT")
        print(f"Planned SL: {planned_stop_loss} USDT")
        print(f"Side: {side}")
        print(f"Position Size: {position_size} {pair.replace('USDT','')}")
        print("========================")

    def get_all_open_positions(self, pair:str=''):
        if pair:
            return [o for o in self.exchange.get_all_open_positions() if o.pair.lower() == pair.lower()]
        return self.exchange.get_all_open_positions()
    
    def eval_sl(self, pair:str=''):
        open_positions = self.get_all_open_positions(pair)
        for open_position in open_positions:
            min_price_step = self.exchange.get_min_price_step(pair=open_position.pair)
            sl_price = self.risk_manager.calculate_sl_price(open_position, min_price_step)
            self.exchange.eval_sl(open_position, sl_price)
    
    def eval_tp(self, pair:str=''):
        open_positions = self.get_all_open_positions(pair)
        for open_position in open_positions:
            min_price_step = self.exchange.get_min_price_step(pair=open_position.pair)
            tp_price = self.risk_manager.calculate_tp_price(open_position, min_price_step)
            self.exchange.eval_tp(open_position, tp_price)
    
    def trail_sl(self, pair:str=''):
        open_positions = self.get_all_open_positions(pair)
        market_price = self.exchange.get_market_price(pair)
        for open_position in open_positions:
            min_price_step = self.exchange.get_min_price_step(pair=open_position.pair)
            sl_price = self.risk_manager.calculate_trail_sl_price(market_price, open_position, min_price_step)
            self.exchange.eval_sl(open_position, sl_price)
    
    def trail_tp(self, pair:str=''):
        open_positions = self.get_all_open_positions(pair)
        market_price = self.exchange.get_market_price(pair)
        for open_position in open_positions:
            min_price_step = self.exchange.get_min_price_step(pair=open_position.pair)
            tp_price = self.risk_manager.calculate_trail_tp_price(market_price, open_position, min_price_step)
            self.exchange.eval_tp(open_position, tp_price)

    def close_all_position(self):
        self.exchange.close_all_position()