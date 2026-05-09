import pandas as pd
import numpy as np

def calculate_rsi(prices, period=14):
    """
    Calculate Relative Strength Index (RSI)
    
    Args:
        prices (pd.Series): Series of closing prices
        period (int): RSI period (default 14)
    
    Returns:
        pd.Series: RSI values
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    Calculate MACD (Moving Average Convergence Divergence)
    
    Args:
        prices (pd.Series): Series of closing prices
        fast (int): Fast EMA period
        slow (int): Slow EMA period
        signal (int): Signal line period
    
    Returns:
        tuple: (macd_line, signal_line, histogram)
    """
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """
    Calculate Bollinger Bands
    
    Args:
        prices (pd.Series): Series of closing prices
        period (int): Moving average period
        std_dev (int): Standard deviation multiplier
    
    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    middle_band = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    
    return upper_band, middle_band, lower_band
