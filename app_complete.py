"""
Complete Crypto AI Dashboard - All Phases
This is the complete application with Phase 1, 2, and 3 features.
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
import time

# Add project directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'indicators'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'sentiment'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'chatbot'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'recommendation'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'portfolio'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'prediction'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'auth'))

# Import all modules
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
    page_title="Complete Crypto AI Dashboard",
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
    
    # User info and logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"🚀 Complete Crypto AI Dashboard")
        st.markdown(f"Welcome back, **{st.session_state.current_user['username']}**!")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Sidebar with navigation
    st.sidebar.header("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose Feature:",
        [
            "📈 Market Analysis (Phase 1)",
            "🤖 AI Features (Phase 2)", 
            "💼 Portfolio Tracker (Phase 3)",
            "🔮 Price Prediction (Phase 3)",
            "🎯 Multi-Agent Analysis (Phase 3)",
            "⚙️ Settings"
        ]
    )
    
    # Global settings in sidebar
    st.sidebar.header("⚙️ Configuration")
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
    
    # Risk profile from user settings
    risk_profile = st.session_state.current_user.get('risk_profile', 'moderate')
    
    # Show selected page
    if page == "📈 Market Analysis (Phase 1)":
        show_market_analysis(crypto_symbol, time_period)
    elif page == "🤖 AI Features (Phase 2)":
        show_ai_features(crypto_symbol, time_period)
    elif page == "💼 Portfolio Tracker (Phase 3)":
        show_portfolio_tracker(crypto_symbol)
    elif page == "🔮 Price Prediction (Phase 3)":
        show_price_prediction(crypto_symbol, time_period)
    elif page == "🎯 Multi-Agent Analysis (Phase 3)":
        show_multi_agent_analysis(crypto_symbol, time_period, risk_profile)
    elif page == "⚙️ Settings":
        show_settings()

def show_market_analysis(crypto_symbol, time_period):
    """Phase 1: Market Analysis with technical indicators"""
    
    st.header("📈 Market Analysis & Technical Indicators")
    
    # Fetch data with caching
    @st.cache_data(ttl=300)
    def fetch_crypto_data(symbol, period):
        try:
            data = yf.download(symbol, period=period, interval="1d")
            return data
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None
    
    data = fetch_crypto_data(crypto_symbol, time_period)
    
    if data is not None and not data.empty:
        # Create comprehensive chart
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(
                f'{crypto_symbol} Price Chart',
                'RSI',
                'MACD',
                'Volume'
            ),
            row_heights=[0.5, 0.15, 0.15, 0.2]
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
        
        # RSI
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
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        # MACD
        macd_line, signal_line, histogram = calculate_macd(data['Close'])
        fig.add_trace(
            go.Scatter(x=data.index, y=macd_line, name='MACD', line=dict(color='blue')),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=signal_line, name='Signal', line=dict(color='red')),
            row=3, col=1
        )
        
        # Volume
        if 'Volume' in data.columns:
            fig.add_trace(
                go.Bar(x=data.index, y=data['Volume'], name='Volume'),
                row=4, col=1
            )
        
        fig.update_layout(
            title=f'{crypto_symbol} Complete Technical Analysis',
            height=800,
            xaxis_rangeslider_visible=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations and metrics
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🤖 AI Recommendations")
            current_price = data['Close'].iloc[-1]
            current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
            
            recommendation = get_recommendation(current_rsi, data)
            
            if recommendation['action'] == 'BUY':
                st.success(f"## 🟢 {recommendation['action']}")
            elif recommendation['action'] == 'SELL':
                st.error(f"## 🔴 {recommendation['action']}")
            else:
                st.warning(f"## 🟡 {recommendation['action']}")
            
            st.write("**Reasoning:**")
            st.write(recommendation['reasoning'])
        
        with col2:
            st.subheader("📊 Current Metrics")
            st.write(f"• **Price:** ${current_price:.2f}")
            st.write(f"• **RSI:** {current_rsi:.2f}")
            st.write(f"• **24h Change:** {((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1) * 100):.2f}%")
            st.write(f"• **Volume:** {data['Volume'].iloc[-1]:,.0f}")
            st.write(f"• **Volatility:** {data['Close'].pct_change().std() * 100:.2f}%")

def show_ai_features(crypto_symbol, time_period):
    """Phase 2: AI Features including sentiment and chatbot"""
    
    st.header("🤖 AI-Powered Features")
    
    # Initialize AI components
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = CryptoChatbot()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📰 Market Sentiment Analysis")
        
        # Fetch and analyze news
        with st.spinner("Fetching latest crypto news..."):
            news_articles = get_crypto_news(crypto_symbol.replace('-USD', ''), limit=5)
            overall_sentiment = get_overall_sentiment(news_articles)
        
        # Display sentiment
        sentiment_color = {
            'positive': '🟢',
            'negative': '🔴', 
            'neutral': '🟡'
        }
        
        st.markdown(f"### Overall Market Sentiment: {sentiment_color.get(overall_sentiment['overall_sentiment'], '🟡')} {overall_sentiment['overall_sentiment'].upper()}")
        st.write(f"**Sentiment Score:** {overall_sentiment['average_polarity']:.3f}")
        st.write(f"**Articles Analyzed:** {overall_sentiment['total_articles']}")
        
        # Display articles
        st.write("**Latest News Articles:**")
        for i, article in enumerate(news_articles, 1):
            with st.expander(f"{i}. {article['title']} - {article['source']}"):
                st.write(f"**Source:** {article['source']}")
                st.write(f"**Date:** {article['published_date']}")
                if article.get('description'):
                    st.write(f"**Summary:** {article['description']}")
    
    with col2:
        st.subheader("💬 AI Chatbot")
        
        user_question = st.text_input(
            "Ask about crypto analysis:",
            placeholder="e.g., What does the current RSI indicate?",
            key="chat_question"
        )
        
        if st.button("Ask AI", key="ask_ai_button") and user_question:
            with st.spinner("AI thinking..."):
                # Get context for the chatbot
                data = yf.download(crypto_symbol, period="1mo", interval="1d")
                if not data.empty:
                    rsi = calculate_rsi(data['Close'])
                    current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
                    recommendation = get_recommendation(current_rsi, data)
                    
                    context = st.session_state.chatbot.get_crypto_context(
                        crypto_symbol, data, current_rsi, recommendation
                    )
                    response = st.session_state.chatbot.ask_question(user_question, context)
                    
                    st.success("🤖 AI Response:")
                    st.write(response)
        
        # Suggested questions
        with st.expander("💡 Suggested Questions"):
            suggested = st.session_state.chatbot.get_suggested_questions()
            for i, question in enumerate(suggested[:4], 1):
                if st.button(question, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.chat_question = question
                    st.rerun()

def show_portfolio_tracker(crypto_symbol):
    """Phase 3: Portfolio tracking"""
    
    st.header("💼 Portfolio Tracker")
    
    # Initialize portfolio tracker
    if 'portfolio_tracker' not in st.session_state:
        st.session_state.portfolio_tracker = PortfolioTracker()
    
    portfolio = st.session_state.portfolio_tracker
    
    # Portfolio management tabs
    tab1, tab2, tab3 = st.tabs(["📊 Portfolio Overview", "➕ Add Transaction", "📈 Performance"])
    
    with tab1:
        st.subheader("Current Portfolio")
        
        # Get current prices
        current_prices = {}
        try:
            ticker = yf.Ticker(crypto_symbol)
            current_prices[crypto_symbol] = ticker.history(period="1d")['Close'].iloc[-1]
        except:
            current_prices[crypto_symbol] = 0
        
        portfolio_value = portfolio.get_portfolio_value(current_prices)
        
        if portfolio_value['holdings']:
            # Display portfolio summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Value", f"${portfolio_value['total_value']:.2f}")
            
            with col2:
                st.metric("Total Invested", f"${portfolio_value['total_invested']:.2f}")
            
            with col3:
                profit_loss = portfolio_value['total_profit_loss']
                st.metric("Total P&L", f"${profit_loss:.2f}", 
                         f"{portfolio_value['total_profit_loss_percent']:.2f}%")
            
            with col4:
                st.metric("Number of Holdings", portfolio_value['number_of_holdings'])
            
            # Display individual holdings
            st.write("**Holdings Details:**")
            for symbol, holding in portfolio_value['holdings'].items():
                with st.expander(f"{symbol} - {holding['amount']:.6f} units"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Current Price:** ${holding['current_price']:.2f}")
                        st.write(f"**Value:** ${holding['value']:.2f}")
                        st.write(f"**Invested:** ${holding['invested']:.2f}")
                    with col2:
                        st.write(f"**P&L:** ${holding['profit_loss']:.2f}")
                        st.write(f"**P&L %:** {holding['profit_loss_percent']:.2f}%")
                        st.write(f"**Avg Buy Price:** ${holding['average_buy_price']:.2f}")
        else:
            st.info("No holdings in portfolio yet. Add your first transaction!")
    
    with tab2:
        st.subheader("Add Transaction")
        
        trans_type = st.selectbox("Transaction Type", ["Buy", "Sell"])
        symbol = st.text_input("Symbol", value=crypto_symbol.replace('-USD', ''))
        amount = st.number_input("Amount", min_value=0.0, step=0.000001, format="%.6f")
        price = st.number_input("Price per Unit", min_value=0.0, step=0.01, format="%.2f")
        
        if st.button("Add Transaction"):
            if trans_type == "Buy":
                if portfolio.add_holding(symbol, amount, price):
                    st.success(f"Added {amount} {symbol} at ${price}")
                    st.rerun()
            else:
                if portfolio.remove_holding(symbol, amount, price):
                    st.success(f"Sold {amount} {symbol} at ${price}")
                    st.rerun()
    
    with tab3:
        st.subheader("Transaction History")
        
        transactions = portfolio.get_transaction_history()
        if not transactions.empty:
            st.dataframe(transactions, use_container_width=True)
        else:
            st.info("No transactions yet")

def show_price_prediction(crypto_symbol, time_period):
    """Phase 3: LSTM Price Prediction"""
    
    st.header("🔮 AI Price Prediction")
    
    # Initialize LSTM predictor
    if 'lstm_predictor' not in st.session_state:
        st.session_state.lstm_predictor = LSTMPredictor()
    
    predictor = st.session_state.lstm_predictor
    
    # Get historical data
    try:
        data = yf.download(crypto_symbol, period="2y", interval="1d")
        
        if len(data) < 100:
            st.error("Insufficient historical data for prediction. Need at least 100 days.")
            return
        
        # Train or load model
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Model Training")
            
            if st.button("🚀 Train New Model"):
                with st.spinner("Training LSTM model... This may take a few minutes."):
                    try:
                        results = predictor.train(data, epochs=20, lookback=60)
                        st.success("Model trained successfully!")
                        
                        # Display training metrics
                        metrics = results['metrics']
                        st.write("**Training Metrics:**")
                        st.write(f"• Train MAE: {metrics['train_mae']:.4f}")
                        st.write(f"• Test MAE: {metrics['test_mae']:.4f}")
                        st.write(f"• Train RMSE: {metrics['train_rmse']:.4f}")
                        st.write(f"• Test RMSE: {metrics['test_rmse']:.4f}")
                        st.write(f"• Test MAPE: {metrics['test_mape']:.2f}%")
                    except Exception as e:
                        st.error(f"Error training model: {e}")
        
        with col2:
            st.subheader("Model Info")
            model_info = predictor.get_model_summary()
            st.write(model_info)
        
        # Make predictions
        st.subheader("Price Predictions")
        
        days_ahead = st.slider("Days to Predict", 1, 30, 7)
        
        if st.button("🔮 Generate Predictions"):
            with st.spinner("Generating predictions..."):
                try:
                    predictions = predictor.predict(data, days_ahead=days_ahead)
                    
                    # Display predictions
                    st.write("**Predicted Prices:**")
                    
                    pred_df = pd.DataFrame({
                        'Day': range(1, days_ahead + 1),
                        'Predicted Price': predictions['predictions'],
                        'Lower Bound': [ci[0] for ci in predictions['confidence_intervals']],
                        'Upper Bound': [ci[1] for ci in predictions['confidence_intervals']]
                    })
                    
                    st.dataframe(pred_df, use_container_width=True)
                    
                    # Plot predictions
                    fig = go.Figure()
                    
                    # Historical prices
                    fig.add_trace(go.Scatter(
                        x=data.index[-30:],  # Last 30 days
                        y=data['Close'].iloc[-30:],
                        mode='lines',
                        name='Historical Price',
                        line=dict(color='blue')
                    ))
                    
                    # Predictions
                    future_dates = pd.date_range(
                        start=data.index[-1] + timedelta(days=1),
                        periods=days_ahead,
                        freq='D'
                    )
                    
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=predictions['predictions'],
                        mode='lines+markers',
                        name='Predicted Price',
                        line=dict(color='red', dash='dash')
                    ))
                    
                    # Confidence intervals
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=[ci[1] for ci in predictions['confidence_intervals']],
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=[ci[0] for ci in predictions['confidence_intervals']],
                        mode='lines',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(255,0,0,0.2)',
                        name='Confidence Interval',
                        showlegend=True
                    ))
                    
                    fig.update_layout(
                        title=f'{crypto_symbol} Price Prediction - Next {days_ahead} Days',
                        xaxis_title='Date',
                        yaxis_title='Price (USD)',
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Model performance disclaimer
                    st.warning("⚠️ **Disclaimer:** These predictions are for educational purposes only and should not be used for making financial decisions. Cryptocurrency markets are highly volatile and unpredictable.")
                    
                except Exception as e:
                    st.error(f"Error generating predictions: {e}")
    
    except Exception as e:
        st.error(f"Error loading data: {e}")

def show_multi_agent_analysis(crypto_symbol, time_period, risk_profile):
    """Phase 3: Multi-Agent Analysis"""
    
    st.header("🎯 Multi-Agent Analysis")
    
    # Initialize agents
    if 'market_agent' not in st.session_state:
        st.session_state.market_agent = MarketAgent()
        st.session_state.indicator_agent = IndicatorAgent()
        st.session_state.sentiment_agent = SentimentAgent()
        st.session_state.advisor_agent = AdvisorAgent()
    
    market_agent = st.session_state.market_agent
    indicator_agent = st.session_state.indicator_agent
    sentiment_agent = st.session_state.sentiment_agent
    advisor_agent = st.session_state.advisor_agent
    
    # Run multi-agent analysis
    with st.spinner("Running comprehensive multi-agent analysis..."):
        try:
            # Get market data
            market_data = market_agent.fetch_market_data(crypto_symbol, time_period)
            market_summary = market_agent.get_market_summary(crypto_symbol)
            
            if market_data is not None and not market_data.empty:
                # Agent analyses
                indicators = indicator_agent.calculate_all_indicators(market_data)
                indicator_signals = indicator_agent.get_indicator_signals(market_data)
                
                sentiment_analysis = sentiment_agent.analyze_news_sentiment(crypto_symbol.replace('-USD', ''))
                
                # Generate comprehensive advice
                advice = advisor_agent.generate_investment_advice(
                    market_summary, indicators, sentiment_analysis, risk_profile
                )
                
                # Display results
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📊 Agent Analysis Results")
                    
                    # Market Agent
                    with st.expander("🏦 Market Agent Analysis"):
                        st.write("**Market Summary:**")
                        st.json(market_summary)
                    
                    # Indicator Agent
                    with st.expander("📈 Indicator Agent Analysis"):
                        st.write("**Technical Signals:**")
                        st.json(indicator_signals)
                    
                    # Sentiment Agent
                    with st.expander("💭 Sentiment Agent Analysis"):
                        st.write("**Market Sentiment:**")
                        st.json(sentiment_analysis)
                
                with col2:
                    st.subheader("🎯 Advisor Agent Recommendation")
                    
                    overall_rec = advice['overall_recommendation']
                    
                    if overall_rec['action'] == 'BUY':
                        st.success(f"## 🟢 {overall_rec['action']}")
                    elif overall_rec['action'] == 'SELL':
                        st.error(f"## 🔴 {overall_rec['action']}")
                    else:
                        st.warning(f"## 🟡 {overall_rec['action']}")
                    
                    st.write(f"**Confidence:** {overall_rec['confidence']:.2f}")
                    st.write(f"**Reasoning:** {overall_rec['reasoning']}")
                    st.write(f"**Risk Level:** {overall_rec['risk_level']}")
                    
                    # Risk management
                    risk_mgmt = advice['risk_management']
                    st.write("**Risk Management:**")
                    st.write(f"• Stop Loss: ${risk_mgmt['stop_loss']:.2f}")
                    st.write(f"• Take Profit: ${risk_mgmt['take_profit']:.2f}")
                    st.write(f"• Risk/Reward Ratio: {risk_mgmt['risk_reward_ratio']:.2f}")
                    
                    # Position sizing
                    position = advice['position_sizing']
                    st.write("**Position Sizing:**")
                    st.write(f"• Recommended Allocation: {position['recommended_allocation']:.1%}")
                    st.write(f"• Risk Amount: ${position['risk_amount']:.2f}")
                
                # Educational content
                st.subheader("📚 Educational Insights")
                topic = st.selectbox("Learn More:", ["risk_management", "technical_analysis", "sentiment_analysis"])
                edu_content = advisor_agent.get_educational_content(topic)
                
                st.write(f"**{edu_content['title']}**")
                for point in edu_content['content']:
                    st.write(f"• {point}")
                
                # Disclaimer
                st.warning("⚠️ **Disclaimer:** This analysis is for educational purposes only and should not be considered financial advice. Always do your own research before making investment decisions.")
                
            else:
                st.error("Unable to fetch market data for analysis.")
        
        except Exception as e:
            st.error(f"Error in multi-agent analysis: {e}")

def show_settings():
    """User settings page"""
    
    st.header("⚙️ Settings")
    
    tab1, tab2 = st.tabs(["👤 Profile Settings", "🔧 System Settings"])
    
    with tab1:
        st.subheader("User Profile")
        
        user_data = st.session_state.current_user
        
        st.write(f"**Username:** {user_data['username']}")
        st.write(f"**Email:** {user_data['email']}")
        
        # Update risk profile
        new_risk_profile = st.selectbox(
            "Risk Profile",
            ["conservative", "moderate", "aggressive"],
            index=["conservative", "moderate", "aggressive"].index(user_data.get('risk_profile', 'moderate'))
        )
        
        if st.button("Update Risk Profile"):
            # Update user preferences
            st.session_state.auth_system.update_user_preferences(
                user_data['username'],
                {'risk_profile': new_risk_profile}
            )
            st.session_state.current_user['risk_profile'] = new_risk_profile
            st.success("Risk profile updated!")
            st.rerun()
    
    with tab2:
        st.subheader("System Settings")
        
        st.write("**Application Features:**")
        st.write("✅ Phase 1: Market Analysis & Technical Indicators")
        st.write("✅ Phase 2: AI Features (Sentiment & Chatbot)")
        st.write("✅ Phase 3: Advanced Features (Portfolio, Prediction, Multi-Agent)")
        
        st.write("**Data Sources:**")
        st.write("• Yahoo Finance (Market Data)")
        st.write("• NewsData.io (News Sentiment)")
        st.write("• Hugging Face (AI Models)")
        
        st.write("**Model Information:**")
        st.write("• Sentiment Analysis: DistilBERT")
        st.write("• Text Generation: DistilGPT-2")
        st.write("• Price Prediction: LSTM Neural Network")

if __name__ == "__main__":
    main()
