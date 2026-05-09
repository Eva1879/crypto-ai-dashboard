"""
Advisor Agent - Phase 3
This agent provides investment advice and risk management recommendations.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json

class AdvisorAgent:
    def __init__(self):
        """Initialize advisor agent"""
        self.risk_profiles = {
            'conservative': {'max_allocation': 0.1, 'stop_loss': 0.05, 'take_profit': 0.15},
            'moderate': {'max_allocation': 0.2, 'stop_loss': 0.08, 'take_profit': 0.25},
            'aggressive': {'max_allocation': 0.3, 'stop_loss': 0.12, 'take_profit': 0.40}
        }
    
    def generate_investment_advice(self, market_data: Dict, indicators: Dict, 
                                sentiment: Dict, risk_profile: str = 'moderate') -> Dict:
        """
        Generate comprehensive investment advice
        
        Args:
            market_data (dict): Market data and analysis
            indicators (dict): Technical indicators
            sentiment (dict): Sentiment analysis
            risk_profile (str): User's risk profile
        
        Returns:
            dict: Investment advice and recommendations
        """
        if risk_profile not in self.risk_profiles:
            risk_profile = 'moderate'
        
        risk_params = self.risk_profiles[risk_profile]
        
        # Analyze market conditions
        market_analysis = self._analyze_market_conditions(market_data, indicators)
        
        # Analyze sentiment impact
        sentiment_analysis = self._analyze_sentiment_impact(sentiment)
        
        # Generate trading signals
        trading_signals = self._generate_trading_signals(indicators, sentiment)
        
        # Calculate position sizing
        position_sizing = self._calculate_position_sizing(market_data, risk_params)
        
        # Risk management recommendations
        risk_management = self._generate_risk_management(market_data, risk_params)
        
        # Overall recommendation
        overall_recommendation = self._generate_overall_recommendation(
            market_analysis, sentiment_analysis, trading_signals, risk_profile
        )
        
        return {
            'timestamp': datetime.now().isoformat(),
            'risk_profile': risk_profile,
            'market_analysis': market_analysis,
            'sentiment_analysis': sentiment_analysis,
            'trading_signals': trading_signals,
            'position_sizing': position_sizing,
            'risk_management': risk_management,
            'overall_recommendation': overall_recommendation,
            'disclaimer': "This is not financial advice. Please do your own research."
        }
    
    def _analyze_market_conditions(self, market_data: Dict, indicators: Dict) -> Dict:
        """Analyze current market conditions"""
        conditions = {
            'trend_strength': 'unknown',
            'volatility_level': 'unknown',
            'momentum': 'unknown',
            'support_resistance': {}
        }
        
        # Analyze trend
        if 'trend' in market_data:
            trend = market_data['trend']
            if 'strong' in trend:
                conditions['trend_strength'] = 'strong'
            elif 'uptrend' in trend or 'downtrend' in trend:
                conditions['trend_strength'] = 'moderate'
            else:
                conditions['trend_strength'] = 'weak'
        
        # Analyze volatility
        if 'volatility' in market_data:
            volatility = market_data['volatility']
            if volatility > 0.5:
                conditions['volatility_level'] = 'high'
            elif volatility > 0.3:
                conditions['volatility_level'] = 'moderate'
            else:
                conditions['volatility_level'] = 'low'
        
        # Analyze momentum using RSI and MACD
        if 'rsi_14' in indicators:
            rsi = indicators['rsi_14'].iloc[-1] if not indicators['rsi_14'].empty else 50
            if rsi > 70:
                conditions['momentum'] = 'overbought'
            elif rsi < 30:
                conditions['momentum'] = 'oversold'
            elif rsi > 50:
                conditions['momentum'] = 'bullish'
            else:
                conditions['momentum'] = 'bearish'
        
        # Support and resistance levels
        if 'support_level' in market_data and 'resistance_level' in market_data:
            conditions['support_resistance'] = {
                'support': market_data['support_level'],
                'resistance': market_data['resistance_level'],
                'current_price': market_data.get('current_price', 0)
            }
        
        return conditions
    
    def _analyze_sentiment_impact(self, sentiment: Dict) -> Dict:
        """Analyze sentiment impact on trading decisions"""
        impact = {
            'sentiment_score': 0,
            'confidence': 0,
            'impact_level': 'low',
            'contrarian_signal': False
        }
        
        # Get overall sentiment
        if 'overall_sentiment' in sentiment:
            overall = sentiment['overall_sentiment']
            impact['sentiment_score'] = overall.get('polarity', 0)
            impact['confidence'] = overall.get('confidence', 0)
            
            # Determine impact level
            if abs(impact['sentiment_score']) > 0.3 and impact['confidence'] > 0.7:
                impact['impact_level'] = 'high'
            elif abs(impact['sentiment_score']) > 0.15 and impact['confidence'] > 0.5:
                impact['impact_level'] = 'moderate'
            
            # Check for contrarian opportunities
            if impact['sentiment_score'] > 0.5 and impact['confidence'] > 0.8:
                impact['contrarian_signal'] = True  # Extreme bullish might indicate top
        
        return impact
    
    def _generate_trading_signals(self, indicators: Dict, sentiment: Dict) -> Dict:
        """Generate detailed trading signals"""
        signals = {
            'primary_signal': 'hold',
            'signal_strength': 0,
            'supporting_signals': [],
            'conflicting_signals': [],
            'time_horizon': 'medium'
        }
        
        # Technical signals
        tech_signals = []
        
        # RSI signal
        if 'rsi_14' in indicators:
            rsi = indicators['rsi_14'].iloc[-1] if not indicators['rsi_14'].empty else 50
            if rsi < 30:
                tech_signals.append({'type': 'RSI', 'signal': 'buy', 'strength': 2})
            elif rsi > 70:
                tech_signals.append({'type': 'RSI', 'signal': 'sell', 'strength': 2})
            elif rsi < 45:
                tech_signals.append({'type': 'RSI', 'signal': 'buy', 'strength': 1})
            elif rsi > 55:
                tech_signals.append({'type': 'RSI', 'signal': 'sell', 'strength': 1})
        
        # MACD signal
        if 'macd' in indicators:
            macd_data = indicators['macd']
            if 'macd_crossover' in macd_data:
                crossover = macd_data['macd_crossover']
                if crossover.get('last_crossover'):
                    last_cross = crossover['last_crossover']
                    if last_cross['type'] == 'bullish':
                        tech_signals.append({'type': 'MACD', 'signal': 'buy', 'strength': 2})
                    else:
                        tech_signals.append({'type': 'MACD', 'signal': 'sell', 'strength': 2})
        
        # Moving average signal
        if 'moving_averages' in indicators:
            ma_data = indicators['moving_averages']
            if 'ema_crossovers' in ma_data:
                crossover = ma_data['ema_crossovers']
                if crossover.get('last_crossover'):
                    last_cross = crossover['last_crossover']
                    if last_cross['type'] == 'golden_cross':
                        tech_signals.append({'type': 'MA', 'signal': 'buy', 'strength': 2})
                    else:
                        tech_signals.append({'type': 'MA', 'signal': 'sell', 'strength': 2})
        
        # Sentiment signal
        sentiment_signal = None
        if 'overall_sentiment' in sentiment:
            overall = sentiment['overall_sentiment']
            polarity = overall.get('polarity', 0)
            confidence = overall.get('confidence', 0)
            
            if polarity > 0.2 and confidence > 0.6:
                sentiment_signal = {'type': 'Sentiment', 'signal': 'buy', 'strength': 1}
            elif polarity < -0.2 and confidence > 0.6:
                sentiment_signal = {'type': 'Sentiment', 'signal': 'sell', 'strength': 1}
        
        # Combine signals
        all_signals = tech_signals.copy()
        if sentiment_signal:
            all_signals.append(sentiment_signal)
        
        # Calculate primary signal
        buy_strength = sum(s['strength'] for s in all_signals if s['signal'] == 'buy')
        sell_strength = sum(s['strength'] for s in all_signals if s['signal'] == 'sell')
        
        if buy_strength > sell_strength + 1:
            signals['primary_signal'] = 'buy'
            signals['signal_strength'] = buy_strength - sell_strength
        elif sell_strength > buy_strength + 1:
            signals['primary_signal'] = 'sell'
            signals['signal_strength'] = sell_strength - buy_strength
        else:
            signals['primary_signal'] = 'hold'
            signals['signal_strength'] = 0
        
        # Categorize signals
        for signal in all_signals:
            if signal['signal'] == signals['primary_signal']:
                signals['supporting_signals'].append(signal)
            else:
                signals['conflicting_signals'].append(signal)
        
        return signals
    
    def _calculate_position_sizing(self, market_data: Dict, risk_params: Dict) -> Dict:
        """Calculate recommended position sizing"""
        sizing = {
            'recommended_allocation': 0,
            'position_size': 0,
            'risk_amount': 0,
            'sizing_method': 'fixed_percentage'
        }
        
        # Base allocation based on risk profile
        base_allocation = risk_params['max_allocation']
        
        # Adjust based on market conditions
        volatility_adjustment = 1.0
        if 'volatility' in market_data:
            volatility = market_data['volatility']
            if volatility > 0.5:
                volatility_adjustment = 0.5  # Reduce position in high volatility
            elif volatility > 0.3:
                volatility_adjustment = 0.75
        
        sizing['recommended_allocation'] = base_allocation * volatility_adjustment
        sizing['position_size'] = sizing['recommended_allocation']
        sizing['risk_amount'] = sizing['recommended_allocation'] * risk_params['stop_loss']
        
        return sizing
    
    def _generate_risk_management(self, market_data: Dict, risk_params: Dict) -> Dict:
        """Generate risk management recommendations"""
        risk_mgmt = {
            'stop_loss': 0,
            'take_profit': 0,
            'position_limit': 0,
            'risk_reward_ratio': 0,
            'additional_measures': []
        }
        
        current_price = market_data.get('current_price', 0)
        if current_price > 0:
            risk_mgmt['stop_loss'] = current_price * (1 - risk_params['stop_loss'])
            risk_mgmt['take_profit'] = current_price * (1 + risk_params['take_profit'])
            risk_mgmt['position_limit'] = risk_params['max_allocation']
            
            # Calculate risk-reward ratio
            risk_amount = current_price - risk_mgmt['stop_loss']
            reward_amount = risk_mgmt['take_profit'] - current_price
            if risk_amount > 0:
                risk_mgmt['risk_reward_ratio'] = reward_amount / risk_amount
        
        # Additional risk measures
        risk_mgmt['additional_measures'] = [
            'Use trailing stop-loss to protect profits',
            'Consider dollar-cost averaging for entry',
            'Monitor market volatility closely',
            'Set maximum portfolio allocation limits',
            'Regular portfolio rebalancing'
        ]
        
        return risk_mgmt
    
    def _generate_overall_recommendation(self, market_analysis: Dict, 
                                     sentiment_analysis: Dict, 
                                     trading_signals: Dict, 
                                     risk_profile: str) -> Dict:
        """Generate overall investment recommendation"""
        recommendation = {
            'action': 'HOLD',
            'confidence': 0,
            'reasoning': '',
            'time_horizon': 'medium',
            'risk_level': 'medium'
        }
        
        # Base action on trading signals
        primary_signal = trading_signals['primary_signal']
        signal_strength = trading_signals['signal_strength']
        
        # Adjust based on market conditions
        if market_analysis['volatility_level'] == 'high':
            signal_strength *= 0.7  # Reduce signal strength in high volatility
        
        # Adjust based on sentiment impact
        if sentiment_analysis['impact_level'] == 'high':
            signal_strength += 1 if sentiment_analysis['sentiment_score'] > 0 else -1
        
        # Generate final recommendation
        if signal_strength > 2:
            recommendation['action'] = 'BUY'
            recommendation['confidence'] = min(signal_strength / 4, 1.0)
        elif signal_strength < -2:
            recommendation['action'] = 'SELL'
            recommendation['confidence'] = min(abs(signal_strength) / 4, 1.0)
        else:
            recommendation['action'] = 'HOLD'
            recommendation['confidence'] = 0.5
        
        # Generate reasoning
        reasoning_parts = []
        
        if primary_signal != 'hold':
            reasoning_parts.append(f"Technical indicators show {primary_signal} signal")
        
        if sentiment_analysis['impact_level'] != 'low':
            reasoning_parts.append(f"Market sentiment is {sentiment_analysis['sentiment_score']:.2f}")
        
        if market_analysis['volatility_level'] != 'moderate':
            reasoning_parts.append(f"Market volatility is {market_analysis['volatility_level']}")
        
        reasoning_parts.append(f"Risk profile: {risk_profile}")
        
        recommendation['reasoning'] = " | ".join(reasoning_parts)
        
        # Set risk level based on profile and conditions
        if risk_profile == 'conservative':
            recommendation['risk_level'] = 'low'
        elif risk_profile == 'aggressive':
            recommendation['risk_level'] = 'high'
        else:
            recommendation['risk_level'] = 'medium'
        
        return recommendation
    
    def get_portfolio_recommendations(self, portfolio_data: Dict, market_data: Dict) -> Dict:
        """
        Get portfolio-specific recommendations
        
        Args:
            portfolio_data (dict): Current portfolio holdings
            market_data (dict): Current market data
        
        Returns:
            dict: Portfolio recommendations
        """
        recommendations = {
            'rebalancing_needed': False,
            'actions': [],
            'risk_assessment': {},
            'performance_review': {}
        }
        
        # Analyze current portfolio
        if 'holdings' in portfolio_data:
            holdings = portfolio_data['holdings']
            
            # Check for overconcentration
            total_value = sum(h['value'] for h in holdings.values() if 'value' in h)
            if total_value > 0:
                for symbol, holding in holdings.items():
                    allocation = holding.get('value', 0) / total_value
                    if allocation > 0.3:  # More than 30% in one asset
                        recommendations['actions'].append({
                            'type': 'rebalance',
                            'symbol': symbol,
                            'reason': f'Overconcentrated position ({allocation:.1%})',
                            'suggested_action': 'Consider reducing position'
                        })
                        recommendations['rebalancing_needed'] = True
        
        # Performance review
        recommendations['performance_review'] = {
            'review_period': 'Last 30 days',
            'recommendations': [
                'Review underperforming positions',
                'Consider taking profits on strong performers',
                'Reassess investment thesis for each holding'
            ]
        }
        
        return recommendations
    
    def get_educational_content(self, topic: str) -> Dict:
        """
        Get educational content about investing topics
        
        Args:
            topic (str): Educational topic
        
        Returns:
            dict: Educational content
        """
        content = {
            'risk_management': {
                'title': 'Understanding Risk Management',
                'content': [
                    'Never invest more than you can afford to lose',
                    'Use stop-loss orders to limit downside',
                    'Diversify your portfolio across different assets',
                    'Position sizing is crucial for long-term success',
                    'Regular portfolio rebalancing helps maintain risk levels'
                ]
            },
            'technical_analysis': {
                'title': 'Technical Analysis Basics',
                'content': [
                    'RSI indicates overbought/oversold conditions',
                    'Moving averages help identify trends',
                    'Volume confirms price movements',
                    'Support and resistance levels are key price points',
                    'Multiple indicators provide better signals'
                ]
            },
            'sentiment_analysis': {
                'title': 'Market Sentiment Analysis',
                'content': [
                    'News sentiment can impact short-term price movements',
                    'Social media sentiment provides real-time insights',
                    'Contrarian investing often pays off during extremes',
                    'Sentiment should be used with technical analysis',
                    'Market psychology drives many price movements'
                ]
            }
        }
        
        return content.get(topic, {
            'title': 'Investment Education',
            'content': ['Educational content not available for this topic']
        })
