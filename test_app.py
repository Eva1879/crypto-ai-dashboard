"""
Test script for Crypto AI Dashboard
This script tests all major components before deployment.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test all module imports"""
    print("🧪 Testing Module Imports...")
    
    try:
        # Phase 1 imports
        from indicators.rsi import calculate_rsi
        from recommendation.engine import get_recommendation
        print("✅ Phase 1 modules imported successfully")
        
        # Phase 2 imports
        from sentiment.news_analyzer import get_crypto_news, get_overall_sentiment
        from chatbot.ai_chatbot import CryptoChatbot
        print("✅ Phase 2 modules imported successfully")
        
        # Phase 3 imports
        from portfolio.tracker import PortfolioTracker
        from prediction.lstm_model import LSTMPredictor
        from agents.market_agent import MarketAgent
        from agents.indicator_agent import IndicatorAgent
        from agents.sentiment_agent import SentimentAgent
        from agents.advisor_agent import AdvisorAgent
        from auth.auth_system import AuthSystem
        print("✅ Phase 3 modules imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_fetching():
    """Test data fetching functionality"""
    print("\n📊 Testing Data Fetching...")
    
    try:
        import yfinance as yf
        import pandas as pd
        
        # Test fetching BTC data
        data = yf.download("BTC-USD", period="1mo", interval="1d")
        
        if data.empty:
            print("❌ No data fetched")
            return False
        
        print(f"✅ Successfully fetched {len(data)} days of data")
        print(f"   - Latest price: ${data['Close'].iloc[-1]:.2f}")
        print(f"   - Date range: {data.index[0]} to {data.index[-1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data fetching error: {e}")
        return False

def test_technical_indicators():
    """Test technical indicators"""
    print("\n📈 Testing Technical Indicators...")
    
    try:
        import yfinance as yf
        from indicators.rsi import calculate_rsi, calculate_macd
        
        # Get test data
        data = yf.download("BTC-USD", period="3mo", interval="1d")
        
        if not data.empty:
            # Test RSI
            rsi = calculate_rsi(data['Close'])
            current_rsi = rsi.iloc[-1]
            print(f"✅ RSI calculated: {current_rsi:.2f}")
            
            # Test MACD
            macd_line, signal_line, histogram = calculate_macd(data['Close'])
            print(f"✅ MACD calculated successfully")
            
            # Test recommendation engine
            from recommendation.engine import get_recommendation
            recommendation = get_recommendation(current_rsi, data)
            print(f"✅ Recommendation: {recommendation['action']}")
            
            return True
        
    except Exception as e:
        print(f"❌ Technical indicators error: {e}")
        return False

def test_portfolio_tracker():
    """Test portfolio tracking"""
    print("\n💼 Testing Portfolio Tracker...")
    
    try:
        from portfolio.tracker import PortfolioTracker
        
        # Create portfolio tracker
        portfolio = PortfolioTracker("test_portfolio.json")
        print("✅ Portfolio tracker initialized")
        
        # Test adding holding
        portfolio.add_holding("BTC", 0.1, 50000, "2024-01-01")
        print("✅ Holding added successfully")
        
        # Test portfolio value calculation
        current_prices = {"BTC-USD": 55000}
        portfolio_value = portfolio.get_portfolio_value(current_prices)
        print(f"✅ Portfolio value calculated: ${portfolio_value['total_value']:.2f}")
        
        # Clean up test file
        import os
        if os.path.exists("test_portfolio.json"):
            os.remove("test_portfolio.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio tracker error: {e}")
        return False

def test_ai_components():
    """Test AI components"""
    print("\n🤖 Testing AI Components...")
    
    try:
        # Test chatbot
        from chatbot.ai_chatbot import CryptoChatbot
        chatbot = CryptoChatbot()
        print("✅ Chatbot initialized")
        
        # Test sentiment analysis
        from sentiment.news_analyzer import analyze_sentiment
        sentiment = analyze_sentiment("Bitcoin is showing strong bullish momentum today")
        print(f"✅ Sentiment analysis: {sentiment['classification']}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI components error: {e}")
        return False

def test_authentication():
    """Test authentication system"""
    print("\n🔐 Testing Authentication System...")
    
    try:
        from auth.auth_system import AuthSystem
        
        # Create test auth system
        auth = AuthSystem("test_users.json")
        print("✅ Auth system initialized")
        
        # Test user registration
        result = auth.register_user("testuser", "test@example.com", "testpass123", "moderate")
        if result['success']:
            print("✅ User registration successful")
        
        # Test user login
        login_result = auth.login_user("testuser", "testpass123")
        if login_result['success']:
            print("✅ User login successful")
        
        # Clean up test file
        import os
        if os.path.exists("test_users.json"):
            os.remove("test_users.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Crypto AI Dashboard - Testing Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_data_fetching,
        test_technical_indicators,
        test_portfolio_tracker,
        test_ai_components,
        test_authentication
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for deployment.")
        return True
    else:
        print("⚠️  Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
