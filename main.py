from binance import Client
from src.config import binance_viewer


def main():

    prices = binance_viewer.get_symbol_info('BNBBTC')

    print(prices)




if __name__=='__main__':
    main()