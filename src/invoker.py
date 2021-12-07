from abc import ABC, abstractmethod


class Invoker(ABC):
    pass


class TradeInvoker(Invoker):

    def __init__(self)