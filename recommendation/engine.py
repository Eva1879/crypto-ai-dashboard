import pandas as pd
import numpy as np

def get_recommendation(rsi, data, threshold_sell=70, threshold_buy=30):
    """
    Generate BUY/HOLD/SELL recommendation based on RSI and price action
    
    Args:
        rsi (float): Current RSI value
        data (pd.DataFrame): Price data with OHLCV
        threshold_sell (float): RSI threshold for sell signal
        threshold_buy (float): RSI threshold for buy signal
    
    Returns:
        dict: Recommendation with action and reasoning
    """
    current_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
    
    # Calculate price change
    price_change = (current_price / prev_price - 1) * 100
    
    # Calculate moving averages for trend analysis
    ma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    ma_50 = data['Close'].rolling(window=50).mean().iloc[-1] if len(data) >= 50 else ma_20
    
    # Determine trend
    if current_price > ma_20 > ma_50:
        trend = "uptrend"
    elif current_price < ma_20 < ma_50:
        trend = "downtrend"
    else:
        trend = "sideways"
    
    # Generate recommendation logic
    reasoning_parts = []
    
    if rsi > threshold_sell:
        action = "SELL"
        reasoning_parts.append(f"RSI ({rsi:.1f}) indicates overbought conditions")
        if price_change > 2:
            reasoning_parts.append(f"Strong upward momentum ({price_change:.1f}%) suggests profit-taking")
    elif rsi < threshold_buy:
        action = "BUY"
        reasoning_parts.append(f"RSI ({rsi:.1f}) indicates oversold conditions")
        if price_change < -2:
            reasoning_parts.append(f"Recent decline ({price_change:.1f}%) presents buying opportunity")
    else:
        action = "HOLD"
        reasoning_parts.append(f"RSI ({rsi:.1f}) is in neutral zone")
    
    # Add trend context
    if trend == "uptrend" and action == "BUY":
        reasoning_parts.append("Confirmed uptrend supports buying decision")
    elif trend == "downtrend" and action == "SELL":
        reasoning_parts.append("Confirmed downtrend supports selling decision")
    elif trend == "sideways":
        reasoning_parts.append("Sideways market suggests caution")
    
    # Add volatility check
    volatility = data['Close'].rolling(window=14).std().iloc[-1] / data['Close'].rolling(window=14).mean().iloc[-1]
    if volatility > 0.03:  # High volatility threshold
        reasoning_parts.append("High volatility detected - consider position sizing")
    
    reasoning = " | ".join(reasoning_parts)
    
    return {
        "action": action,
        "reasoning": reasoning,
        "rsi": rsi,
        "trend": trend,
        "volatility": volatility
    }

def calculate_risk_score(data):
    """
    Calculate risk score based on volatility and price action
    
    Args:
        data (pd.DataFrame): Price data
    
    Returns:
        float: Risk score (0-100, higher = riskier)
    """
    # Calculate volatility
    returns = data['Close'].pct_change().dropna()
    volatility = returns.std() * np.sqrt(252)  # Annualized volatility
    
    # Calculate maximum drawdown
    rolling_max = data['Close'].expanding().max()
    drawdown = (data['Close'] - rolling_max) / rolling_max
    max_drawdown = abs(drawdown.min())
    
    # Combine metrics for risk score
    risk_score = min(100, (volatility * 100) + (max_drawdown * 200))
    
    return risk_score
