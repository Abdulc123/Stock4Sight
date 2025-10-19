from dataclasses import dataclass, field
from news.article import Article
from static.company_ticker_map import CompanyTickerMap

@dataclass
class TickerSentiment:
    symbol: str
    related_articles: list[Article] = field(init=False, default_factory=list)
    avg_sentiment_score: float = field(init=False)
    company_name: str = field(init=False)

    def __post_init__(self):
        self.company_name = CompanyTickerMap.getCompany(self.symbol)
        self.avg_sentiment_score = 0.0
    
    def AddArticle(self, article: Article):
        self.related_articles.append(article)
    
    def CalculateAvgScore(self):
        if not self.related_articles:
            self.avg_sentiment_score = 0.0
        else:
            self.avg_sentiment_score = sum(article.score for article in self.related_articles) / len(self.related_articles)

    def __str__(self):
        return f"Ticker = {self.symbol:<10}  | Company = {self.company_name:<45} |  Score = {self.avg_sentiment_score:>5.2f}"
    
    def __lt__(self, other):
        return self.avg_sentiment_score <= other.avg_sentiment_score 


