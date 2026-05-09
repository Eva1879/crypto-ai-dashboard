"""
Sentiment Agent - Phase 3
This agent handles sentiment analysis from news and social media sources.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
import re
from sentiment.news_analyzer import analyze_sentiment, get_crypto_news
from transformers import pipeline
import warnings
warnings.filterwarnings('ignore')

class SentimentAgent:
    def __init__(self):
        """Initialize sentiment agent"""
        try:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis", 
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
        except:
            self.sentiment_analyzer = None
        
        self.cache = {}
        self.cache_timeout = 1800  # 30 minutes
    
    def analyze_news_sentiment(self, symbol: str, limit: int = 20) -> Dict:
        """
        Analyze sentiment from news articles
        
        Args:
            symbol (str): Cryptocurrency symbol
            limit (int): Number of articles to analyze
        
        Returns:
            dict: Sentiment analysis results
        """
        cache_key = f"news_sentiment_{symbol}"
        current_time = datetime.now().timestamp()
        
        # Check cache
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if current_time - timestamp < self.cache_timeout:
                return data
        
        try:
            # Fetch news articles
            articles = get_crypto_news(symbol, limit)
            
            if not articles:
                return self._get_empty_sentiment_analysis()
            
            # Analyze each article
            article_sentiments = []
            for article in articles:
                # Analyze title
                title_sentiment = self._analyze_text_sentiment(article['title'])
                
                # Analyze description if available
                desc_sentiment = None
                if article.get('description'):
                    desc_sentiment = self._analyze_text_sentiment(article['description'])
                
                # Combine sentiments
                if desc_sentiment:
                    combined_polarity = (title_sentiment['polarity'] + desc_sentiment['polarity']) / 2
                    combined_confidence = (title_sentiment.get('confidence', 0.5) + desc_sentiment.get('confidence', 0.5)) / 2
                else:
                    combined_polarity = title_sentiment['polarity']
                    combined_confidence = title_sentiment.get('confidence', 0.5)
                
                article_sentiments.append({
                    'title': article['title'],
                    'source': article['source'],
                    'sentiment': self._classify_sentiment(combined_polarity),
                    'polarity': combined_polarity,
                    'confidence': combined_confidence,
                    'date': article.get('published_date', ''),
                    'url': article.get('url', '')
                })
            
            # Calculate overall sentiment
            overall_sentiment = self._calculate_overall_sentiment(article_sentiments)
            
            result = {
                'symbol': symbol,
                'overall_sentiment': overall_sentiment,
                'article_count': len(article_sentiments),
                'articles': article_sentiments,
                'sentiment_distribution': self._get_sentiment_distribution(article_sentiments),
                'last_updated': datetime.now().isoformat()
            }
            
            # Cache results
            self.cache[cache_key] = (result, current_time)
            
            return result
            
        except Exception as e:
            print(f"Error analyzing news sentiment for {symbol}: {e}")
            return self._get_empty_sentiment_analysis()
    
    def analyze_social_sentiment(self, symbol: str) -> Dict:
        """
        Analyze sentiment from social media (simulated)
        
        Args:
            symbol (str): Cryptocurrency symbol
        
        Returns:
            dict: Social sentiment analysis
        """
        # In a real implementation, this would fetch from Twitter, Reddit, etc.
        # For now, we'll simulate social sentiment based on recent price action
        
        cache_key = f"social_sentiment_{symbol}"
        current_time = datetime.now().timestamp()
        
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if current_time - self.cache_timeout:
                return data
        
        # Simulate social sentiment data
        social_sentiments = self._simulate_social_sentiment(symbol)
        
        result = {
            'symbol': symbol,
            'social_sentiment': social_sentiments,
            'overall_social_sentiment': self._calculate_overall_sentiment(social_sentiments),
            'last_updated': datetime.now().isoformat()
        }
        
        self.cache[cache_key] = (result, current_time)
        return result
    
    def _analyze_text_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        if self.sentiment_analyzer:
            try:
                result = self.sentiment_analyzer(text[:512])
                label = result[0]['label'].lower()
                score = result[0]['score']
                
                if label == 'positive':
                    polarity = score
                elif label == 'negative':
                    polarity = -score
                else:
                    polarity = 0
                
                return {
                    'polarity': polarity,
                    'classification': self._classify_sentiment(polarity),
                    'confidence': score
                }
            except:
                pass
        
        # Fallback to simple keyword-based sentiment
        return self._keyword_sentiment_analysis(text)
    
    def _keyword_sentiment_analysis(self, text: str) -> Dict:
        """Simple keyword-based sentiment analysis"""
        positive_words = ['bullish', 'buy', 'up', 'rise', 'growth', 'profit', 'gain', 'strong', 'positive']
        negative_words = ['bearish', 'sell', 'down', 'fall', 'decline', 'loss', 'weak', 'negative', 'crash']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = positive_count + negative_count
        if total_words == 0:
            return {'polarity': 0, 'classification': 'neutral', 'confidence': 0.5}
        
        polarity = (positive_count - negative_count) / total_words
        confidence = min(total_words / 10, 1.0)  # More words = higher confidence
        
        return {
            'polarity': polarity,
            'classification': self._classify_sentiment(polarity),
            'confidence': confidence
        }
    
    def _classify_sentiment(self, polarity: float) -> str:
        """Classify sentiment based on polarity score"""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    def _calculate_overall_sentiment(self, sentiments: List[Dict]) -> Dict:
        """Calculate overall sentiment from multiple sentiment analyses"""
        if not sentiments:
            return {'classification': 'neutral', 'polarity': 0, 'confidence': 0}
        
        polarities = [s['polarity'] for s in sentiments if 'polarity' in s]
        confidences = [s.get('confidence', 0.5) for s in sentiments]
        
        if not polarities:
            return {'classification': 'neutral', 'polarity': 0, 'confidence': 0}
        
        # Weighted average based on confidence
        weighted_polarity = sum(p * c for p, c in zip(polarities, confidences)) / sum(confidences)
        avg_confidence = np.mean(confidences)
        
        return {
            'classification': self._classify_sentiment(weighted_polarity),
            'polarity': weighted_polarity,
            'confidence': avg_confidence
        }
    
    def _get_sentiment_distribution(self, sentiments: List[Dict]) -> Dict:
        """Get distribution of sentiment classifications"""
        if not sentiments:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        classifications = [s.get('sentiment', 'neutral') for s in sentiments]
        total = len(classifications)
        
        return {
            'positive': classifications.count('positive') / total * 100,
            'negative': classifications.count('negative') / total * 100,
            'neutral': classifications.count('neutral') / total * 100
        }
    
    def _simulate_social_sentiment(self, symbol: str) -> List[Dict]:
        """Simulate social media sentiment (placeholder for real implementation)"""
        # In real implementation, this would fetch from Twitter API, Reddit API, etc.
        social_posts = [
            {
                'platform': 'Twitter',
                'content': f'Bullish on {symbol}! Technical indicators look strong 🚀',
                'sentiment': 'positive',
                'polarity': 0.7,
                'confidence': 0.8,
                'engagement': 150
            },
            {
                'platform': 'Reddit',
                'content': f'What are your thoughts on {symbol} price action this week?',
                'sentiment': 'neutral',
                'polarity': 0.1,
                'confidence': 0.6,
                'engagement': 89
            },
            {
                'platform': 'Twitter',
                'content': f'{symbol} showing some weakness, might be time to take profits',
                'sentiment': 'negative',
                'polarity': -0.4,
                'confidence': 0.7,
                'engagement': 67
            }
        ]
        
        return social_posts
    
    def _get_empty_sentiment_analysis(self) -> Dict:
        """Get empty sentiment analysis when no data is available"""
        return {
            'overall_sentiment': {'classification': 'neutral', 'polarity': 0, 'confidence': 0},
            'article_count': 0,
            'articles': [],
            'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
            'last_updated': datetime.now().isoformat()
        }
    
    def get_sentiment_trend(self, symbol: str, days: int = 7) -> Dict:
        """
        Get sentiment trend over time
        
        Args:
            symbol (str): Cryptocurrency symbol
            days (int): Number of days to analyze
        
        Returns:
            dict: Sentiment trend analysis
        """
        # In a real implementation, this would fetch historical sentiment data
        # For now, we'll simulate a trend
        
        trend_data = []
        base_sentiment = np.random.normal(0.1, 0.2)  # Random base sentiment
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            # Add some random variation
            daily_sentiment = base_sentiment + np.random.normal(0, 0.1)
            
            trend_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'sentiment': self._classify_sentiment(daily_sentiment),
                'polarity': daily_sentiment
            })
        
        # Calculate trend direction
        polarities = [d['polarity'] for d in trend_data]
        if len(polarities) > 1:
            trend_slope = (polarities[-1] - polarities[0]) / len(polarities)
            if trend_slope > 0.05:
                trend_direction = 'improving'
            elif trend_slope < -0.05:
                trend_direction = 'declining'
            else:
                trend_direction = 'stable'
        else:
            trend_direction = 'stable'
        
        return {
            'symbol': symbol,
            'trend_data': trend_data,
            'trend_direction': trend_direction,
            'average_polarity': np.mean(polarities) if polarities else 0,
            'last_updated': datetime.now().isoformat()
        }
