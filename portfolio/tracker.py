"""
Portfolio Tracking Module - Phase 3
This module manages cryptocurrency portfolio tracking and performance analysis.
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st

class PortfolioTracker:
    def __init__(self, data_file: str = "data/portfolio.json"):
        """
        Initialize portfolio tracker
        
        Args:
            data_file (str): Path to portfolio data file
        """
        self.data_file = data_file
        self.ensure_data_directory()
        self.portfolio_data = self.load_portfolio()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def load_portfolio(self) -> Dict:
        """Load portfolio data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            else:
                return self.create_default_portfolio()
        except Exception as e:
            st.error(f"Error loading portfolio: {e}")
            return self.create_default_portfolio()
    
    def create_default_portfolio(self) -> Dict:
        """Create default portfolio structure"""
        return {
            "holdings": {},
            "transactions": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def save_portfolio(self):
        """Save portfolio data to file"""
        try:
            self.portfolio_data["last_updated"] = datetime.now().isoformat()
            with open(self.data_file, 'w') as f:
                json.dump(self.portfolio_data, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving portfolio: {e}")
            return False
    
    def add_holding(self, symbol: str, amount: float, buy_price: float, buy_date: str = None):
        """
        Add cryptocurrency holding to portfolio
        
        Args:
            symbol (str): Cryptocurrency symbol
            amount (float): Amount of cryptocurrency
            buy_price (float): Purchase price per unit
            buy_date (str): Purchase date (ISO format)
        """
        if buy_date is None:
            buy_date = datetime.now().isoformat()
        
        symbol_key = symbol.replace('-USD', '')
        
        if symbol_key not in self.portfolio_data["holdings"]:
            self.portfolio_data["holdings"][symbol_key] = {
                "amount": 0,
                "total_invested": 0,
                "average_buy_price": 0,
                "transactions": []
            }
        
        holding = self.portfolio_data["holdings"][symbol_key]
        old_amount = holding["amount"]
        old_invested = holding["total_invested"]
        
        # Update holding
        holding["amount"] += amount
        holding["total_invested"] += (amount * buy_price)
        holding["average_buy_price"] = holding["total_invested"] / holding["amount"]
        
        # Add transaction
        transaction = {
            "type": "buy",
            "amount": amount,
            "price": buy_price,
            "date": buy_date,
            "total": amount * buy_price
        }
        holding["transactions"].append(transaction)
        self.portfolio_data["transactions"].append({
            **transaction,
            "symbol": symbol_key
        })
        
        self.save_portfolio()
        return True
    
    def remove_holding(self, symbol: str, amount: float, sell_price: float, sell_date: str = None):
        """
        Remove cryptocurrency from portfolio
        
        Args:
            symbol (str): Cryptocurrency symbol
            amount (float): Amount to sell
            sell_price (float): Sell price per unit
            sell_date (str): Sell date (ISO format)
        """
        if sell_date is None:
            sell_date = datetime.now().isoformat()
        
        symbol_key = symbol.replace('-USD', '')
        
        if symbol_key not in self.portfolio_data["holdings"]:
            st.error(f"No holding found for {symbol}")
            return False
        
        holding = self.portfolio_data["holdings"][symbol_key]
        
        if amount > holding["amount"]:
            st.error(f"Cannot sell more than you own. Available: {holding['amount']}")
            return False
        
        # Calculate profit/loss
        cost_basis = holding["average_buy_price"] * amount
        proceeds = amount * sell_price
        profit_loss = proceeds - cost_basis
        
        # Update holding
        holding["amount"] -= amount
        holding["total_invested"] -= cost_basis
        
        # Remove holding if amount is zero
        if holding["amount"] <= 0.00001:  # Account for floating point
            del self.portfolio_data["holdings"][symbol_key]
        
        # Add transaction
        transaction = {
            "type": "sell",
            "amount": amount,
            "price": sell_price,
            "date": sell_date,
            "total": proceeds,
            "profit_loss": profit_loss,
            "profit_loss_percent": (profit_loss / cost_basis * 100) if cost_basis > 0 else 0
        }
        
        if symbol_key in self.portfolio_data["holdings"]:
            holding["transactions"].append(transaction)
        
        self.portfolio_data["transactions"].append({
            **transaction,
            "symbol": symbol_key
        })
        
        self.save_portfolio()
        return True
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> Dict:
        """
        Calculate current portfolio value
        
        Args:
            current_prices (dict): Current prices for cryptocurrencies
        
        Returns:
            dict: Portfolio value analysis
        """
        total_value = 0
        total_invested = 0
        holdings_value = {}
        
        for symbol, holding in self.portfolio_data["holdings"].items():
            current_price = current_prices.get(f"{symbol}-USD", 0)
            if current_price == 0:
                current_price = current_prices.get(symbol, 0)
            
            holding_value = holding["amount"] * current_price
            holdings_value[symbol] = {
                "amount": holding["amount"],
                "current_price": current_price,
                "value": holding_value,
                "invested": holding["total_invested"],
                "profit_loss": holding_value - holding["total_invested"],
                "profit_loss_percent": ((holding_value - holding["total_invested"]) / holding["total_invested"] * 100) if holding["total_invested"] > 0 else 0,
                "average_buy_price": holding["average_buy_price"]
            }
            
            total_value += holding_value
            total_invested += holding["total_invested"]
        
        return {
            "total_value": total_value,
            "total_invested": total_invested,
            "total_profit_loss": total_value - total_invested,
            "total_profit_loss_percent": ((total_value - total_invested) / total_invested * 100) if total_invested > 0 else 0,
            "holdings": holdings_value,
            "number_of_holdings": len(self.portfolio_data["holdings"])
        }
    
    def get_transaction_history(self) -> pd.DataFrame:
        """Get transaction history as DataFrame"""
        if not self.portfolio_data["transactions"]:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.portfolio_data["transactions"])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        return df
    
    def get_performance_metrics(self, current_prices: Dict[str, float]) -> Dict:
        """
        Calculate portfolio performance metrics
        
        Args:
            current_prices (dict): Current prices
        
        Returns:
            dict: Performance metrics
        """
        portfolio_value = self.get_portfolio_value(current_prices)
        transactions = self.get_transaction_history()
        
        metrics = {
            "best_performer": None,
            "worst_performer": None,
            "total_transactions": len(transactions),
            "buy_transactions": len(transactions[transactions['type'] == 'buy']) if not transactions.empty else 0,
            "sell_transactions": len(transactions[transactions['type'] == 'sell']) if not transactions.empty else 0
        }
        
        # Find best and worst performers
        if portfolio_value["holdings"]:
            holdings = portfolio_value["holdings"]
            best = max(holdings.items(), key=lambda x: x[1]["profit_loss_percent"])
            worst = min(holdings.items(), key=lambda x: x[1]["profit_loss_percent"])
            
            metrics["best_performer"] = {
                "symbol": best[0],
                "profit_loss_percent": best[1]["profit_loss_percent"]
            }
            metrics["worst_performer"] = {
                "symbol": worst[0],
                "profit_loss_percent": worst[1]["profit_loss_percent"]
            }
        
        return metrics
    
    def reset_portfolio(self):
        """Reset portfolio to default state"""
        self.portfolio_data = self.create_default_portfolio()
        self.save_portfolio()
        return True
