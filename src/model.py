from src.positionmodel import PositionModel


class Model:
    pair:str=''
    planned_stop_loss:str=''
    open_positions:list[PositionModel]=[]
