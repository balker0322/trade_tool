from src.invoker import TradeInvoker
from src.exchange import BinanceExchange
from src.riskmanager import RiskManager
from src.config import VIEWER_API_KEY, VIEWER_API_SECRET
from src.config import TRADER_API_KEY, TRADER_API_SECRET
from src.config import RISK_AMOUNT, RR_RATIO

binance_viewer = BinanceExchange(VIEWER_API_KEY, VIEWER_API_SECRET)
binance_trader = BinanceExchange(TRADER_API_KEY, TRADER_API_SECRET)
risk_manager = RiskManager(RISK_AMOUNT, RR_RATIO)

def trade_test(pair, planned_stop_loss):
    trader = TradeInvoker(exchange=binance_viewer, risk_manager=risk_manager)
    trader.open_position_test(pair, planned_stop_loss)

def trade(pair, planned_stop_loss):
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.open_position(pair, planned_stop_loss)
    trader.eval_sl(pair)
    trader.eval_tp(pair)

def trail_sltp(pair):
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.trail_sl(pair)
    trader.trail_tp(pair)

def eval_sltp(pair):
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.eval_sl(pair)
    trader.eval_tp(pair)

def close_all():
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.close_all_position()


if __name__=='__main__':
    pair = 'BTCUSDT'
    # trade(pair, 49500.00)
    # trade_test(pair, 49100.00)
    trail_sltp(pair)
    # eval_sltp(pair)
    