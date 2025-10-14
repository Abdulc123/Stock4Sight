import os, re, json
import requests # type: ignore
import spacy # type: ignore
from rapidfuzz import process # type: ignore
from typing import List, Optional
from dotenv import load_dotenv
from news.article import Article

class NewsAccessor:
    def __init__(self):
        load_dotenv()
        self.NLP = spacy.load("en_core_web_trf") # English NEW Model (Named Entity Recognition)
        self.params = self.loadParams()
        self.company_tickers = self.loadCompanyTickersJSON()
        self.all_tickers = set(self.company_tickers.values())
        self.news_articles = [] 
    
    def loadParams(self) -> dict[str, str]:
        params = {
            "q": "stock market",   # Search keyword
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": os.getenv("NEWS_API_KEY")
        }
        return params

    def loadCompanyTickersJSON(self) -> dict[str, str]:
        current_dir = os.path.dirname(__file__) # Gets absolute path to the current file
        parent_dir = os.path.abspath(os.path.join(current_dir, "..")) # Moves up one folder to Main
        json_path = os.path.join(parent_dir, "static", "company_ticker.json")
        with open(json_path, "r") as file:
            data = json.load(file)
        
        return {normalize(k) : v for k,v in data.items()}

    def GetNewsArticles(self, url = "https://newsapi.org/v2/everything") -> None:
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
            tickers = {self.getTickerFromOrganization(org) for org in organizations}
            article = Article(title, description, tickers)
            if tickers: 
                self.news_articles.append(article) 
        print(self.news_articles)

    def getOrganizationsFromArticle(self, title: str, description: str) -> List[str]:
        text = f"{title}  {description or ''}"
        document = self.NLP(text)
        return [cleanOrgName(entity.text) for entity in document.ents if entity.label_ == "ORG"]

    def getTickerFromOrganization(self, company_name: str) -> Optional[str]:
        norm_name = normalize(cleanOrgName(company_name))
        if norm_name in self.all_tickers:
            return norm_name
        
        # find best fuzzy match among dictionary keys
        match = process.extractOne(
            norm_name,
            self.company_tickers.keys(),
            score_cutoff=90 # only accept reasonably close matches
        )
        
        if match:
            matched_company, _, _ = match
            return self.company_tickers[matched_company]
        return None


def normalize(text: str):
    return re.sub(r"[^A-Z0-9\s]", "", text.upper()) 

def cleanOrgName(name: str) -> str:
    # remove suffixes that confuse search
    name = re.sub(r",?\s*(Inc\.?|LLC|Ltd\.?|LLP|Co\.?|Group|Corporation|Corp\.?)", "", name, flags=re.I)
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)  # remove symbols like & or -
    return name.strip()