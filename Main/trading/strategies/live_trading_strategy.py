from trading.strategies.trading_strategy import TradingStrategy

class LiveTradingStrategy(TradingStrategy):

    def ExecuteTrade(self, ticker, action, amount):
        print("Executing Live Trades...")

    def GetPositions(self):
        pass