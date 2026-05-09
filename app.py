import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import sys
import os

# Add project directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'indicators'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'sentiment'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'chatbot'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'recommendation'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import our modules
from indicators.rsi import calculate_rsi
from recommendation.engine import get_recommendation
from sentiment.news_analyzer import get_crypto_news, get_overall_sentiment
from chatbot.ai_chatbot import CryptoChatbot
from portfolio.tracker import PortfolioTracker
from prediction.lstm_model import LSTMPredictor
from agents.market_agent import MarketAgent
from agents.indicator_agent import IndicatorAgent
from agents.sentiment_agent import SentimentAgent
from agents.advisor_agent import AdvisorAgent
from auth.auth_system import init_auth_state, require_auth, login_page, register_page, logout

st.set_page_config(
    page_title="Crypto AI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 Crypto AI Dashboard")
st.markdown("Real-time cryptocurrency analysis with AI-powered recommendations")

# Sidebar for cryptocurrency selection
st.sidebar.header("📊 Configuration")
crypto_symbol = st.sidebar.selectbox(
    "Select Cryptocurrency",
    ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD", "SOL-USD", "DOGE-USD"],
    index=0
)

time_period = st.sidebar.selectbox(
    "Time Period",
    ["1mo", "3mo", "6mo", "1y", "2y"],
    index=2
)

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.header(f"📈 {crypto_symbol} Price Chart")
    
    # Fetch data
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def fetch_crypto_data(symbol, period):
        try:
            data = yf.download(symbol, period=period, interval="1d")
            return data
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None
    
    data = fetch_crypto_data(crypto_symbol, time_period)
    
    if data is not None and not data.empty:
        # Create candlestick chart
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=(f'{crypto_symbol} Price', 'RSI'),
            row_width=[0.2, 0.7]
        )
        
        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Calculate and add RSI
        rsi = calculate_rsi(data['Close'])
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=rsi,
                name='RSI',
                line=dict(color='purple')
            ),
            row=2, col=1
        )
        
        # Add RSI overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        fig.update_layout(
            title=f'{crypto_symbol} Technical Analysis',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("Unable to fetch cryptocurrency data. Please try again.")

with col2:
    st.header("🤖 AI Recommendation")
    
    if data is not None and not data.empty:
        # Get current price and RSI
        current_price = data['Close'].iloc[-1]
        current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
        
        # Get recommendation
        recommendation = get_recommendation(current_rsi, data)
        
        # Display recommendation with color
        if recommendation['action'] == 'BUY':
            st.success(f"## 🟢 {recommendation['action']}")
        elif recommendation['action'] == 'SELL':
            st.error(f"## 🔴 {recommendation['action']}")
        else:
            st.warning(f"## 🟡 {recommendation['action']}")
        
        st.write("**Reasoning:**")
        st.write(recommendation['reasoning'])
        
        st.write("**Current Metrics:**")
        st.write(f"• Price: ${current_price:.2f}")
        st.write(f"• RSI: {current_rsi:.2f}")
        st.write(f"• 24h Change: {((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1) * 100):.2f}%")

# Phase 2: Market Sentiment & News Analysis
st.header("📰 Market Sentiment & News")
col3, col4 = st.columns([2, 1])

# Initialize chatbot
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = CryptoChatbot()

with col3:
    st.subheader("Latest News & Sentiment Analysis")
    
    # Fetch and analyze news
    with st.spinner("Fetching latest crypto news..."):
        news_articles = get_crypto_news(crypto_symbol.replace('-USD', ''), limit=5)
        overall_sentiment = get_overall_sentiment(news_articles)
    
    # Display overall sentiment
    sentiment_color = {
        'positive': '🟢',
        'negative': '🔴', 
        'neutral': '🟡'
    }
    
    st.markdown(f"### Overall Market Sentiment: {sentiment_color.get(overall_sentiment['overall_sentiment'], '🟡')} {overall_sentiment['overall_sentiment'].upper()}")
    st.write(f"**Sentiment Score:** {overall_sentiment['average_polarity']:.3f}")
    st.write(f"**Articles Analyzed:** {overall_sentiment['total_articles']}")
    
    # Display individual articles
    st.write("**Latest News Articles:**")
    for i, article in enumerate(news_articles, 1):
        with st.expander(f"{i}. {article['title']} - {article['source']}"):
            st.write(f"**Source:** {article['source']}")
            st.write(f"**Date:** {article['published_date']}")
            if article.get('description'):
                st.write(f"**Summary:** {article['description']}")
            if article.get('url') and article['url'] != 'https://example.com':
                st.write(f"**Link:** [{article['url']}]({article['url']})")

with col4:
    st.subheader("💬 AI Chatbot")
    
    # Chatbot interface
    user_question = st.text_input(
        "Ask about crypto analysis:",
        placeholder="e.g., What does the current RSI indicate?",
        key="chat_question"
    )
    
    if st.button("Ask AI", key="ask_ai_button") and user_question:
        with st.spinner("AI thinking..."):
            context = st.session_state.chatbot.get_crypto_context(
                crypto_symbol, data, rsi, recommendation
            )
            response = st.session_state.chatbot.ask_question(user_question, context)
            
            st.success("🤖 AI Response:")
            st.write(response)
    
    # Suggested questions
    with st.expander("💡 Suggested Questions"):
        suggested = st.session_state.chatbot.get_suggested_questions()
        for i, question in enumerate(suggested[:4], 1):  # Show first 4
            if st.button(question, key=f"suggest_{i}", use_container_width=True):
                st.session_state.chat_question = question
                st.rerun()

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** This dashboard provides real-time cryptocurrency analysis with technical indicators and AI-powered recommendations. Select different cryptocurrencies and time periods from the sidebar to customize your analysis.")
