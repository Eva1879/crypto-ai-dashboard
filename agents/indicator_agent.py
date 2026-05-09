"""
Indicator Agent - Phase 3
This agent calculates and analyzes technical indicators.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from indicators.rsi import calculate_rsi, calculate_macd, calculate_bollinger_bands

class IndicatorAgent:
    def __init__(self):
        """Initialize indicator agent"""
        pass
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> Dict:
        """
        Calculate all technical indicators
        
        Args:
            data (pd.DataFrame): OHLCV data
        
        Returns:
            dict: All calculated indicators
        """
        if data.empty:
            return {}
        
        indicators = {}
        
        # Momentum indicators
        indicators['rsi'] = self._calculate_rsi_extended(data['Close'])
        indicators['macd'] = self._calculate_macd_extended(data['Close'])
        indicators['stochastic'] = self._calculate_stochastic(data)
        
        # Trend indicators
        indicators['moving_averages'] = self._calculate_moving_averages(data['Close'])
        indicators['bollinger_bands'] = calculate_bollinger_bands(data['Close'])
        indicators['adx'] = self._calculate_adx(data)
        
        # Volatility indicators
        indicators['atr'] = self._calculate_atr(data)
        indicators['vwap'] = self._calculate_vwap(data)
        
        # Volume indicators
        if 'Volume' in data.columns:
            indicators['volume_indicators'] = self._calculate_volume_indicators(data)
        
        return indicators
    
    def _calculate_rsi_extended(self, prices: pd.Series, periods: List[int] = [14, 21]) -> Dict:
        """Calculate RSI for multiple periods"""
        rsi_values = {}
        for period in periods:
            rsi_values[f'rsi_{period}'] = calculate_rsi(prices, period)
        return rsi_values
    
    def _calculate_macd_extended(self, prices: pd.Series) -> Dict:
        """Calculate MACD with multiple parameters"""
        macd_line, signal_line, histogram = calculate_macd(prices)
        
        return {
            'macd_line': macd_line,
            'signal_line': signal_line,
            'histogram': histogram,
            'macd_crossover': self._detect_macd_crossover(macd_line, signal_line),
            'signal_strength': self._calculate_macd_signal_strength(histogram)
        }
    
    def _calculate_stochastic(self, data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> Dict:
        """Calculate Stochastic oscillator"""
        low_min = data['Low'].rolling(window=k_period).min()
        high_max = data['High'].rolling(window=k_period).max()
        
        k_percent = 100 * ((data['Close'] - low_min) / (high_max - low_min))
        d_percent = k_percent.rolling(window=d_period).mean()
        
        return {
            'k_percent': k_percent,
            'd_percent': d_percent,
            'stochastic_crossover': self._detect_stochastic_crossover(k_percent, d_percent)
        }
    
    def _calculate_moving_averages(self, prices: pd.Series) -> Dict:
        """Calculate various moving averages"""
        return {
            'sma_10': prices.rolling(window=10).mean(),
            'sma_20': prices.rolling(window=20).mean(),
            'sma_50': prices.rolling(window=50).mean(),
            'sma_200': prices.rolling(window=200).mean(),
            'ema_12': prices.ewm(span=12).mean(),
            'ema_26': prices.ewm(span=26).mean(),
            'ema_crossovers': self._detect_ma_crossovers(prices)
        }
    
    def _calculate_adx(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average Directional Index"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        # Calculate True Range
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Calculate directional movements
        up_move = high - high.shift()
        down_move = low.shift() - low
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        # Calculate ADX
        atr = tr.rolling(window=period).mean()
        plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).mean() / atr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).mean() / atr)
        
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()
        
        return adx
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    def _calculate_vwap(self, data: pd.DataFrame) -> pd.Series:
        """Calculate Volume Weighted Average Price"""
        if 'Volume' not in data.columns:
            return pd.Series(index=data.index, dtype=float)
        
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        vwap = (typical_price * data['Volume']).cumsum() / data['Volume'].cumsum()
        
        return vwap
    
    def _calculate_volume_indicators(self, data: pd.DataFrame) -> Dict:
        """Calculate volume-based indicators"""
        volume = data['Volume']
        
        # On-Balance Volume
        obv = []
        obv_value = 0
        for i in range(len(data)):
            if i == 0:
                obv_value = volume.iloc[i]
            else:
                if data['Close'].iloc[i] > data['Close'].iloc[i-1]:
                    obv_value += volume.iloc[i]
                elif data['Close'].iloc[i] < data['Close'].iloc[i-1]:
                    obv_value -= volume.iloc[i]
            obv.append(obv_value)
        
        # Volume Moving Average
        volume_sma = volume.rolling(window=20).mean()
        
        return {
            'obv': pd.Series(obv, index=data.index),
            'volume_sma': volume_sma,
            'volume_ratio': volume / volume_sma
        }
    
    def _detect_macd_crossover(self, macd_line: pd.Series, signal_line: pd.Series) -> Dict:
        """Detect MACD crossovers"""
        crossover_points = []
        
        for i in range(1, len(macd_line)):
            if macd_line.iloc[i-1] < signal_line.iloc[i-1] and macd_line.iloc[i] > signal_line.iloc[i]:
                crossover_points.append({'date': macd_line.index[i], 'type': 'bullish'})
            elif macd_line.iloc[i-1] > signal_line.iloc[i-1] and macd_line.iloc[i] < signal_line.iloc[i]:
                crossover_points.append({'date': macd_line.index[i], 'type': 'bearish'})
        
        return {
            'crossover_points': crossover_points,
            'last_crossover': crossover_points[-1] if crossover_points else None
        }
    
    def _detect_stochastic_crossover(self, k_percent: pd.Series, d_percent: pd.Series) -> Dict:
        """Detect Stochastic crossovers"""
        crossover_points = []
        
        for i in range(1, len(k_percent)):
            if k_percent.iloc[i-1] < d_percent.iloc[i-1] and k_percent.iloc[i] > d_percent.iloc[i]:
                crossover_points.append({'date': k_percent.index[i], 'type': 'bullish'})
            elif k_percent.iloc[i-1] > d_percent.iloc[i-1] and k_percent.iloc[i] < d_percent.iloc[i]:
                crossover_points.append({'date': k_percent.index[i], 'type': 'bearish'})
        
        return {
            'crossover_points': crossover_points,
            'last_crossover': crossover_points[-1] if crossover_points else None
        }
    
    def _detect_ma_crossovers(self, prices: pd.Series) -> Dict:
        """Detect moving average crossovers"""
        sma_20 = prices.rolling(window=20).mean()
        sma_50 = prices.rolling(window=50).mean()
        
        crossover_points = []
        
        for i in range(1, len(sma_20)):
            if sma_20.iloc[i-1] < sma_50.iloc[i-1] and sma_20.iloc[i] > sma_50.iloc[i]:
                crossover_points.append({'date': sma_20.index[i], 'type': 'golden_cross'})
            elif sma_20.iloc[i-1] > sma_50.iloc[i-1] and sma_20.iloc[i] < sma_50.iloc[i]:
                crossover_points.append({'date': sma_20.index[i], 'type': 'death_cross'})
        
        return {
            'crossover_points': crossover_points,
            'last_crossover': crossover_points[-1] if crossover_points else None
        }
    
    def _calculate_macd_signal_strength(self, histogram: pd.Series) -> str:
        """Calculate MACD signal strength"""
        current_hist = histogram.iloc[-1]
        
        if abs(current_hist) > 0.5:
            return "strong"
        elif abs(current_hist) > 0.2:
            return "moderate"
        else:
            return "weak"
    
    def get_indicator_signals(self, data: pd.DataFrame) -> Dict:
        """
        Get trading signals from all indicators
        
        Args:
            data (pd.DataFrame): OHLCV data
        
        Returns:
            dict: Trading signals
        """
        indicators = self.calculate_all_indicators(data)
        signals = {
            'overall_signal': 'neutral',
            'signal_strength': 0,
            'individual_signals': {}
        }
        
        signal_count = 0
        signal_strength_sum = 0
        
        # RSI signals
        if 'rsi_14' in indicators:
            rsi_current = indicators['rsi_14'].iloc[-1]
            if rsi_current > 70:
                signals['individual_signals']['rsi'] = 'sell'
                signal_count -= 1
                signal_strength_sum -= 2
            elif rsi_current < 30:
                signals['individual_signals']['rsi'] = 'buy'
                signal_count += 1
                signal_strength_sum += 2
            else:
                signals['individual_signals']['rsi'] = 'neutral'
        
        # MACD signals
        if 'macd' in indicators:
            macd_crossover = indicators['macd']['macd_crossover']
            if macd_crossover['last_crossover']:
                if macd_crossover['last_crossover']['type'] == 'bullish':
                    signals['individual_signals']['macd'] = 'buy'
                    signal_count += 1
                    signal_strength_sum += 1
                else:
                    signals['individual_signals']['macd'] = 'sell'
                    signal_count -= 1
                    signal_strength_sum -= 1
        
        # Moving average signals
        if 'moving_averages' in indicators:
            ma_crossover = indicators['moving_averages']['ema_crossovers']
            if ma_crossover['last_crossover']:
                if ma_crossover['last_crossover']['type'] == 'golden_cross':
                    signals['individual_signals']['ma'] = 'buy'
                    signal_count += 1
                    signal_strength_sum += 1
                else:
                    signals['individual_signals']['ma'] = 'sell'
                    signal_count -= 1
                    signal_strength_sum -= 1
        
        # Determine overall signal
        if signal_count > 0:
            signals['overall_signal'] = 'buy'
        elif signal_count < 0:
            signals['overall_signal'] = 'sell'
        
        signals['signal_strength'] = abs(signal_strength_sum)
        
        return signals
