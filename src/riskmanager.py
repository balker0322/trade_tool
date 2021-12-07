from abc import ABC, abstractmethod


class IRiskManager(ABC):

    @abstractmethod
    def calculate_position_size(self) -> float:
        '''
        this will calculate position size based on set risk amount
        '''

class RiskManager(IRiskManager):

    def __init__(self, risk_amount:float, rr_ratio:float):
        self.risk_amount = risk_amount
        self.rr_ratio = rr_ratio