from trading.strategies.trading_strategy import TradingStrategy
from sentiment.ticker_sentiment import TickerSentiment

class LiveTradingStrategy(TradingStrategy):

    def ExecuteTrade(self, tickerSentiment: TickerSentiment):
        print("Executing Live Trades...")

    def ReviewPositions(self):
        pass