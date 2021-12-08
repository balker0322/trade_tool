from decimal import Decimal as d
from abc import ABC, abstractmethod

RISK = '0.05'
RR_RATIO = '2.0'
K_FACTOR = '1.0008'

class ITradeCalculator(ABC):

    @abstractmethod
    def calc_position_size(self, entry_price, stop_loss_price, min_lot_size, risk=RISK):
        pass

    @abstractmethod    
    def long_tp(self, entry_price, position_size, min_price_step, risk=RISK, rr_ratio=RR_RATIO):
        pass

    @abstractmethod    
    def short_tp(self, entry_price, position_size, min_price_step, risk=RISK, rr_ratio=RR_RATIO):
        pass

    @abstractmethod    
    def long_sl(self, entry_price, position_size, min_price_step, risk=RISK):
        pass

    @abstractmethod    
    def short_sl(self, entry_price, position_size, min_price_step, risk=RISK):
        pass


class TradeCalculator(ITradeCalculator):

    def __init__(self, k_factor:str=K_FACTOR):
        self.k_factor = d(k_factor)
        self.adj_factor =  d('1.0')/self.k_factor

    def calc_position_size(self, entry_price, stop_loss_price, min_lot_size, risk=RISK):
        if float(entry_price) > float(stop_loss_price):
            return self.long_pos_size(entry_price, stop_loss_price, min_lot_size, risk)
        return self.short_pos_size(entry_price, stop_loss_price, min_lot_size, risk)

    def long_pos_size(self, entry_price, stop_loss_price, min_lot_size, risk=RISK):
        # print('calc long_pos_size')
        adj_factor = self.adj_factor
        ps = d(stop_loss_price)*adj_factor - d(entry_price)
        ps *= d('-1.0')
        ps = d(risk) / ps
        return float(self.round_param(ps, min_lot_size))

    def short_pos_size(self, entry_price, stop_loss_price, min_lot_size, risk=RISK):
        # print('calc short_pos_size')
        adj_factor = d('1.0') / self.k_factor
        ps = d(entry_price)*adj_factor - d(stop_loss_price)
        ps = d(risk) / ps
        return float(self.round_param(ps, min_lot_size))

    def calc_pnl_exit_price(self, entry_price, position, min_price_step, pnl):
        if float(position) > 0.0:
            return self.long_pnl_exit_price(entry_price, position, min_price_step, pnl, k_factor)
        return self.short_pnl_exit_price(entry_price, position, min_price_step, pnl, k_factor)

    def long_pnl_exit_price(self, entry_price, position, min_price_step, pnl):
        adj_factor = d('1.0') / self.k_factor
        exit_price = d(pnl) / abs(d(position))
        exit_price += d(entry_price)
        exit_price /= adj_factor
        return float(self.round_param(exit_price, min_price_step))

    def short_pnl_exit_price(self, entry_price, position, min_price_step, pnl):
        adj_factor = d('1.0') / self.k_factor
        exit_price = d(pnl) / abs(d(position))
        exit_price = d(entry_price)*adj_factor - exit_price
        return float(self.round_param(exit_price, min_price_step))

    def calc_exit_price(self, entry_price, stop_loss_price, min_price_step, rr_ratio=RR_RATIO):
        if float(entry_price) > float(stop_loss_price):
            return long_exit_price(entry_price, stop_loss_price, min_price_step, rr_ratio)
        return self.short_exit_price(entry_price, stop_loss_price, min_price_step, rr_ratio)

    def long_exit_price(self, entry_price, stop_loss_price, min_price_step, rr_ratio=RR_RATIO):
        a = d(entry_price)
        b = d(stop_loss_price)
        k = d('1.0')/self.k_factor
        rr = d(rr_ratio)*d('-1.0')
        exit_price = (rr*(b*k-a)+a)/k
        return float(self.round_param(exit_price, min_price_step))

    def short_exit_price(self, entry_price, stop_loss_price, min_price_step, rr_ratio=RR_RATIO):
        a = d(stop_loss_price)
        b = d(entry_price)
        k = d('1.0')/self.k_factor
        rr = d(rr_ratio)*d('-1.0')
        exit_price = (b*k)-(rr*(b*k-a))
        return float(round_param(exit_price, min_price_step))

    def long_tp(self, entry_price, position_size, min_price_step, risk=RISK, rr_ratio=RR_RATIO):
        print('calc long_tp')
        adj_factor = d('1.0') / self.k_factor
        tp = abs(d(risk)*d(rr_ratio)) / abs(d(position_size))
        tp = d(entry_price) + tp
        tp = tp / adj_factor
        return float(self.round_param(tp, min_price_step))

    def short_tp(self, entry_price, position_size, min_price_step, risk=RISK, rr_ratio=RR_RATIO):
        print('calc short_tp')
        adj_factor = d('1.0') / self.k_factor
        tp = abs(d(risk)*d(rr_ratio)) / abs(d(position_size))
        tp = d(entry_price)*adj_factor - tp
        return float(self.round_param(tp, min_price_step))

    def long_sl(self, entry_price, position_size, min_price_step, risk=RISK):
        print('calc long_sl')
        adj_factor = d('1.0') / self.k_factor
        sl = abs(d(risk)) / abs(d(position_size))
        sl = d(entry_price) - sl
        sl = sl / adj_factor
        return float(self.round_param(sl, min_price_step))

    def short_sl(self, entry_price, position_size, min_price_step, risk=RISK):
        print('calc short_sl')
        adj_factor = d('1.0') / self.k_factor
        sl = abs(d(risk)) / abs(d(position_size))
        sl = d(entry_price)*adj_factor + sl
        return float(self.round_param(sl, min_price_step))

    def round_param(self, param_size, min_param_step):
        param_size_str = str(param_size)
        min_param_step_str = str(min_param_step)
        return d(param_size_str) - (d(param_size_str)%d(min_param_step_str))

    def calc_percent_pnl(self, entry_price, position_size, exit_price, capital, side='LONG'):
        if side=='LONG':
            return self.long_percent_pnl(entry_price, position_size, exit_price, capital, k_factor)
        return self.short_percent_pnl(entry_price, position_size, exit_price, capital, k_factor)

    def long_percent_pnl(self, entry_price, position_size, exit_price, capital):
        adj_factor = d('1.0') / self.k_factor
        risk = d(exit_price)*adj_factor - d(entry_price)
        risk = risk*abs(d(position_size))
        risk = risk / d(capital)
        return float(risk)

    def short_percent_pnl(self, entry_price, position_size, exit_price, capital):
        adj_factor = d('1.0') / self.k_factor
        risk = d(entry_price)*adj_factor - d(exit_price)
        risk = risk*abs(d(position_size))
        risk = risk / d(capital)
        return float(risk)

    def split_position(self, total, split_count, min_lot_size):
        position_list = []
        # remaining = round_param(total, min_lot_size)
        remaining = abs(d(total))
        for i in range(split_count):
            position_item = round_param(remaining/d(int(split_count-i)), min_lot_size)
            if i + 1 == split_count:
                position_item = remaining
            position_item = abs(position_item)
            position_list.append(float(position_item))
            remaining -= position_item
        print(remaining)
        return position_list



if __name__=='__main__':
    tc = TradeCalculator()

    # [PositionModel(entry_price='50398.43', position_size='0.001', pair='BTCUSDT', sl_price='', tp_price='')

    entry_price='50398.43'
    position_size='0.001'
    risk_amount = '500.0'

    x = tc.long_tp(entry_price, position_size, '.001', risk_amount, 0.8)
    print(f'long_tp: {x}')

    x = tc.short_tp(entry_price, position_size, '.001', risk_amount, 0.8)
    print(f'short_tp: {x}')
    
    x = tc.long_sl(entry_price, position_size, '.001', risk_amount)
    print(f'long_sl: {x}')
    
    x = tc.short_sl(entry_price, position_size, '.001', risk_amount)
    print(f'short_sl: {x}')
    