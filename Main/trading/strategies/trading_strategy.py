from abc import ABC, abstractmethod
from sentiment.ticker_sentiment import TickerSentiment

class TradingStrategy(ABC):

    @abstractmethod
    def ExecuteTrade(self, tickerSentiment: TickerSentiment):
        pass

    @abstractmethod
    def GetPositions(self):
        pass