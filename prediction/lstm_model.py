"""
LSTM Prediction Model - Phase 3
This module implements LSTM-based cryptocurrency price prediction using TensorFlow/Keras.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os
import json
import warnings
warnings.filterwarnings('ignore')

class LSTMPredictor:
    def __init__(self, model_dir="data/models"):
        """
        Initialize LSTM predictor
        
        Args:
            model_dir (str): Directory to save/load models
        """
        self.model_dir = model_dir
        self.scaler = MinMaxScaler()
        self.model = None
        self.history = None
        self.ensure_model_directory()
    
    def ensure_model_directory(self):
        """Ensure model directory exists"""
        os.makedirs(self.model_dir, exist_ok=True)
    
    def prepare_data(self, data: pd.DataFrame, lookback: int = 60, target_column: str = 'Close') -> tuple:
        """
        Prepare data for LSTM training
        
        Args:
            data (pd.DataFrame): Historical price data
            lookback (int): Number of previous days to use for prediction
            target_column (str): Column to predict
        
        Returns:
            tuple: (X_train, y_train, X_test, y_test, scaler)
        """
        # Use only the target column for basic prediction
        prices = data[[target_column]].values
        
        # Scale the data
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_prices = self.scaler.fit_transform(prices)
        
        # Create sequences
        X, y = [], []
        for i in range(lookback, len(scaled_prices)):
            X.append(scaled_prices[i-lookback:i, 0])
            y.append(scaled_prices[i, 0])
        
        X, y = np.array(X), np.array(y)
        
        # Split data (80% train, 20% test)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Reshape for LSTM [samples, timesteps, features]
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
        
        return X_train, y_train, X_test, y_test
    
    def build_model(self, input_shape: tuple, dropout_rate: float = 0.2) -> Sequential:
        """
        Build LSTM model architecture
        
        Args:
            input_shape (tuple): Input shape for LSTM
            dropout_rate (float): Dropout rate for regularization
        
        Returns:
            Sequential: Compiled LSTM model
        """
        model = Sequential([
            # First LSTM layer
            LSTM(50, return_sequences=True, input_shape=input_shape),
            BatchNormalization(),
            Dropout(dropout_rate),
            
            # Second LSTM layer
            LSTM(50, return_sequences=True),
            BatchNormalization(),
            Dropout(dropout_rate),
            
            # Third LSTM layer
            LSTM(50, return_sequences=False),
            BatchNormalization(),
            Dropout(dropout_rate),
            
            # Dense layers
            Dense(25, activation='relu'),
            Dropout(dropout_rate),
            Dense(1, activation='linear')  # Linear activation for regression
        ])
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, data: pd.DataFrame, epochs: int = 50, batch_size: int = 32, 
              lookback: int = 60, save_model: bool = True) -> dict:
        """
        Train LSTM model
        
        Args:
            data (pd.DataFrame): Historical price data
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            lookback (int): Number of previous days for prediction
            save_model (bool): Whether to save the trained model
        
        Returns:
            dict: Training results and metrics
        """
        if len(data) < lookback + 100:
            raise ValueError(f"Insufficient data. Need at least {lookback + 100} days, got {len(data)}")
        
        # Prepare data
        X_train, y_train, X_test, y_test = self.prepare_data(data, lookback)
        
        # Build model
        self.model = self.build_model((X_train.shape[1], 1))
        
        # Callbacks
        early_stopping = EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        reduce_lr = ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=0.00001
        )
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_test, y_test),
            callbacks=[early_stopping, reduce_lr],
            verbose=0
        )
        
        # Evaluate model
        train_pred = self.model.predict(X_train)
        test_pred = self.model.predict(X_test)
        
        # Inverse transform predictions
        train_pred = self.scaler.inverse_transform(train_pred)
        test_pred = self.scaler.inverse_transform(test_pred)
        y_train_orig = self.scaler.inverse_transform(y_train.reshape(-1, 1))
        y_test_orig = self.scaler.inverse_transform(y_test.reshape(-1, 1))
        
        # Calculate metrics
        metrics = {
            'train_mae': mean_absolute_error(y_train_orig, train_pred),
            'test_mae': mean_absolute_error(y_test_orig, test_pred),
            'train_rmse': np.sqrt(mean_squared_error(y_train_orig, train_pred)),
            'test_rmse': np.sqrt(mean_squared_error(y_test_orig, test_pred)),
            'train_mape': np.mean(np.abs((y_train_orig - train_pred) / y_train_orig)) * 100,
            'test_mape': np.mean(np.abs((y_test_orig - test_pred) / y_test_orig)) * 100
        }
        
        # Save model if requested
        if save_model:
            self.save_model()
        
        return {
            'metrics': metrics,
            'history': self.history.history,
            'predictions': {
                'train': train_pred.flatten(),
                'test': test_pred.flatten()
            }
        }
    
    def predict(self, data: pd.DataFrame, days_ahead: int = 7, lookback: int = 60) -> dict:
        """
        Make predictions for future prices
        
        Args:
            data (pd.DataFrame): Historical price data
            days_ahead (int): Number of days to predict ahead
            lookback (int): Number of previous days to use
        
        Returns:
            dict: Predictions and confidence intervals
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        if len(data) < lookback:
            raise ValueError(f"Insufficient data. Need at least {lookback} days, got {len(data)}")
        
        # Prepare the last sequence
        prices = data[['Close']].values
        scaled_prices = self.scaler.transform(prices)
        last_sequence = scaled_prices[-lookback:].reshape(1, lookback, 1)
        
        predictions = []
        current_sequence = last_sequence.copy()
        
        # Make predictions step by step
        for _ in range(days_ahead):
            pred = self.model.predict(current_sequence, verbose=0)
            predictions.append(pred[0, 0])
            
            # Update sequence for next prediction
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1, 0] = pred[0, 0]
        
        # Inverse transform predictions
        predictions = np.array(predictions).reshape(-1, 1)
        predictions = self.scaler.inverse_transform(predictions).flatten()
        
        # Calculate confidence intervals (simplified approach)
        last_price = data['Close'].iloc[-1]
        volatility = data['Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
        
        confidence_intervals = []
        for i, pred in enumerate(predictions):
            # Confidence widens with time horizon
            confidence_factor = 1 + (volatility * np.sqrt((i + 1) / 252))
            lower_bound = pred / confidence_factor
            upper_bound = pred * confidence_factor
            confidence_intervals.append((lower_bound, upper_bound))
        
        return {
            'predictions': predictions,
            'confidence_intervals': confidence_intervals,
            'last_price': last_price,
            'volatility': volatility
        }
    
    def save_model(self, symbol: str = "default"):
        """Save trained model and scaler"""
        if self.model is None:
            raise ValueError("No model to save")
        
        # Save model
        model_path = os.path.join(self.model_dir, f"lstm_model_{symbol}.h5")
        self.model.save(model_path)
        
        # Save scaler
        scaler_path = os.path.join(self.model_dir, f"scaler_{symbol}.pkl")
        import pickle
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        return True
    
    def load_model(self, symbol: str = "default"):
        """Load trained model and scaler"""
        model_path = os.path.join(self.model_dir, f"lstm_model_{symbol}.h5")
        scaler_path = os.path.join(self.model_dir, f"scaler_{symbol}.pkl")
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            return False
        
        # Load model
        self.model = tf.keras.models.load_model(model_path)
        
        # Load scaler
        import pickle
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        return True
    
    def get_model_summary(self) -> dict:
        """Get model summary and training info"""
        if self.model is None:
            return {"status": "No model trained"}
        
        return {
            "status": "Model trained",
            "parameters": self.model.count_params(),
            "layers": len(self.model.layers),
            "input_shape": self.model.input_shape,
            "output_shape": self.model.output_shape
        }
