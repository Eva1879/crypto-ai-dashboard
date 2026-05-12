"""
Streamlit Deployable Crypto Dashboard - Standalone Version
Works without complex module dependencies for easy deployment
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import requests
from textblob import TextBlob
import os

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    h1, h2, h3 {
        color: white !important;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
    div[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Crypto AI Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

def login_page():
    """Simple login page"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 30px; border-radius: 20px; margin-bottom: 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);">
        <h1 style="text-align: center; margin: 0; color: white; font-size: 2.5em;">
            🚀 Crypto AI Dashboard
        </h1>
        <p style="text-align: center; margin: 10px 0 0 0; color: rgba(255, 255, 255, 0.9); font-size: 1.2em;">
            Multi-Agent Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
    
    with col2:
        st.info("Use any username/password to demo")

def calculate_rsi(prices, period=14):
    """Calculate RSI"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    exp1 = prices.ewm(span=fast, adjust=False).mean()
    exp2 = prices.ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices, period=20, std_dev=2):
    """Calculate Bollinger Bands"""
    middle_band = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    upper_band = middle_band + (std * std_dev)
    lower_band = middle_band - (std * std_dev)
    return upper_band, middle_band, lower_band

def get_recommendation(rsi, prices):
    """Simple recommendation logic"""
    current_rsi = rsi.iloc[-1] if hasattr(rsi, 'iloc') else rsi
    current_price = prices.iloc[-1] if hasattr(prices, 'iloc') else prices
    
    if current_rsi < 30:
        return {"signal": "BUY", "reasoning": "RSI indicates oversold condition"}
    elif current_rsi > 70:
        return {"signal": "SELL", "reasoning": "RSI indicates overbought condition"}
    else:
        return {"signal": "HOLD", "reasoning": "RSI indicates neutral condition"}

def get_crypto_news(symbol="BTC", limit=5):
    """Simple mock news for demo"""
    return [
        {"title": f"Bitcoin shows strong momentum", "source": "CryptoNews", "url": "#"},
        {"title": f"Ethereum upgrades network", "source": "CryptoNews", "url": "#"},
        {"title": f"Market volatility increases", "source": "CryptoNews", "url": "#"}
    ]

def get_overall_sentiment(news):
    """Simple sentiment analysis"""
    positive_count = sum(1 for article in news if "strong" in article["title"].lower())
    negative_count = sum(1 for article in news if "volatility" in article["title"].lower())
    
    if positive_count > negative_count:
        sentiment = "positive"
    elif negative_count > positive_count:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    return {"overall": sentiment, "confidence": 0.75}

def show_main_dashboard():
    """Main dashboard"""
    # Beautiful header
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%;
                padding: 30px; border-radius: 20px; margin-bottom: 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);">
        <h1 style="text-align: center; margin: 0; color: white; font-size: 2.5em;">
            🚀 Crypto AI Dashboard
        </h1>
        <p style="text-align: center; margin: 10px 0 0 0; color: rgba(255, 255, 255, 0.9); font-size: 1.2em;">
            Multi-Agent Intelligence Platform (Deployable Version)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info and logout
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">👤 User</h3>
            <p style="margin: 5px 0 0 0; font-weight: bold;">{st.session_state.username}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #666;">
                Risk Profile: Moderate
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">📊 Status</h3>
            <p style="margin: 5px 0 0 0; font-weight: bold; color: #00ff88;">✅ Online</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar with navigation
    st.sidebar.header("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose Feature:",
        [
            "📈 Market Analysis",
            "🤖 AI Features", 
            "💼 Portfolio Tracker",
        ]
    )
    
    # Global settings in sidebar
    st.sidebar.header("⚙️ Configuration")
    crypto_symbol = st.sidebar.selectbox(
        "Select Cryptocurrency:",
        ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD", "SOL-USD", "DOGE-USD"]
    )
    
    time_period = st.sidebar.selectbox(
        "Time Period:",
        ["1mo", "3mo", "6mo", "1y", "2y"]
    )
    
    # Show selected page
    if page == "📈 Market Analysis":
        show_market_analysis(crypto_symbol, time_period)
    elif page == "🤖 AI Features":
        show_ai_features(crypto_symbol)
    elif page == "💼 Portfolio Tracker":
        show_portfolio_tracker()

def show_market_analysis(symbol, period):
    """Show market analysis"""
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="margin: 0; color: #667eea;">📈 Market Analysis</h2>
        <p style="margin: 10px 0 0 0; color: #666;">{symbol} - {period}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch data
    try:
        data = yf.download(symbol, period=period, interval='1d')
        
        if data.empty:
            st.error("No data available for this symbol/period combination")
            return
        
        # Calculate indicators
        data['RSI'] = calculate_rsi(data['Close'])
        macd_line, signal_line, histogram = calculate_macd(data['Close'])
        data['MACD'] = macd_line
        data['Signal'] = signal_line
        data['Histogram'] = histogram
        upper_band, middle_band, lower_band = calculate_bollinger_bands(data['Close'])
        data['Upper_Band'] = upper_band
        data['Middle_Band'] = middle_band
        data['Lower_Band'] = lower_band
        
        # Create candlestick chart
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                           vertical_spacing=0.03, row_heights=[0.7, 0.3])
        
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Upper_Band'],
            name='Upper Band',
            line=dict(color='rgba(255,0,0,0.5)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Lower_Band'],
            name='Lower Band',
            line=dict(color='rgba(0,255,0,0.5)')
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['RSI'],
            name='RSI',
            line=dict(color='purple')
        ), row=2, col=1)
        
        fig.update_layout(
            title=f'{symbol} Price Chart with Technical Indicators',
            xaxis_rangeslider_visible=False,
            height=800
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Get recommendation
        current_price = data['Close'].iloc[-1]
        current_rsi = data['RSI'].iloc[-1]
        recommendation = get_recommendation(current_rsi, data['Close'])
        
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">💡 Recommendation</h3>
            <p style="margin: 10px 0 0 0; font-size: 1.5em; font-weight: bold; color: {'green' if recommendation['signal'] == 'BUY' else 'red' if recommendation['signal'] == 'SELL' else 'orange'};">
                {recommendation['signal']}
            </p>
            <p style="margin: 5px 0 0 0; color: #666;">{recommendation['reasoning']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")

def show_ai_features(symbol):
    """Show AI features"""
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="margin: 0; color: #667eea;">🤖 AI Features</h2>
        <p style="margin: 10px 0 0 0; color: #666;">Sentiment Analysis & Market Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch news
    with st.spinner("Fetching latest crypto news..."):
        try:
            news = get_crypto_news(symbol.replace('-USD', ''), limit=5)
            
            if news:
                st.markdown("### 📰 Latest News")
                for article in news:
                    st.markdown(f"""
                    <div class="metric-card" style="margin-bottom: 10px;">
                        <h4 style="margin: 0; color: #667eea;">{article['title']}</h4>
                        <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #666;">
                            Source: {article['source']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Get overall sentiment
                sentiment = get_overall_sentiment(news)
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin: 0; color: #667eea;">📊 Overall Sentiment</h3>
                    <p style="margin: 10px 0 0 0; font-size: 1.5em; font-weight: bold; color: {'green' if sentiment['overall'] == 'positive' else 'red' if sentiment['overall'] == 'negative' else 'orange'};">
                        {sentiment['overall'].upper()}
                    </p>
                    <p style="margin: 5px 0 0 0; color: #666;">Confidence: {sentiment['confidence']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No news articles available at the moment")
                
        except Exception as e:
            st.error(f"Error fetching news: {str(e)}")

def show_portfolio_tracker():
    """Show portfolio tracking"""
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="margin: 0; color: #667eea;">💼 Portfolio Tracker</h2>
        <p style="margin: 10px 0 0 0; color: #666;">Manage your cryptocurrency holdings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple portfolio data
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    
    # Add holding form
    with st.expander("➕ Add Holding"):
        col1, col2, col3 = st.columns(3)
        with col1:
            symbol = st.selectbox("Symbol", ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE"])
        with col2:
            amount = st.number_input("Amount", min_value=0.0, value=0.0)
        with col3:
            price = st.number_input("Price", min_value=0.0, value=0.0)
        
        if st.button("Add to Portfolio"):
            st.session_state.portfolio.append({
                'symbol': f"{symbol}-USD",
                'amount': amount,
                'price': price,
                'value': amount * price
            })
            st.success("Holding added!")
    
    # Show portfolio
    if st.session_state.portfolio:
        st.markdown("### Your Holdings")
        for holding in st.session_state.portfolio:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 10px;">
                <h4 style="margin: 0; color: #667eea;">{holding['symbol']}</h4>
                <p style="margin: 5px 0 0 0; color: #666;">
                    Amount: {holding['amount']} | Price: ${holding['price']:.2f} | Value: ${holding['value']:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No holdings in portfolio yet")

def main():
    """Main application"""
    if not st.session_state.logged_in:
        login_page()
    else:
        show_main_dashboard()

if __name__ == "__main__":
    main()
