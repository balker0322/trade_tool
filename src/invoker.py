from abc import ABC, abstractmethod
from binance import Client


class Invoker(ABC):
    pass


class TradeInvoker(Invoker):
    pass