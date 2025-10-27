from trading.strategies.trading_strategy import TradingStrategy
from sentiment.ticker_sentiment import TickerSentiment

class TradeExecutor:
    def __init__(self, strategy: TradingStrategy):
        self.trading_strategy = strategy
    
    def Trade(self, tickerSentiment: TickerSentiment):
        self.trading_strategy.ExecuteTrade(tickerSentiment)
    
    def ReviewPositions(self):
        self.trading_strategy.ReviewPositions()