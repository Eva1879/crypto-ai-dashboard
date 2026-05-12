"""
Vercel API for Crypto Dashboard
Flask-based API that works with Vercel serverless functions
"""

from flask import Flask, jsonify, render_template_string
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import requests
from textblob import TextBlob
import json
import os

app = Flask(__name__)

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

@app.route('/')
def home():
    """Serve the dashboard HTML"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto AI Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 20px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            text-align: center;
        }
        .header h1 {
            margin: 0;
            color: white;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.2em;
        }
        .controls {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .chart-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-card h3 {
            margin: 0;
            color: #667eea;
        }
        .metric-card p {
            margin: 5px 0 0 0;
            color: #666;
        }
        .button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            margin: 5px;
        }
        .button:hover {
            background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
        }
        .select {
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid #ddd;
            margin: 5px;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
            font-weight: bold;
        }
        .news-item {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        .news-item h4 {
            margin: 0 0 5px 0;
            color: #667eea;
        }
        .news-item p {
            margin: 0;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Crypto AI Dashboard</h1>
            <p>Multi-Agent Intelligence Platform (Vercel Version)</p>
        </div>
        
        <div class="controls">
            <h3 style="margin: 0 0 15px 0; color: #667eea;">📊 Configuration</h3>
            <select id="cryptoSelect" class="select">
                <option value="BTC-USD">Bitcoin (BTC)</option>
                <option value="ETH-USD">Ethereum (ETH)</option>
                <option value="BNB-USD">Binance Coin (BNB)</option>
                <option value="XRP-USD">Ripple (XRP)</option>
                <option value="ADA-USD">Cardano (ADA)</option>
                <option value="SOL-USD">Solana (SOL)</option>
                <option value="DOGE-USD">Dogecoin (DOGE)</option>
            </select>
            <select id="periodSelect" class="select">
                <option value="1mo">1 Month</option>
                <option value="3mo">3 Months</option>
                <option value="6mo">6 Months</option>
                <option value="1y">1 Year</option>
                <option value="2y">2 Years</option>
            </select>
            <button class="button" onclick="loadData()">📈 Load Data</button>
            <button class="button" onclick="loadNews()">📰 Load News</button>
        </div>
        
        <div id="loading" class="loading" style="display: none;">
            Loading data... Please wait...
        </div>
        
        <div id="chartContainer" class="chart-container">
            <h3 style="margin: 0 0 15px 0; color: #667eea;">📈 Market Analysis</h3>
            <div id="chart"></div>
        </div>
        
        <div id="recommendationContainer" class="metric-card">
            <h3 style="margin: 0; color: #667eea;">💡 Recommendation</h3>
            <p style="margin: 10px 0 0 0;">Click "Load Data" to get analysis</p>
        </div>
        
        <div id="newsContainer" class="metric-card">
            <h3 style="margin: 0 0 15px 0; color: #667eea;">📰 Latest News</h3>
            <p style="margin: 0; color: #666;">Click "Load News" to get latest crypto news</p>
        </div>
        
        <div id="sentimentContainer" class="metric-card">
            <h3 style="margin: 0; color: #667eea;">📊 Overall Sentiment</h3>
            <p style="margin: 10px 0 0 0;">Click "Load News" to get sentiment analysis</p>
        </div>
    </div>

    <script>
        async function loadData() {
            const crypto = document.getElementById('cryptoSelect').value;
            const period = document.getElementById('periodSelect').value;
            
            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch(`/api/market-data?symbol=${crypto}&period=${period}`);
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Update chart
                updateChart(data.chart_data);
                
                // Update recommendation
                const recommendationDiv = document.getElementById('recommendationContainer');
                recommendationDiv.innerHTML = `
                    <h3 style="margin: 0; color: #667eea;">💡 Recommendation</h3>
                    <p style="margin: 10px 0 0 0; font-size: 1.5em; font-weight: bold; color: ${data.recommendation.signal === 'BUY' ? 'green' : data.recommendation.signal === 'SELL' ? 'red' : 'orange'};">
                        ${data.recommendation.signal}
                    </p>
                    <p style="margin: 5px 0 0 0; color: #666;">${data.recommendation.reasoning}</p>
                `;
                
            } catch (error) {
                alert('Error loading data: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        async function loadNews() {
            const crypto = document.getElementById('cryptoSelect').value;
            
            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch(`/api/news?symbol=${crypto.replace('-USD', '')}`);
                const data = await response.json();
                
                // Update news
                const newsDiv = document.getElementById('newsContainer');
                newsDiv.innerHTML = `
                    <h3 style="margin: 0 0 15px 0; color: #667eea;">📰 Latest News</h3>
                    ${data.news.map(article => `
                        <div class="news-item">
                            <h4>${article.title}</h4>
                            <p>Source: ${article.source}</p>
                        </div>
                    `).join('')}
                `;
                
                // Update sentiment
                const sentimentDiv = document.getElementById('sentimentContainer');
                sentimentDiv.innerHTML = `
                    <h3 style="margin: 0; color: #667eea;">📊 Overall Sentiment</h3>
                    <p style="margin: 10px 0 0 0; font-size: 1.5em; font-weight: bold; color: ${data.sentiment.overall === 'positive' ? 'green' : data.sentiment.overall === 'negative' ? 'red' : 'orange'};">
                        ${data.sentiment.overall.toUpperCase()}
                    </p>
                    <p style="margin: 5px 0 0 0; color: #666;">Confidence: ${data.sentiment.confidence.toFixed(2)}</p>
                `;
                
            } catch (error) {
                alert('Error loading news: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function updateChart(chartData) {
            const chartDiv = document.getElementById('chart');
            Plotly.newPlot(chartDiv, chartData.data, chartData.layout, {responsive: true});
        }
        
        // Load initial data
        window.onload = function() {
            loadData();
        };
    </script>
</body>
</html>
    """)

@app.route('/api/market-data')
def market_data():
    """API endpoint for market data"""
    try:
        symbol = request.args.get('symbol', 'BTC-USD')
        period = request.args.get('period', '1mo')
        
        # Fetch data
        data = yf.download(symbol, period=period, interval='1d')
        
        if data.empty:
            return jsonify({'error': 'No data available'})
        
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
        
        # Create chart data
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
        
        # Get recommendation
        current_price = data['Close'].iloc[-1]
        current_rsi = data['RSI'].iloc[-1]
        recommendation = get_recommendation(current_rsi, data['Close'])
        
        return jsonify({
            'chart_data': fig.to_dict(),
            'recommendation': recommendation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/news')
def news():
    """API endpoint for news"""
    try:
        symbol = request.args.get('symbol', 'BTC')
        
        # Get news
        news_data = get_crypto_news(symbol, limit=5)
        
        # Get sentiment
        sentiment = get_overall_sentiment(news_data)
        
        return jsonify({
            'news': news_data,
            'sentiment': sentiment
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

# For Vercel serverless functions
from flask import request

if __name__ == '__main__':
    app.run(debug=True)
else:
    # Vercel serverless function handler
    def handler(event):
        return app(event)
