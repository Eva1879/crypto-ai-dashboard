# 🚀 Crypto AI Dashboard - Quick Start Commands

## 📋 Prerequisites Installation

### Install Git (if not installed)
```bash
# Download Git from: https://git-scm.com/download/win
# Or use Chocolatey (if installed):
choco install git

# Or use Windows Package Manager:
winget install --id Git.Git -e --source winget
```

### Verify Installation
```bash
# Check Git version
git --version

# Check Python version
python --version

# Check Streamlit
streamlit --version
```

---

## 🧪 Testing Commands (Run in Order)

### 1. Environment Setup
```bash
# Navigate to project directory
cd C:\Users\grace\CascadeProjects\crypto-ai-dashboard

# Install dependencies
pip install -r requirements.txt

# Fix TensorFlow compatibility
pip install tf-keras

# Create data directory
mkdir data
```

### 2. Frontend Testing (Streamlit)
```bash
# Test main application (all phases)
streamlit run app_complete.py

# Test Phase 1+2 only
streamlit run app.py

# Access in browser: http://localhost:8501
```

### 3. Backend Testing (API Calls)
```bash
# Test data fetching
python -c "
import yfinance as yf
data = yf.download('BTC-USD', period='1mo')
print(f'✅ Fetched {len(data)} days')
print(f'Latest price: ${data.Close.iloc[-1]:.2f}')
"

# Test sentiment analysis
python -c "
from sentiment.news_analyzer import analyze_sentiment
result = analyze_sentiment('Bitcoin is showing strong bullish momentum')
print(f'✅ Sentiment: {result[\"classification\"]}')
"

# Test portfolio tracker
python -c "
from portfolio.tracker import PortfolioTracker
portfolio = PortfolioTracker()
portfolio.add_holding('BTC', 0.1, 50000)
print('✅ Portfolio tracker working')
"

# Test authentication
python -c "
from auth.auth_system import AuthSystem
auth = AuthSystem()
result = auth.register_user('testuser', 'test@example.com', 'testpass123', 'moderate')
print(f'✅ Auth system: {result[\"success\"]}')
"
```

### 4. AI Components Testing
```bash
# Test chatbot
python -c "
from chatbot.ai_chatbot import CryptoChatbot
chatbot = CryptoChatbot()
response = chatbot.ask_question('What is RSI?')
print(f'✅ Chatbot: {response[:50]}...')"

# Test LSTM predictor
python -c "
from prediction.lstm_model import LSTMPredictor
predictor = LSTMPredictor()
print('✅ LSTM predictor initialized')"

# Test multi-agent system
python -c "
from agents.market_agent import MarketAgent
from agents.indicator_agent import IndicatorAgent
market_agent = MarketAgent()
indicator_agent = IndicatorAgent()
print('✅ Multi-agent system working')
"
```

---

## 🔧 Git Repository Setup

### 1. Initialize Git Repository
```bash
# Navigate to project directory
cd C:\Users\grace\CascadeProjects\crypto-ai-dashboard

# Initialize Git repository
git init

# Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Create .gitignore File
```bash
# Create .gitignore
echo "# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Data files
data/
*.json
*.pkl
*.h5

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db" > .gitignore
```

### 3. Add Files and Commit
```bash
# Add all files
git add .

# Check status
git status

# Create initial commit
git commit -m "Initial commit: Complete Crypto AI Dashboard

Features:
- Phase 1: Market analysis, technical indicators, recommendations
- Phase 2: AI features, sentiment analysis, chatbot (free alternatives)
- Phase 3: Portfolio tracking, LSTM prediction, multi-agent architecture, authentication

Tech Stack:
- Frontend: Streamlit
- Backend: Python
- AI: Hugging Face Transformers (free), TensorFlow/Keras
- Data: Yahoo Finance, NewsData.io
- Auth: Custom authentication system"
```

---

## 📤 GitHub Push Commands

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Repository name: `crypto-ai-dashboard`
4. Description: `Complete cryptocurrency AI dashboard with technical analysis, sentiment analysis, portfolio tracking, and price prediction`
5. Make it **Public**
6. **DO NOT** initialize with README
7. Click "Create repository"

### 2. Push to GitHub
```bash
# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/crypto-ai-dashboard.git

# Push to GitHub
git push -u origin main

# If you encounter errors, use force push (only first time)
git push -u origin main --force
```

---

## 🌐 Deployment Commands

### Streamlit Community Cloud (Recommended)
```bash
# 1. Push code to GitHub (already done above)
# 2. Go to https://share.streamlit.io/
# 3. Click "Deploy now"
# 4. Connect your GitHub repository
# 5. Select crypto-ai-dashboard repository
# 6. Main file path: app_complete.py
# 7. Click "Deploy"

# Your app will be available at: https://yourusername-crypto-ai-dashboard.streamlit.app/
```

### Alternative: Render
```bash
# Create render.yaml
echo "
services:
  - type: web
    name: crypto-ai-dashboard
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app_complete.py --server.port=\$PORT
    envVars:
      - key: PORT
        value: 10000
" > render.yaml

# Add and deploy
git add render.yaml
git commit -m "Add Render deployment configuration"
git push
```

---

## 🔍 Manual Testing Checklist

### Frontend Testing (Browser)
1. Open http://localhost:8501
2. Test user registration and login
3. Test cryptocurrency selection
4. Test time period selection
5. Verify Phase 1: Market analysis charts
6. Verify Phase 2: AI features and chatbot
7. Verify Phase 3: Portfolio and prediction features
8. Test navigation between all sections

### Backend Testing (Terminal)
1. Run all test commands above
2. Verify data fetching works
3. Verify AI components load
4. Verify file operations work
5. Check for any error messages

### Integration Testing
1. Test complete user workflow
2. Test portfolio with real data
3. Test AI chatbot responses
4. Test prediction model training
5. Test multi-agent analysis

---

## 🚨 Common Issues & Solutions

### Git Not Found
```bash
# Install Git
winget install --id Git.Git -e --source winget

# Or download from: https://git-scm.com/download/win
```

### Port Already in Use
```bash
# Kill existing Streamlit process
taskkill /F /IM streamlit.exe

# Or use different port
streamlit run app_complete.py --server.port 8502
```

### TensorFlow/Keras Issues
```bash
# Fix compatibility
pip install tf-keras

# Or downgrade TensorFlow
pip install tensorflow==2.10.0
```

### Module Import Errors
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

### GitHub Push Errors
```bash
# Use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/crypto-ai-dashboard.git

# Or configure credentials
git config --global credential.helper store
```

---

## 📞 Support

If you encounter issues:
1. Check the [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions
2. Review [README.md](README.md) for project information
3. Check [Streamlit Documentation](https://docs.streamlit.io/)
4. Test each component individually using the commands above

---

## 🎉 Success Criteria

- [ ] All terminal tests pass
- [ ] Application runs in browser
- [ ] All features work (Phase 1, 2, 3)
- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] Deployed to Streamlit Cloud
- [ ] Live URL accessible

**🚀 Your Crypto AI Dashboard is ready for production!**
