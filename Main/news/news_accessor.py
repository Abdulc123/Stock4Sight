import os, re, json
import requests # type: ignore
import spacy # type: ignore
from rapidfuzz import process # type: ignore
from typing import List, Optional
from dotenv import load_dotenv
from news.article import Article
from static.company_ticker_map import CompanyTickerMap
from utils.util import Util

class NewsAccessor:
    def __init__(self):
        load_dotenv()
        self.NLP = spacy.load("en_core_web_trf") # English NEW Model (Named Entity Recognition)
        self.params = self.loadParams()
        self.news_articles = [] 
    
    def loadParams(self) -> dict[str, str]:
        params = {
            "q": "stock market",   # Search keyword
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": os.getenv("NEWS_API_KEY")
        }
        return params

    def GetNewsArticles(self, url = "https://newsapi.org/v2/everything") -> List[Article]:
        params = self.loadParams()
        response = requests.get(url, params)

        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            return
        
        data = response.json()
        articles = data.get("articles", [])
        for article in articles:
            title = article['title']
            description = article['description']
            organizations = self.getOrganizationsFromArticle(title, description)
            tickers = {t for org in organizations if (t := self.getTickerFromOrganization(org)) is not None}
            article = Article(title, description, tickers)
            if len(tickers) > 0: 
                self.news_articles.append(article) 

        return self.news_articles

    def getOrganizationsFromArticle(self, title: str, description: str) -> List[str]:
        text = f"{title}  {description or ''}"
        document = self.NLP(text)
        return [Util.cleanOrgName(entity.text) for entity in document.ents if entity.label_ == "ORG"]

    def getTickerFromOrganization(self, company_name: str) -> Optional[str]:
        company_name = Util.normalize(company_name)
        if company_name in CompanyTickerMap.ticker_to_company.keys():
            return company_name
        
        # find best fuzzy match among dictionary keys
        match = process.extractOne(
            company_name,
            CompanyTickerMap.company_to_ticker.keys(),
            score_cutoff=90 # only accept reasonably close matches
        )
        
        if match:
            matched_company, _, _ = match
            return CompanyTickerMap.getTicker(matched_company)
        return None