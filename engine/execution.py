
class Execution:
    def __init__(self, slippage: float, commission: float):
        self.slippage = slippage
        self.commission = commission
    def calculate_trade_price(self, price: float, signal: int) -> float:
        trade_price = price
        if signal == 1:
            trade_price = trade_price * (1 +self.slippage) 
            trade_price = trade_price * (1 + self.commission)
        elif signal == -1:
            trade_price = trade_price * (1 - self.slippage)
            trade_price = trade_price * (1 - self.commission)
        return trade_price