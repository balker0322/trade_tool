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
        position_size = self.risk_manager.calculate_position_size(market_price, planned_stop_loss)
        self.exchange.open_position(pair, position_size)
    
    def add_sl_on_open_position(self):
        open_positions = self.exchange.get_all_open_positions()
        if open_positions:
            for open_position in open_positions:
                sl_price = self.risk_manager.calculate_sl_price(open_position)
                self.exchange.add_sl_on_open_position(open_position, sl_price)
    
    def add_tp_on_open_position(self):
        open_positions = self.exchange.get_all_open_positions()
        if open_positions:
            for open_position in open_positions:
                tp_price = self.risk_manager.calculate_tp_price(open_position)
                self.exchange.add_tp_on_open_position(open_position, tp_price)

    def close_all_position(self):
        self.exchange.close_all_position()