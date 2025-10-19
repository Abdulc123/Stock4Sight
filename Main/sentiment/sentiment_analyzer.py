from transformers import AutoTokenizer, AutoModelForSequenceClassification
from news.article import Article
from sentiment.ticker_sentiment import TickerSentiment
from queue import PriorityQueue
import torch

# Finbert model for financial sentiment 
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

sentiment_to_value = {
    "positive" : 1,
    "neutral" : 0,
    "negative" : -1
}

class SentimentAnalyzer:
    # positive = investors would favor this news (possible buy)
    # neutral =  no significant market shift (hold)
    # negative = investors might react negatively (possible sell)
    
    @staticmethod
    def Analyze(article: Article) -> dict:
        text = f"{article.title} {article.description or ''}"
        tokens = tokenizer(text, return_tensors='pt', truncation=True, padding=True) # converts raw text to numerical tokens
        output = model(**tokens) # sends the tokenized tensors through finBERT -> Outputs a logit vector [Negative, Neutral, Positive]
        probs = torch.nn.functional.softmax(output.logits, dim=-1) # converts raw logits into proababilities that sum to 1

        labels = ['negative', 'neutral', 'positive'] 
        confidence, label = torch.max(probs, dim=1) # finds the index of the highest probability value
        sentiment = {
            "label": labels[label.item()], # negative, neutral, positive
            "confidence": confidence.item(), # probability
            "scores": dict(zip(labels, probs[0].tolist())) # scores for each of the labels
        }

        article.sentiment = sentiment["label"]
        article.confidence = sentiment["confidence"]
        article.score = sentiment_to_value[article.sentiment] * article.confidence
    
    def GetTickerAverageSentimentScore(news_articles: list[Article]) -> PriorityQueue:
        ticker_sentiments = {} 
        pq = PriorityQueue()
        for article in news_articles:
            for ticker in article.tickers:
                if ticker not in ticker_sentiments:
                    ticker_sentiments[ticker] = TickerSentiment(ticker)

                ticker_sentiments[ticker].AddArticle(article)
        
        for sentiment in ticker_sentiments.values():
            sentiment.CalculateAvgScore()
            pq.put((-sentiment.avg_sentiment_score, sentiment))
                    
        return pq



