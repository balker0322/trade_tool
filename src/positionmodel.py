from dataclasses import dataclass


@dataclass
class PositionModel:
    entry_price:str = ''
    position_size:str = ''
    pair:str = ''
    sl_price:str = ''
    tp_price:str = ''

    def is_open_position(self) -> bool:
        if self.position_size:
            if not (abs(float(self.position_size)) == 0.0):
                return True
        return False
    
    def is_long(self) -> bool:
        if float(self.position_size) > 0.0:
            return True
        return False


