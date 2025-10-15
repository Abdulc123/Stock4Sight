# Reading From the config file 
# Set up logger to write to a file, allows me to keep track what is happening 
# Store current positions in sql table, based on paper trading positions

# Start based on start time
    # Read articles from NEWSAPI website, (Done)
        # Store the ticker and heading title (Done)
        # Feed to Finbert for a buy\sell\hold confidence number (Done)
    # Calculate the average confidence for a given stock based on multiple articles
    # Use confidence number and config thresholds to determine the action and how much money to put in or sell
    # Call alpaca paper trading api and put in the request

# End based on end time

from news.news_accessor import NewsAccessor
from sentiment.sentiment_analyzer import SentimentAnalyzer
from static.company_ticker_map import CompanyTickerMap
from sentiment.ticker_sentiment import TickerSentiment


class Stock4Sight:
    def __init__(self):
        self.news_articles = None
        self.news_accessor = NewsAccessor()
        CompanyTickerMap.loadMaps()

    def start(self):
        self.news_articles = self.news_accessor.GetNewsArticles()
        self.analyzeArticles()
        self.outputTickerAvgSentiment()
    
    def analyzeArticles(self):
        for article in self.news_articles:
            SentimentAnalyzer.Analyze(article)
            article.OutputSentiment()

    def outputTickerAvgSentiment(self):   
        # Get the list of ticker sentiments for all of them         
        ticker_sentiments = SentimentAnalyzer.GetTickerAverageSentimentScore(self.news_articles)
        for t_sentiment in ticker_sentiments.values():
            print(t_sentiment)

def main():
    stock4Sight = Stock4Sight()
    stock4Sight.start()

if __name__ == "__main__":
    main()
