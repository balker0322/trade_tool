from binance import Client
from src.config import binance_viewer, risk_manager
from src.invoker import TradeInvoker


def main():

    trader = TradeInvoker(exchange=binance_viewer, risk_manager=risk_manager)
    trader.open_position(pair='BTCUSDT', planned_stop_loss=50999.99)
    trader.add_sl_on_open_position()
    trader.close_all_position()


if __name__=='__main__':
    main()