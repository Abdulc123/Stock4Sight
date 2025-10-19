import sqlite3
import os
from datetime import datetime
from news.article import Article
from static.company_ticker_map import CompanyTickerMap

class DatabaseManager:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "database", "stock4sight.db")

    @staticmethod
    def getConnection():
        return sqlite3.connect(DatabaseManager.DB_PATH)

    @staticmethod
    def StoreNewsSentiment(article: Article):
        """
        sentiment = Positive, Neutral, Negative
        confidence = % of how certain it is on the sentiment
        score = sentiment value (-1, 0,  1) * confidence percentage
        """
        connection = DatabaseManager.getConnection()
        cursor = connection.cursor()
        for ticker in article.tickers:
            cursor.execute(
                """
                INSERT OR IGNORE INTO news_sentiments (ticker, company_name, sentiment, confidence, score, article_title, published_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (ticker, CompanyTickerMap.getCompany(ticker), article.sentiment, article.confidence, article.score, article.title, datetime.now().isoformat())
            )
            connection.commit()
        connection.close()

    
    @staticmethod
    def LogTrade():
        pass

    @staticmethod
    def GetAllTrades(ticker):
        pass
    