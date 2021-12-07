from binance import Client
from src.config import config


def main():
    mode = 'viewing'
    api_key = config['binance_keys'][mode]['API_KEY']
    api_secret = config['binance_keys'][mode]['SECRET_KEY']
    client = Client(api_key, api_secret)

    prices = client.get_symbol_info('BNBBTC')

    print(prices)




if __name__=='__main__':
    main()