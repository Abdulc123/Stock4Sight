from typing import Set, Optional
from dataclasses import dataclass, field

@dataclass(eq=True, frozen=False)
class Article:
    title: str
    description: str
    tickers: Set[str] = field(default_factory=set)
    sentiment: Optional[int] = None
    
    def __post_init__(self):
        self.tickers = {t for t in self.tickers if t}
    
    def SetSentiment(self, sentiment: int) -> None:
        self.sentiment = sentiment

    def __str__(self):
        return f"{self.title} | {self.tickers} | Sentiment: {self.sentiment}"
    