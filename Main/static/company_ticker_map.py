import os, json, re
from utils.util import Util

class CompanyTickerMap:
    company_to_ticker = {}
    ticker_to_company = {}

    @staticmethod
    def loadMaps():
        current_dir = os.path.dirname(__file__) # Gets absolute path to the current file
        parent_dir = os.path.abspath(os.path.join(current_dir, "..")) # Moves up one folder to Main
        json_path = os.path.join(parent_dir, "static", "company_ticker.json")
        with open(json_path, "r") as file:
            company_to_ticker = json.load(file)
            CompanyTickerMap.company_to_ticker = {Util.normalize(k) : v for k,v in company_to_ticker.items()}
        
        CompanyTickerMap.ticker_to_company = {v : k for k, v in company_to_ticker.items()}
        

    @staticmethod
    def getTicker(company_name) -> str:
        return CompanyTickerMap.company_to_ticker.get(company_name, None)

    @staticmethod
    def getCompany(ticker) ->  str:
        return CompanyTickerMap.ticker_to_company.get(ticker, None)
