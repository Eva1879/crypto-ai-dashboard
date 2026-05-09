# 🚀 Crypto AI Dashboard

A comprehensive cryptocurrency analysis dashboard with AI-powered recommendations, technical indicators, and real-time market insights.

## 📋 Features

### ✅ Phase 1: Market Analysis (Complete)
- **Real-time Crypto Price Fetching**: Fetch live cryptocurrency data from Yahoo Finance
- **Interactive Candlestick Charts**: Beautiful, interactive price charts with Plotly
- **Technical Indicators**: Calculate and display RSI, MACD, Bollinger Bands
- **AI Recommendations**: Intelligent BUY/HOLD/SELL signals based on technical analysis
- **Multi-cryptocurrency Support**: Analyze BTC, ETH, BNB, XRP, ADA, SOL, DOGE and more

### ✅ Phase 2: AI Features (Complete)
- **News Sentiment Analysis**: Analyze market sentiment from crypto news using Hugging Face
- **AI-Generated Summaries**: Get AI-powered market summaries with free models
- **Interactive Chatbot**: Ask questions about cryptocurrency analysis using DistilGPT-2

### ✅ Phase 3: Advanced Features (Complete)
- **Portfolio Tracking**: Complete portfolio management with P&L tracking
- **LSTM Prediction Models**: TensorFlow/Keras neural network for price forecasting
- **Multi-Agent Architecture**: 4 specialized AI agents for comprehensive analysis
- **User Authentication**: Secure login/registration system with risk profiles

## 🏗️ Architecture

```
Streamlit UI (app_complete.py)
     ↓
Python Backend
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Indicators    │  Recommendation │   Portfolio     │
│   Module        │     Engine      │   Tracker       │
│                 │                 │                 │
│ • RSI, MACD     │ • Buy/Hold/Sell │ • Holdings      │
│ • Bollinger     │ • Risk Analysis │ • P&L Tracking  │
│ • Moving Aves   │ • Trend Analysis│ • Transactions  │
└─────────────────┴─────────────────┴─────────────────┘
     ↓
AI & Prediction Modules
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Multi-Agent   │  LSTM Models    │  Authentication │
│   Architecture  │                 │    System       │
│                 │                 │                 │
│ • Market Agent  │ • Price Forecast│ • User Login    │
│ • Indicator     │ • Neural Net    │ • Risk Profiles │
│ • Sentiment     │ • Training      │ • Session Mgmt  │
│ • Advisor       │ • Predictions   │ • Security      │
└─────────────────┴─────────────────┴─────────────────┘
     ↓
External Services
┌─────────────────┬─────────────────┬─────────────────┐
│  Yahoo Finance  │   Hugging Face  │   NewsData.io   │
│                 │                 │                 │
│ • Price Data    │ • DistilBERT    │ • News Articles │
│ • Historical    │ • DistilGPT-2   │ • Sentiment     │
│ • Real-time     │ • Free AI       │ • Analysis      │
└─────────────────┴─────────────────┴─────────────────┘
```

## 📁 Project Structure

```
crypto-ai-dashboard/
│
├── app_complete.py          # Complete application (All Phases)
├── app.py                   # Phase 1+2 application
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── render.yaml             # Render deployment configuration
│
├── data/                   # Data storage (cache, logs)
├── indicators/             # Technical indicators
│   ├── __init__.py
│   └── rsi.py             # RSI, MACD, Bollinger Bands
│
├── sentiment/             # Sentiment analysis
│   ├── __init__.py
│   └── news_analyzer.py   # News sentiment analysis
│
├── chatbot/               # AI chatbot
│   ├── __init__.py
│   └── ai_chatbot.py     # Hugging Face-powered chatbot
│
├── portfolio/             # Portfolio tracking
│   ├── __init__.py
│   └── tracker.py        # Portfolio management system
│
├── prediction/            # LSTM prediction models
│   ├── __init__.py
│   └── lstm_model.py     # TensorFlow/Keras models
│
├── agents/               # Multi-agent architecture
│   ├── __init__.py
│   ├── market_agent.py   # Market data analysis
│   ├── indicator_agent.py # Technical indicators
│   ├── sentiment_agent.py # Sentiment analysis
│   └── advisor_agent.py  # Investment advice
│
├── auth/                 # Authentication system
│   ├── __init__.py
│   └── auth_system.py    # User login/registration
│
├── recommendation/        # Recommendation engine
│   ├── __init__.py
│   └── engine.py         # Buy/Hold/Sell logic
│
└── utils/                # Utility functions
    ├── __init__.py
    └── data_fetcher.py   # Data fetching utilities
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- 4GB+ RAM recommended (for AI models)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Eva1879/crypto-ai-dashboard.git
cd crypto-ai-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app_complete.py
```

4. **Open your browser**
Navigate to `http://localhost:8501`

**Note**: First run may take 5-10 minutes as AI models download

## 🎮 Usage

### Authentication
1. **Register**: Create a new account with username, email, and password
2. **Login**: Access your personalized dashboard
3. **Risk Profile**: Set your investment risk preference (conservative/moderate/aggressive)

### Market Analysis (Phase 1)
1. **Select Cryptocurrency**: Choose from BTC, ETH, BNB, XRP, ADA, SOL, DOGE
2. **Choose Time Period**: Select analysis timeframe (1mo, 3mo, 6mo, 1y, 2y)
3. **View Charts**: Interactive candlestick charts with RSI, MACD, Volume
4. **Get Recommendations**: AI-powered Buy/Hold/Sell signals with reasoning

### AI Features (Phase 2)
1. **News Sentiment**: Analyze market sentiment from latest crypto news
2. **AI Chatbot**: Ask questions about market analysis and get AI responses
3. **Market Summaries**: Get AI-generated market summaries

### Advanced Features (Phase 3)
1. **Portfolio Tracking**: Add/remove holdings, track P&L, view performance
2. **LSTM Predictions**: Train neural networks and forecast prices
3. **Multi-Agent Analysis**: Get comprehensive analysis from 4 AI agents
4. **Risk Management**: Personalized investment advice and risk assessment

## 🧠 Technical Details

### Indicators Used
- **RSI (Relative Strength Index)**: Momentum oscillator measuring overbought/oversold conditions
- **Moving Averages**: Trend analysis using 20-day and 50-day MAs
- **Volatility Analysis**: Risk assessment based on price volatility

### Recommendation Logic
The recommendation engine considers:
- **RSI Levels**: Overbought (>70) → SELL, Oversold (<30) → BUY
- **Trend Analysis**: Confirmed uptrends/downtrends
- **Price Action**: Recent price movements and momentum
- **Volatility**: Risk assessment and position sizing suggestions

### Data Sources
- **Yahoo Finance API**: Real-time and historical price data
- **NewsData.io API**: Crypto news from multiple sources (free tier)
- **Hugging Face**: Free AI models (DistilBERT, DistilGPT-2)

## 🔧 Configuration

### Environment Variables
Create a `.env` file for API keys:
```env
NEWS_API_KEY=pub_cb7a7f66947c4fdbb107797493a185a4
```

**Note**: Uses free APIs and local AI models - no paid services required!

### Supported Cryptocurrencies
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)
- Binance Coin (BNB-USD)
- XRP (XRP-USD)
- Cardano (ADA-USD)
- Solana (SOL-USD)
- Dogecoin (DOGE-USD)
- And more...

## 🚀 Getting Started

### Local Development (Recommended)
```bash
# Clone the repository
git clone https://github.com/Eva1879/crypto-ai-dashboard.git
cd crypto-ai-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app_complete.py

# Access at: http://localhost:8501
```

### Prerequisites
- Python 3.8+
- pip package manager
- 4GB+ RAM recommended (for AI models)

### Installation Notes
- TensorFlow/Keras may take 5-10 minutes to install
- Hugging Face models download on first run
- Total installation time: 10-15 minutes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📊 Development Status

### ✅ All Phases Complete

#### Phase 1: Market Analysis ✅
- [x] Real-time price fetching from Yahoo Finance
- [x] Interactive candlestick charts with Plotly
- [x] Technical indicators (RSI, MACD, Bollinger Bands)
- [x] AI-powered Buy/Hold/Sell recommendations
- [x] Multi-cryptocurrency support

#### Phase 2: AI Features ✅
- [x] News sentiment analysis using Hugging Face DistilBERT
- [x] AI chatbot using DistilGPT-2 (free models)
- [x] Market summaries and insights
- [x] Free API integration (NewsData.io)

#### Phase 3: Advanced Features ✅
- [x] Portfolio tracking with P&L management
- [x] LSTM neural network price prediction
- [x] Multi-agent architecture (4 specialized agents)
- [x] User authentication with risk profiles
- [x] Complete deployment configuration

## ⚠️ Disclaimer

**This is not financial advice.** The dashboard provides technical analysis and AI-powered insights for educational purposes only. Always do your own research before making investment decisions. Cryptocurrency markets are highly volatile and risky.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Yahoo Finance** for real-time market data
- **Streamlit** for the web framework
- **Plotly** for interactive charts
- **Hugging Face** for free AI models (DistilBERT, DistilGPT-2)
- **NewsData.io** for free news API
- **TensorFlow/Keras** for neural network capabilities
- **The open-source community** for making this project possible

---

**Built with ❤️ for the crypto community**
