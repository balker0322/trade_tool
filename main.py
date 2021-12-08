from src.invoker import TradeInvoker
from src.exchange import BinanceExchange
from src.riskmanager import RiskManager
from src.config import VIEWER_API_KEY, VIEWER_API_SECRET
from src.config import TRADER_API_KEY, TRADER_API_SECRET
from src.config import RISK_AMOUNT, RR_RATIO


def trade_test(pair, planned_stop_loss):
    binance_viewer = BinanceExchange(VIEWER_API_KEY, VIEWER_API_SECRET)
    risk_manager = RiskManager(RISK_AMOUNT, RR_RATIO)
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.open_position_test(pair, planned_stop_loss)

def trade(pair, planned_stop_loss):
    binance_viewer = BinanceExchange(VIEWER_API_KEY, VIEWER_API_SECRET)
    binance_trader = BinanceExchange(TRADER_API_KEY, TRADER_API_SECRET)
    risk_manager = RiskManager(RISK_AMOUNT, RR_RATIO)
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.open_position(pair, planned_stop_loss)
    trader.eval_sl(pair)
    trader.eval_tp(pair)

def close_all():
    binance_viewer = BinanceExchange(VIEWER_API_KEY, VIEWER_API_SECRET)
    binance_trader = BinanceExchange(TRADER_API_KEY, TRADER_API_SECRET)
    risk_manager = RiskManager(RISK_AMOUNT, RR_RATIO)
    trader = TradeInvoker(exchange=binance_trader, risk_manager=risk_manager)
    trader.close_all_position()


if __name__=='__main__':
    trade_test('BTCUSDT', 50517)