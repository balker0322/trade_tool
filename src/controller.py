from binance import Client
from src.invoker import TradeInvoker
from src.exchange import BinanceExchange
from src.riskmanager import RiskManager
from src.config import VIEWER_API_KEY, VIEWER_API_SECRET, RISK_AMOUNT, RR_RATIO

binance_viewer = BinanceExchange(VIEWER_API_KEY, VIEWER_API_SECRET)
risk_manager = RiskManager(RISK_AMOUNT, RR_RATIO)
trader = TradeInvoker(exchange=binance_viewer, risk_manager=risk_manager)

class Controller:

    def __init__(self):
        self.trader

