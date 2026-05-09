"""
AI Chatbot Module - Phase 2
This module provides AI-powered cryptocurrency analysis and Q&A functionality using free alternatives.
"""

import streamlit as st
from typing import Dict, List
import json
import os
from transformers import pipeline
import re
import warnings
warnings.filterwarnings('ignore')

class CryptoChatbot:
    def __init__(self):
        """
        Initialize the crypto chatbot using free Hugging Face models
        """
        try:
            # Initialize free text generation model
            self.generator = pipeline(
                "text-generation", 
                model="distilgpt2",
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=50256  # EOS token for GPT-2
            )
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
            self.generator = None
        
        self.conversation_history = []
        
    def get_crypto_context(self, symbol, data, rsi, recommendation):
        """
        Get current cryptocurrency context for the chatbot
        
        Args:
            symbol (str): Cryptocurrency symbol
            data (pd.DataFrame): Price data
            rsi (float): Current RSI value
            recommendation (dict): Current recommendation
        
        Returns:
            str: Context string for the AI
        """
        current_price = data['Close'].iloc[-1]
        price_change = ((data['Close'].iloc[-1] / data['Close'].iloc[-2] - 1) * 100) if len(data) > 1 else 0
        
        context = f"""
        Current Cryptocurrency Analysis for {symbol}:
        - Current Price: ${current_price:.2f}
        - 24h Change: {price_change:.2f}%
        - RSI: {rsi:.2f}
        - Recommendation: {recommendation['action']}
        - Trend: {recommendation.get('trend', 'unknown')}
        - Reasoning: {recommendation['reasoning']}
        
        You are a cryptocurrency expert assistant. Provide helpful, accurate, and balanced advice.
        Always mention that this is not financial advice and users should do their own research.
        """
        
        return context
    
    def ask_question(self, question, context=None):
        """
        Ask a question to the AI chatbot using free Hugging Face models
        
        Args:
            question (str): User's question
            context (str): Additional context about current crypto data
        
        Returns:
            str: AI response
        """
        if not self.model_loaded:
            return self.get_fallback_response(question, context)
        
        try:
            # Prepare prompt with context and question
            prompt = "You are a cryptocurrency expert assistant. "
            prompt += "Provide helpful, accurate, and balanced advice. "
            prompt += "Always mention that this is not financial advice and users should do their own research.\n\n"
            
            if context:
                prompt += f"Current Market Context:\n{context}\n\n"
            
            prompt += f"User Question: {question}\n\n"
            prompt += "Expert Response:"
            
            # Generate response using free model
            responses = self.generator(prompt, max_new_tokens=150, num_return_sequences=1)
            
            # Extract and clean the response
            answer = responses[0]['generated_text']
            answer = answer.replace(prompt, "").strip()
            
            # Clean up common issues with generated text
            answer = re.sub(r'User Question:.*', '', answer, flags=re.DOTALL)
            answer = re.sub(r'Current Market Context:.*', '', answer, flags=re.DOTALL)
            answer = answer.strip()
            
            if not answer or len(answer) < 10:
                return self.get_fallback_response(question, context)
            
            # Add disclaimer
            if "financial advice" not in answer.lower():
                answer += "\n\n*Note: This is not financial advice. Please do your own research.*"
            
            # Update conversation history
            self.conversation_history.append({"question": question, "answer": answer})
            
            return answer
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self.get_fallback_response(question, context)
    
    def get_fallback_response(self, question, context=None):
        """
        Get a fallback response when AI model is not available
        
        Args:
            question (str): User's question
            context (str): Additional context
        
        Returns:
            str: Fallback response
        """
        question_lower = question.lower()
        
        # Pattern-based responses for common questions
        if "rsi" in question_lower:
            return "RSI (Relative Strength Index) is a momentum oscillator that measures the speed and change of price movements. Values above 70 indicate overbought conditions, while values below 30 indicate oversold conditions. *Note: This is not financial advice.*"
        
        elif "buy" in question_lower or "sell" in question_lower:
            return "I recommend looking at multiple technical indicators including RSI, moving averages, and volume analysis before making trading decisions. Consider your risk tolerance and investment goals. *Note: This is not financial advice.*"
        
        elif "trend" in question_lower:
            return "Trend analysis involves looking at price movements over time. An uptrend is characterized by higher highs and higher lows, while a downtrend has lower highs and lower lows. Moving averages can help identify the overall trend direction. *Note: This is not financial advice.*"
        
        elif "risk" in question_lower:
            return "Risk management in crypto includes position sizing, setting stop-losses, diversification, and only investing what you can afford to lose. Consider the high volatility of cryptocurrency markets. *Note: This is not financial advice.*"
        
        else:
            return "I'm currently using a simplified response system. For detailed analysis, please refer to the technical indicators shown in the dashboard, including RSI, price action, and the AI recommendations. *Note: This is not financial advice.*"
    
    def get_suggested_questions(self):
        """
        Get list of suggested questions for users
        
        Returns:
            list: Suggested questions
        """
        return [
            "What does the current RSI indicate?",
            "Should I consider buying at this price?",
            "What are the key risk factors?",
            "How does the current trend look?",
            "What technical indicators should I watch?",
            "Explain the current market sentiment",
            "What's a good entry/exit strategy?",
            "How does this compare to historical patterns?"
        ]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

def create_chatbot_interface(chatbot, symbol, data, rsi, recommendation):
    """
    Create Streamlit chatbot interface
    
    Args:
        chatbot (CryptoChatbot): Chatbot instance
        symbol (str): Cryptocurrency symbol
        data (pd.DataFrame): Price data
        rsi (float): Current RSI value
        recommendation (dict): Current recommendation
    """
    st.subheader("💬 Ask AI Assistant")
    
    # Get context
    context = chatbot.get_crypto_context(symbol, data, rsi, recommendation)
    
    # Suggested questions
    with st.expander("💡 Suggested Questions"):
        suggested_questions = chatbot.get_suggested_questions()
        cols = st.columns(2)
        for i, question in enumerate(suggested_questions):
            col = cols[i % 2]
            if col.button(question, key=f"question_{i}"):
                st.session_state.user_question = question
    
    # User input
    user_question = st.text_input(
        "Ask about cryptocurrency analysis:",
        value=st.session_state.get('user_question', ''),
        key="chat_input"
    )
    
    # Ask button
    if st.button("Ask AI", key="ask_button") and user_question:
        with st.spinner("Thinking..."):
            response = chatbot.ask_question(user_question, context)
            st.success("🤖 AI Response:")
            st.write(response)
        
        # Clear the question from session state
        if 'user_question' in st.session_state:
            del st.session_state.user_question
    
    # Clear history button
    if st.button("Clear Conversation History"):
        chatbot.clear_history()
        st.info("Conversation history cleared.")
