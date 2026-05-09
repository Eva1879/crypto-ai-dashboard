"""
Market Agent - Phase 3
This agent handles market data fetching and basic market analysis.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class MarketAgent:
    def __init__(self):
        """Initialize the market agent"""
        self.cache = {}
        self.cache_timeout = 300  # 5 minutes
    
    def fetch_market_data(self, symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """
        Fetch market data for a cryptocurrency
        
        Args:
            symbol (str): Cryptocurrency symbol
            period (str): Time period
        
        Returns:
            pd.DataFrame: Market data
        """
        cache_key = f"{symbol}_{period}"
        current_time = datetime.now().timestamp()
        
        # Check cache
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_timeout:
                return data
        
        try:
            # Fetch fresh data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval="1d")
            
            if data.empty:
                return None
            
            # Cache the data
            self.cache[cache_key] = (data, current_time)
            
            return data
            
        except Exception as e:
            print(f"Error fetching market data for {symbol}: {e}")
            return None
    
    def get_market_overview(self, symbols: List[str]) -> Dict:
        """
        Get market overview for multiple cryptocurrencies
        
        Args:
            symbols (list): List of cryptocurrency symbols
        
        Returns:
            dict: Market overview
        """
        overview = {}
        
        for symbol in symbols:
            data = self.fetch_market_data(symbol, "5d")
            if data is not None and not data.empty:
                current_price = data['Close'].iloc[-1]
                prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
                
                # Calculate basic metrics
                price_change = current_price - prev_close
                price_change_pct = (price_change / prev_close) * 100 if prev_close != 0 else 0
                
                # Calculate volatility (5-day)
                returns = data['Close'].pct_change().dropna()
                volatility = returns.std() * np.sqrt(252)  # Annualized
                
                overview[symbol] = {
                    'current_price': current_price,
                    'price_change': price_change,
                    'price_change_pct': price_change_pct,
                    'volatility': volatility,
                    'volume': data['Volume'].iloc[-1] if 'Volume' in data.columns else 0,
                    'market_cap': self._get_market_cap(symbol),
                    'trend': self._determine_trend(data)
                }
        
        return overview
    
    def _get_market_cap(self, symbol: str) -> float:
        """Get market cap for cryptocurrency"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return info.get('marketCap', 0)
        except:
            return 0
    
    def _determine_trend(self, data: pd.DataFrame) -> str:
        """Determine trend based on moving averages"""
        if len(data) < 20:
            return "insufficient_data"
        
        current_price = data['Close'].iloc[-1]
        ma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
        ma_50 = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else ma_20
        
        if current_price > ma_20 > ma_50:
            return "strong_uptrend"
        elif current_price > ma_20:
            return "uptrend"
        elif current_price < ma_20 < ma_50:
            return "strong_downtrend"
        elif current_price < ma_20:
            return "downtrend"
        else:
            return "sideways"
    
    def analyze_volume(self, symbol: str, period: str = "1mo") -> Dict:
        """
        Analyze volume patterns
        
        Args:
            symbol (str): Cryptocurrency symbol
            period (str): Time period
        
        Returns:
            dict: Volume analysis
        """
        data = self.fetch_market_data(symbol, period)
        if data is None or 'Volume' not in data.columns:
            return {}
        
        volume = data['Volume']
        current_volume = volume.iloc[-1]
        avg_volume = volume.mean()
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        return {
            'current_volume': current_volume,
            'average_volume': avg_volume,
            'volume_ratio': volume_ratio,
            'volume_trend': 'increasing' if volume.iloc[-5:].mean() > volume.iloc[-10:-5].mean() else 'decreasing'
        }
    
    def get_market_summary(self, symbol: str) -> Dict:
        """
        Get comprehensive market summary for a symbol
        
        Args:
            symbol (str): Cryptocurrency symbol
        
        Returns:
            dict: Market summary
        """
        data = self.fetch_market_data(symbol, "3mo")
        if data is None or data.empty:
            return {}
        
        current_price = data['Close'].iloc[-1]
        
        # Price statistics
        price_stats = {
            'current': current_price,
            'high_52w': data['High'].max(),
            'low_52w': data['Low'].min(),
            'change_1d': ((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1) * 100) if len(data) > 1 else 0,
            'change_1w': ((data['Close'].iloc[-1] / data['Close'].iloc[-7] - 1) * 100) if len(data) > 7 else 0,
            'change_1m': ((data['Close'].iloc[-1] / data['Close'].iloc[-30] - 1) * 100) if len(data) > 30 else 0
        }
        
        # Technical indicators
        returns = data['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252)
        
        # Support and resistance levels (simplified)
        recent_highs = data['High'].rolling(window=20).max()
        recent_lows = data['Low'].rolling(window=20).min()
        
        support_level = recent_lows.iloc[-1]
        resistance_level = recent_highs.iloc[-1]
        
        return {
            'symbol': symbol,
            'price_stats': price_stats,
            'volatility': volatility,
            'support_level': support_level,
            'resistance_level': resistance_level,
            'trend': self._determine_trend(data),
            'volume_analysis': self.analyze_volume(symbol),
            'last_updated': datetime.now().isoformat()
        }
