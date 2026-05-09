"""
Data Fetching Utilities
This module handles fetching cryptocurrency data from various sources.
"""

import yfinance as yf
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List

class CryptoDataFetcher:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def fetch_yahoo_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Fetch cryptocurrency data from Yahoo Finance
        
        Args:
            symbol (str): Cryptocurrency symbol (e.g., 'BTC-USD')
            period (str): Time period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval (str): Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            pd.DataFrame: OHLCV data or None if error
        """
        try:
            # Check cache first
            cache_key = f"{symbol}_{period}_{interval}"
            current_time = time.time()
            
            if cache_key in self.cache:
                cached_data, timestamp = self.cache[cache_key]
                if current_time - timestamp < self.cache_timeout:
                    return cached_data
            
            # Fetch fresh data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                return None
            
            # Cache the data
            self.cache[cache_key] = (data, current_time)
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_multiple_crypto_data(self, symbols: List[str], period: str = "1mo") -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple cryptocurrencies
        
        Args:
            symbols (list): List of cryptocurrency symbols
            period (str): Time period
        
        Returns:
            dict: Dictionary with symbol as key and DataFrame as value
        """
        data_dict = {}
        
        for symbol in symbols:
            data = self.fetch_yahoo_data(symbol, period)
            if data is not None:
                data_dict[symbol] = data
        
        return data_dict
    
    def get_crypto_info(self, symbol: str) -> Optional[Dict]:
        """
        Get basic information about a cryptocurrency
        
        Args:
            symbol (str): Cryptocurrency symbol
        
        Returns:
            dict: Basic cryptocurrency information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'name': info.get('longName', 'Unknown'),
                'symbol': info.get('symbol', symbol),
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap', None),
                'volume_24h': info.get('volume24Hr', None),
                'circulating_supply': info.get('circulatingSupply', None),
                'description': info.get('longBusinessSummary', 'No description available')
            }
            
        except Exception as e:
            print(f"Error getting info for {symbol}: {e}")
            return None
    
    def get_real_time_price(self, symbol: str) -> Optional[float]:
        """
        Get real-time price for a cryptocurrency
        
        Args:
            symbol (str): Cryptocurrency symbol
        
        Returns:
            float: Current price or None if error
        """
        try:
            data = self.fetch_yahoo_data(symbol, period="1d", interval="1m")
            if data is not None and not data.empty:
                return float(data['Close'].iloc[-1])
            return None
            
        except Exception as e:
            print(f"Error getting real-time price for {symbol}: {e}")
            return None

def validate_symbol(symbol: str) -> bool:
    """
    Validate cryptocurrency symbol format
    
    Args:
        symbol (str): Cryptocurrency symbol
    
    Returns:
        bool: True if valid format
    """
    # Basic validation for common crypto symbols
    valid_patterns = [
        r'^[A-Z]{2,4}-USD$',  # BTC-USD, ETH-USD
        r'^[A-Z]{2,4}-USDT$', # BTC-USDT, ETH-USDT
        r'^[A-Z]{2,4}$'       # BTC, ETH (for some APIs)
    ]
    
    import re
    return any(re.match(pattern, symbol.upper()) for pattern in valid_patterns)

def get_supported_symbols() -> List[str]:
    """
    Get list of commonly supported cryptocurrency symbols
    
    Returns:
        list: List of supported symbols
    """
    return [
        "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD", 
        "SOL-USD", "DOGE-USD", "DOT-USD", "MATIC-USD", "LINK-USD",
        "UNI-USD", "LTC-USD", "AVAX-USD", "ATOM-USD", "FIL-USD"
    ]
