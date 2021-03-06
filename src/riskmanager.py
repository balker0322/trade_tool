from abc import ABC, abstractmethod
from src.positionmodel import PositionModel
from src.tradecalc import ITradeCalculator, TradeCalculator

K_FACTOR = '1.0008'

class IRiskManager(ABC):

    @abstractmethod
    def calculate_position_size(self, market_price, planned_stop_loss, min_lot_size) -> str:
        '''
        this will calculate position size based on set risk amount
        '''

    @abstractmethod
    def calculate_sl_price(self, open_position:PositionModel, min_price_step:str) -> str:
        pass

    @abstractmethod
    def calculate_tp_price(self, open_position:PositionModel, min_price_step:str) -> str:
        pass


class RiskManager(IRiskManager):

    def __init__(self, risk_amount:str, rr_ratio:str, trade_calc:ITradeCalculator=TradeCalculator(K_FACTOR)):
        self.risk_amount = risk_amount
        self.rr_ratio = rr_ratio
        self.trade_calc = trade_calc

    def calculate_position_size(self, market_price, planned_stop_loss, min_lot_size) -> str:
        result = self.trade_calc.calc_position_size(
            entry_price=market_price,
            stop_loss_price=planned_stop_loss,
            min_lot_size=min_lot_size,
            risk=self.risk_amount,
        )
        return str(result)

    def calculate_sl_price(self, open_position:PositionModel, min_price_step:str) -> str:
        calc_sl_price = self.trade_calc.short_sl
        if open_position.is_long():
            calc_sl_price = self.trade_calc.long_sl
        return calc_sl_price(
            entry_price=open_position.entry_price,
            position_size=open_position.position_size,
            min_price_step=min_price_step,
            risk=self.risk_amount,
        )

    def calculate_tp_price(self, open_position:PositionModel, min_price_step:str) -> str:
        calc_sl_price = self.trade_calc.short_tp
        if open_position.is_long():
            calc_sl_price = self.trade_calc.long_tp
        return calc_sl_price(
            entry_price=open_position.entry_price,
            position_size=open_position.position_size,
            min_price_step=min_price_step,
            risk=self.risk_amount,
            rr_ratio=self.rr_ratio,
        )

    def calculate_trail_sl_price(self, market_price, open_position:PositionModel, min_price_step:str) -> str:
        is_increasing = float(market_price) > float(open_position.entry_price)
        calc_sl_price = self.trade_calc.short_sl
        entry_price = market_price if not is_increasing else open_position.entry_price
        if open_position.is_long():
            calc_sl_price = self.trade_calc.long_sl
            entry_price = market_price if is_increasing else open_position.entry_price
        return calc_sl_price(
            entry_price=entry_price,
            position_size=open_position.position_size,
            min_price_step=min_price_step,
            risk=self.risk_amount,
        )

    def calculate_trail_tp_price(self, market_price, open_position:PositionModel, min_price_step:str) -> str:
        is_increasing = float(market_price) > float(open_position.entry_price)
        calc_tp_price = self.trade_calc.short_tp
        entry_price = market_price if not is_increasing else open_position.entry_price
        if open_position.is_long():
            calc_tp_price = self.trade_calc.long_tp
            entry_price = market_price if is_increasing else open_position.entry_price
        return calc_tp_price(
            entry_price=entry_price,
            position_size=open_position.position_size,
            min_price_step=min_price_step,
            risk=self.risk_amount,
            rr_ratio=self.rr_ratio,
        )

    def _is_winning(self, market_price, entry_price, is_long):
        is_increasing = market_price > entry_price
        if is_long and is_increasing:
            return True
        if not is_long and not is_increasing:
            return True
        return False
