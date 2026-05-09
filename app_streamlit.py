"""
Streamlit-Optimized Crypto Dashboard - Lightweight Version
Works without TensorFlow and heavy ML models for deployment compatibility
"""

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
sys.path.append(os.path.join(os.path.dirname(__file__), 'portfolio'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'auth'))

# Import lightweight modules
from indicators.rsi import calculate_rsi, calculate_macd, calculate_bollinger_bands
from recommendation.engine import get_recommendation
from sentiment.news_analyzer import get_crypto_news, get_overall_sentiment
from portfolio.tracker import PortfolioTracker
from agents.market_agent import MarketAgent
from agents.indicator_agent import IndicatorAgent
from agents.sentiment_agent import SentimentAgent
from agents.advisor_agent import AdvisorAgent
from auth.auth_system import init_auth_state, require_auth, login_page, register_page, logout

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

# Initialize authentication
init_auth_state()

def main():
    """Main application with authentication and all features"""
    
    # Authentication check
    if not require_auth():
        # Show login/register page
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_page()
        
        with tab2:
            register_page()
        
        return
    
    # User is authenticated - show main dashboard
    show_main_dashboard()

def show_main_dashboard():
    """Show the main dashboard with all features"""
    
    # Beautiful header
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 30px; border-radius: 20px; margin-bottom: 20px;
                border: 2px solid rgba(255, 255, 255, 0.2);">
        <h1 style="text-align: center; margin: 0; color: white; font-size: 2.5em;">
            🚀 Crypto AI Dashboard
        </h1>
        <p style="text-align: center; margin: 10px 0 0 0; color: rgba(255, 255, 255, 0.9); font-size: 1.2em;">
            Multi-Agent Intelligence Platform (Lightweight Version)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # User info and logout
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #667eea;">👤 User</h3>
            <p style="margin: 5px 0 0 0; font-weight: bold;">{st.session_state.current_user['username']}</p>
            <p style="margin: 5px 0 0 0; font-size: 0.9em; color: #666;">
                Risk Profile: {st.session_state.current_user.get('risk_profile', 'Moderate')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
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
            "🎯 Multi-Agent Analysis",
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
    elif page == "🎯 Multi-Agent Analysis":
        show_multi_agent_analysis(crypto_symbol, time_period)

def show_market_analysis(symbol, period):
    """Show market analysis with technical indicators"""
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
    """Show AI features without heavy models"""
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
    
    # Initialize portfolio
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = PortfolioTracker()
    
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
            st.session_state.portfolio.add_holding(f"{symbol}-USD", amount, price)
            st.success("Holding added!")
    
    # Show portfolio
    portfolio = st.session_state.portfolio.get_portfolio()
    
    if portfolio['holdings']:
        st.markdown("### Your Holdings")
        for holding in portfolio['holdings']:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 10px;">
                <h4 style="margin: 0; color: #667eea;">{holding['symbol']}</h4>
                <p style="margin: 5px 0 0 0; color: #666;">
                    Amount: {holding['amount']} | Avg Price: ${holding['avg_price']:.2f}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No holdings in portfolio yet")

def show_multi_agent_analysis(symbol, period):
    """Show multi-agent analysis"""
    st.markdown(f"""
    <div class="metric-card">
        <h2 style="margin: 0; color: #667eea;">🎯 Multi-Agent Analysis</h2>
        <p style="margin: 10px 0 0 0; color: #666;">Comprehensive AI analysis from 4 specialized agents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch data
    try:
        data = yf.download(symbol, period=period, interval='1d')
        
        if data.empty:
            st.error("No data available for this symbol/period combination")
            return
        
        # Initialize agents
        market_agent = MarketAgent()
        indicator_agent = IndicatorAgent()
        sentiment_agent = SentimentAgent()
        advisor_agent = AdvisorAgent()
        
        # Get analysis from each agent
        with st.spinner("Running multi-agent analysis..."):
            market_analysis = market_agent.analyze_market(symbol, data)
            indicator_analysis = indicator_agent.analyze_indicators(data)
            sentiment_analysis = sentiment_agent.analyze_sentiment(symbol)
            advisor_analysis = advisor_agent.provide_advice(market_analysis, indicator_analysis, sentiment_analysis)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">🏦 Market Agent</h3>
                <p style="margin: 10px 0 0 0; color: #666;">Market Overview & Trends</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(market_analysis.get('overview', 'Analysis complete'))
            
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">📊 Indicator Agent</h3>
                <p style="margin: 10px 0 0 0; color: #666;">Technical Indicators</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(indicator_analysis.get('summary', 'Analysis complete'))
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">📰 Sentiment Agent</h3>
                <p style="margin: 10px 0 0 0; color: #666;">Market Sentiment</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(sentiment_analysis.get('overall_sentiment', 'Analysis complete'))
            
            st.markdown("""
            <div class="metric-card">
                <h3 style="margin: 0; color: #667eea;">💼 Advisor Agent</h3>
                <p style="margin: 10px 0 0 0; color: #666;">Investment Advice</p>
            </div>
            """, unsafe_allow_html=True)
            st.info(advisor_analysis.get('recommendation', 'Analysis complete'))
        
    except Exception as e:
        st.error(f"Error running analysis: {str(e)}")

if __name__ == "__main__":
    main()
