# 🚀 Crypto AI Dashboard

A comprehensive cryptocurrency analysis dashboard with AI-powered recommendations, technical indicators, and real-time market insights.

## 📋 Features

### ✅ Phase 1: MVP (Complete)
- **Real-time Crypto Price Fetching**: Fetch live cryptocurrency data from Yahoo Finance
- **Interactive Candlestick Charts**: Beautiful, interactive price charts with Plotly
- **Technical Indicators**: Calculate and display RSI (Relative Strength Index)
- **AI Recommendations**: Intelligent BUY/HOLD/SELL signals based on technical analysis
- **Multi-cryptocurrency Support**: Analyze BTC, ETH, BNB, XRP, ADA, SOL, DOGE and more

### 🔄 Phase 2: AI Features (In Progress)
- **News Sentiment Analysis**: Analyze market sentiment from crypto news
- **AI-Generated Summaries**: Get AI-powered market summaries
- **Interactive Chatbot**: Ask questions about cryptocurrency analysis

### 🎯 Phase 3: Advanced Features (Planned)
- Portfolio tracking
- Prediction models
- LSTM forecasting
- Multi-agent architecture
- User authentication

## 🏗️ Architecture

```
Streamlit UI (app.py)
     ↓
Python Backend
     ↓
┌─────────────────┬─────────────────┬─────────────────┐
│   Indicators    │  Recommendation │     Utils       │
│   Module        │     Engine      │   Module        │
│                 │                 │                 │
│ • RSI           │ • Buy/Hold/Sell │ • Data Fetcher  │
│ • MACD          │ • Risk Analysis │ • Validation    │
│ • Bollinger     │ • Trend Analysis│ • Caching       │
└─────────────────┴─────────────────┴─────────────────┘
     ↓
APIs + AI Modules (Phase 2)
     ↓
External Services
┌─────────────────┬─────────────────┬─────────────────┐
│  Yahoo Finance  │   News APIs     │   OpenAI API    │
│                 │                 │                 │
│ • Price Data    │ • News Articles │ • ChatGPT       │
│ • Historical    │ • Sentiment     │ • Analysis      │
│ • Real-time     │ • Summaries     │ • Q&A           │
└─────────────────┴─────────────────┴─────────────────┘
```

## 📁 Project Structure

```
crypto-ai-dashboard/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
│
├── data/                    # Data storage (cache, logs)
├── indicators/              # Technical indicators
│   ├── __init__.py
│   └── rsi.py              # RSI, MACD, Bollinger Bands
│
├── sentiment/              # Sentiment analysis (Phase 2)
│   ├── __init__.py
│   └── news_analyzer.py    # News sentiment analysis
│
├── chatbot/                # AI chatbot (Phase 2)
│   ├── __init__.py
│   └── ai_chatbot.py      # OpenAI-powered chatbot
│
├── recommendation/         # Recommendation engine
│   ├── __init__.py
│   └── engine.py          # Buy/Hold/Sell logic
│
└── utils/                  # Utility functions
    ├── __init__.py
    └── data_fetcher.py    # Data fetching utilities
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd crypto-ai-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser**
Navigate to `http://localhost:8501`

## 🎮 Usage

### Basic Analysis (Phase 1)
1. **Select Cryptocurrency**: Choose from the dropdown in the sidebar
2. **Choose Time Period**: Select analysis timeframe (1mo, 3mo, 6mo, 1y, 2y)
3. **View Charts**: Interactive candlestick charts with RSI overlay
4. **Get Recommendations**: AI-powered Buy/Hold/Sell signals with reasoning

### Advanced Features (Phase 2)
1. **News Sentiment**: Analyze market sentiment from latest crypto news
2. **AI Chatbot**: Ask questions about market analysis and get AI responses
3. **Market Summaries**: Get AI-generated market summaries

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
- **News APIs** (Phase 2): Crypto news from multiple sources
- **OpenAI API** (Phase 2): AI-powered analysis and chatbot

## 🔧 Configuration

### Environment Variables (Phase 2)
Create a `.env` file for API keys:
```env
OPENAI_API_KEY=your_openai_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

### Supported Cryptocurrencies
- Bitcoin (BTC-USD)
- Ethereum (ETH-USD)
- Binance Coin (BNB-USD)
- XRP (XRP-USD)
- Cardano (ADA-USD)
- Solana (SOL-USD)
- Dogecoin (DOGE-USD)
- And more...

## 🚀 Deployment

### Streamlit Community Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy automatically

### Render
1. Create `render.yaml` configuration
2. Connect GitHub repository
3. Deploy with one click

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📊 Development Roadmap

### Phase 1 ✅ (Complete)
- [x] Basic price fetching
- [x] Candlestick charts
- [x] RSI indicator
- [x] Basic recommendations

### Phase 2 🔄 (In Progress)
- [x] News sentiment framework
- [x] Chatbot framework
- [ ] News API integration
- [ ] OpenAI integration
- [ ] AI summaries

### Phase 3 📋 (Planned)
- [ ] Portfolio tracking
- [ ] Prediction models
- [ ] LSTM forecasting
- [ ] User authentication
- [ ] Multi-agent architecture

## ⚠️ Disclaimer

**This is not financial advice.** The dashboard provides technical analysis and AI-powered insights for educational purposes only. Always do your own research before making investment decisions. Cryptocurrency markets are highly volatile and risky.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Yahoo Finance for market data
- Streamlit for the web framework
- Plotly for interactive charts
- OpenAI for AI capabilities
- The open-source community

---

**Built with ❤️ for the crypto community**
