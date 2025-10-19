from abc import ABC, abstractmethod

class TradingStrategy(ABC):

    @abstractmethod
    def ExecuteTrade(self, ticker, action, amount):
        pass

    @abstractmethod
    def GetPositions(self):
        pass