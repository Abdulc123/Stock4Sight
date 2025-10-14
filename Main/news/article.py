from typing import Set, Optional
from dataclasses import dataclass, field

@dataclass(eq=True, frozen=False)
class Article:
    title: str
    description: str
    tickers: Set[str] = field(default_factory=set)
    sentiment: str = None
    confidence: int = None
    score: float = None

    def OutputSentiment(self) -> None:
        print(f"{str(self.tickers):<15} {self.title[:80]:<80}... -> {self.sentiment:<10} ({self.confidence:.2f}) Score={self.score:<5.2f}")
        
    def SetSentiment(self, sentiment: int) -> None:
        self.sentiment = sentiment

    def __str__(self):
        return f"{self.title} | {self.tickers} | Sentiment: {self.sentiment} {self.score:.2f}"
    