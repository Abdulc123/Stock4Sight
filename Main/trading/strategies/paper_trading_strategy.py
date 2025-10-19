from trading.strategies.trading_strategy import TradingStrategy

class PaperTradingStrategy(TradingStrategy):

    def ExecuteTrade(self, ticker, action, amount):
        print("Executing Paper Trades...")

    def GetPositions(self):
        pass