import os
from alpaca_trade_api import REST # type: ignore
from dotenv import load_dotenv
from trading.strategies.trading_strategy import TradingStrategy
from sentiment.ticker_sentiment import TickerSentiment

load_dotenv()

class PaperTradingStrategy(TradingStrategy):
    """
    Executes sentiment-driven trades using Alpaca's Paper Trading API.
    Automatically handles:
        - Daily sentiment-based rebalancing
        - Profit-taking / stop-loss exits
        - Inactivity trimming for tickers no longer in the news
    """
    def __init__(
            self, 
            using_db=False, 
            max_trade_allocation: float=0.10,  # maximum percentage of total portfolio to allocate to any one ticker
            rebalance_threshold: float=0.01,   # minimum difference (1%) between current and target allocations required before making a trade
            max_profit_threshold: float=0.10,  # maximum percentage gain, before selling a stock
            stop_loss_threshold: float=-0.05,  # percent loss when to exit a losing trade
            max_inactive_days: int=7           # sell\trim holdings if no updated news for x days ???
        ):
        print("Executing Paper Trades...")
        self.api = REST( os.getenv("ALPACA_API_KEY_10k"), os.getenv("ALPACA_SECRET_KEY_10k"), os.getenv("ALPACA_API_BASE_URL") )
        self.using_db = using_db
        self.max_trade_allocation = max_trade_allocation
        self.rebalance_threshold = rebalance_threshold
        self.max_profit_threshold = max_profit_threshold
        self.stop_loss_threshold = stop_loss_threshold
        self.max_inactive_days = max_inactive_days

    def ExecuteTrade(self, tickerSentiment: TickerSentiment):
        try:
            account = self.api.get_account()
            portfolio_value = float(account.portfolio_value)
            ticker_current_price = float(self.api.get_latest_trade(tickerSentiment.symbol).p)
        except Exception as e:
            print(f"{tickerSentiment.symbol}: Failed to fetch account or price {e}")
            return

        target_allocation = self.getAllocationPercentage(tickerSentiment.avg_sentiment_score)
        current_allocation, quantity_owned = self.getCurrentAllocationAndQuantity(tickerSentiment.symbol, portfolio_value)
        allocation_diff = target_allocation - current_allocation
        trade_amount = allocation_diff * portfolio_value                    # money we want to allocate to the trade
        shares_to_trade = int(abs(trade_amount) / ticker_current_price)     # number of shares the money equals

        # Skip if there is a small difference between current allocations and the trade being made
        if abs(allocation_diff) <= self.rebalance_threshold or shares_to_trade == 0:
            print(f"{tickerSentiment.symbol} HOLD — allocation stable ({current_allocation:.2%} ≈ target {target_allocation:.2%})")
            return # Hold since the current allocation and target allocation have a delta <= self.rebalance threshold
        
        # Execute buy sell orders
        if allocation_diff > 0:
            print(f"{tickerSentiment.symbol:<10} BUY {shares_to_trade} shares → {current_allocation:.2%} → {target_allocation:.2%}")
            self.submitOrder(tickerSentiment.symbol, shares_to_trade, "buy")
        else:
            print(f"{tickerSentiment.symbol:<10} SELL {shares_to_trade} shares → {current_allocation:.2%} → {target_allocation:.2%}")
            self.submitOrder(tickerSentiment.symbol, shares_to_trade, "sell")
        
        # Place holder to update local database position tracking

    def ReviewExistingPositions(self):
        """
        Periodically checks all held positions:
          - Takes profit if gain ≥ TAKE_PROFIT_PCT
          - Stops loss if drop ≤ STOP_LOSS_PCT
          - Trims or exits if no sentiment/news for MAX_INACTIVITY_DAYS ??
        """
        pass

    def getAllocationPercentage(self, sentiment: float) -> float:
        return sentiment * self.max_trade_allocation # [-1, 1] * 0.10 (max_trade_allocation)
    
    def getCurrentAllocationAndQuantity(self, ticker: str, total_portfolio_value: float):
        try:
            position = self.api.get_position(ticker)
            current_allocation = float(position.market_value) / total_portfolio_value
            quantity_owned = float(position.qty)
        except Exception as e:
            current_allocation = 0
            quantity_owned = 0
        
        return current_allocation, quantity_owned
    
    def submitOrder(self, ticker: str, quantity: int, side: str):
        try:
            self.api.submit_order(
                symbol=ticker,
                qty=quantity,
                side=side,
                type="market",
                time_in_force="gtc"
            )
        except Exception as e:
            print(f"{ticker}: Order Failed... (Side={side}, Shares={quantity})")

    def GetPositions(self):
        try:
            return self.api.list_positions()
        except Exception as e:
            print(f"Error retrieving positions: {e}")
            return []