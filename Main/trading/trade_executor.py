from trading.strategies.trading_strategy import TradingStrategy

class TradeExecutor:
    def __init__(self, strategy: TradingStrategy):
        self.trading_strategy = strategy
    
    def Trade(self, ticker, action, amount):
        self.trading_strategy.ExecuteTrade(ticker, action, amount)