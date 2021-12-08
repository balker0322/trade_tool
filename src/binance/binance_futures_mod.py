from .binance_futures import BinanceFutures
from src.binance.binance_futures_api import Client
from .mod_func import *

def test_output(
    symbol = None,
    type = None,
    newClientOrderId = None,
    side = None,
    quantity = None,
    activationPrice = None,
    callbackRate = None,
    price = None,
    timeInForce = None,
    stopPrice = None,
    reduceOnly = None,
):
    print("=============================================")
    print(f"symbol: {symbol}")
    print(f"type: {type}")
    print(f"newClientOrderId: {newClientOrderId}")
    print(f"side: {side}")
    print(f"quantity: {quantity}")
    print(f"activationPrice: {activationPrice}")
    print(f"callbackRate: {callbackRate}")
    print(f"price: {price}")
    print(f"timeInForce: {timeInForce}")
    print(f"stopPrice: {stopPrice}")
    print(f"reduceOnly: {reduceOnly}")
    print("=============================================")


class BinanceFuturesMod(BinanceFutures):

    def __init__(self, api_key:str, api_secret:str):
        self.client = Client(api_key=api_key, api_secret=api_secret)

    def __init_client(self):
        pass

    def get_market_price(self):
        """
        get current price
        :return:
        """
        self.__init_client()
        self.market_price = retry(lambda: self.client
                                    .futures_symbol_ticker(symbol=self.pair))
        return self.market_price['price']
        
    def _new_order(self, ord_id, side, ord_qty, limit=0, stop=0, post_only=False, reduce_only=False, trailing_stop=0, activationPrice=0):
        """
        create an order for test
        """
        #removes "+" from order suffix, because of the new regular expression rule for newClientOrderId updated as ^[\.A-Z\:/a-z0-9_-]{1,36}$ (2021-01-26)
        ord_id = ord_id.replace("+", "k") 
        
        if  trailing_stop > 0 and activationPrice > 0:
            ord_type = "TRAILING_STOP_MARKET"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, activationPrice=activationPrice,
                                                              callbackRate=trailing_stop)
        elif trailing_stop > 0:
            ord_type = "TRAILING_STOP_MARKET"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, callbackRate=trailing_stop)
        elif limit > 0 and post_only:
            ord_type = "LIMIT"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, price=limit,
                                                              timeInForce="GTX")
        elif limit > 0 and stop > 0 and reduce_only:
            ord_type = "STOP"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, price=limit,
                                                              stopPrice=stop, reduceOnly="true")
        elif limit > 0 and reduce_only:
            ord_type = "LIMIT"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, price=limit,
                                                              reduceOnly="true", timeInForce="GTC")
        elif limit > 0 and stop > 0:
            ord_type = "STOP"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, price=limit,
                                                              stopPrice=stop)
        elif limit > 0:   
            ord_type = "LIMIT"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, price=limit, timeInForce="GTC")
        elif stop > 0 and reduce_only:
            ord_type = "STOP_MARKET"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, stopPrice=stop,
                                                              reduceOnly="true")    
        elif stop > 0:
            ord_type = "STOP"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty, stopPrice=stop)      
        elif post_only: # limit order with post only
            ord_type = "LIMIT"
            i = 0            
            while True:                 
                prices = self.get_orderbook_ticker()
                limit = float(prices['bidPrice']) if side == "Buy" else float(prices['askPrice'])                
                test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                                  side=side, quantity=ord_qty, price=limit,
                                                                  timeInForce="GTX")
                time.sleep(4)
                break
        else:
            ord_type = "MARKET"
            test_output(symbol=self.pair, type=ord_type, newClientOrderId=ord_id,
                                                              side=side, quantity=ord_qty)

    def fetch_ohlcv(self, bin_size, start_time, end_time):
        pass

    def security(self, bin_size):
        pass

    def __update_ohlcv(self, action, new_data):
        pass

    def __on_update_instrument(self, action, instrument):
        pass

    def __on_update_wallet(self, action, wallet):
        pass

    def __on_update_order(self, action, order):
        pass

    def __on_update_position(self, action, position):
        pass

    def __on_update_margin(self, action, margin):
        pass

    def __on_update_bookticker(self, action, bookticker):
        pass

    def on_update(self, bin_size, strategy):
        pass

    def stop(self):
        pass

    def get_tp_order(self):
        """
        Get open order by id
        :param id: Order id for this pair
        :return:
        """
        self.__init_client()
        open_orders = retry(lambda: self.client
                            .futures_get_open_orders(symbol=self.pair))                                   
        open_orders = [o for o in open_orders if (o["origType"].startswith('TAKE_PROFIT') or o["origType"].startswith('LIMIT')) and o['reduceOnly']]
        return open_orders

    def get_sl_order(self):
        """
        Get open order by id
        :param id: Order id for this pair
        :return:
        """
        self.__init_client()
        open_orders = retry(lambda: self.client
                            .futures_get_open_orders(symbol=self.pair))                                   
        open_orders = [o for o in open_orders if o["origType"].startswith('STOP') and o['reduceOnly']]
        return open_orders
    
    def cancel_existing_tp_order(self):
        tp_orders = self.get_tp_order()
        for tp_order in tp_orders:
            self.cancel(id=tp_order['clientOrderId'])
    
    def cancel_existing_sl_order(self):
        sl_orders = self.get_sl_order()
        for sl_order in sl_orders:
            self.cancel(id=sl_order['clientOrderId'])

    def get_futures_exchange_info(self):
        """
        added
        """
        self.__init_client()
        self.exchange_info = retry(lambda: self.client
                            .futures_exchange_info())            
        return self.exchange_info
