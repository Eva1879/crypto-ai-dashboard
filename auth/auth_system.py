"""
User Authentication System - Phase 3
This module handles user authentication and session management.
"""

import hashlib
import json
import os
import streamlit as st
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import secrets

class AuthSystem:
    def __init__(self, users_file: str = "data/users.json"):
        """
        Initialize authentication system
        
        Args:
            users_file (str): Path to users database file
        """
        self.users_file = users_file
        self.ensure_data_directory()
        self.users = self.load_users()
        self.session_timeout = 3600  # 1 hour
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
    
    def load_users(self) -> Dict:
        """Load users from file"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            else:
                return self.create_default_users()
        except Exception as e:
            st.error(f"Error loading users: {e}")
            return self.create_default_users()
    
    def create_default_users(self) -> Dict:
        """Create default users database"""
        return {
            "users": {},
            "sessions": {},
            "created_at": datetime.now().isoformat()
        }
    
    def save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving users: {e}")
            return False
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, username: str, email: str, password: str, 
                     risk_profile: str = 'moderate') -> Dict:
        """
        Register a new user
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Password
            risk_profile (str): Risk preference
        
        Returns:
            dict: Registration result
        """
        # Validate inputs
        if not username or len(username) < 3:
            return {"success": False, "message": "Username must be at least 3 characters"}
        
        if not email or '@' not in email:
            return {"success": False, "message": "Valid email required"}
        
        if not password or len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters"}
        
        # Check if user already exists
        if username in self.users["users"]:
            return {"success": False, "message": "Username already exists"}
        
        # Check if email already exists
        for user_data in self.users["users"].values():
            if user_data.get("email") == email:
                return {"success": False, "message": "Email already registered"}
        
        # Create user
        user_data = {
            "username": username,
            "email": email,
            "password_hash": self.hash_password(password),
            "risk_profile": risk_profile,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
            "preferences": {
                "default_cryptocurrency": "BTC-USD",
                "default_timeframe": "1mo",
                "notifications_enabled": True
            }
        }
        
        self.users["users"][username] = user_data
        self.save_users()
        
        return {"success": True, "message": "User registered successfully"}
    
    def login_user(self, username: str, password: str) -> Dict:
        """
        Authenticate user login
        
        Args:
            username (str): Username
            password (str): Password
        
        Returns:
            dict: Login result
        """
        if not username or not password:
            return {"success": False, "message": "Username and password required"}
        
        # Check if user exists
        if username not in self.users["users"]:
            return {"success": False, "message": "Invalid username or password"}
        
        user_data = self.users["users"][username]
        
        # Check if user is active
        if not user_data.get("is_active", True):
            return {"success": False, "message": "Account is deactivated"}
        
        # Verify password
        if user_data["password_hash"] != self.hash_password(password):
            return {"success": False, "message": "Invalid username or password"}
        
        # Generate session token
        session_token = self.generate_session_token()
        
        # Store session
        self.users["sessions"][session_token] = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        # Update last login
        user_data["last_login"] = datetime.now().isoformat()
        self.save_users()
        
        return {
            "success": True,
            "message": "Login successful",
            "session_token": session_token,
            "user_data": {
                "username": username,
                "email": user_data["email"],
                "risk_profile": user_data["risk_profile"],
                "preferences": user_data.get("preferences", {})
            }
        }
    
    def logout_user(self, session_token: str) -> Dict:
        """
        Logout user by invalidating session
        
        Args:
            session_token (str): Session token
        
        Returns:
            dict: Logout result
        """
        if session_token in self.users["sessions"]:
            del self.users["sessions"][session_token]
            self.save_users()
            return {"success": True, "message": "Logged out successfully"}
        
        return {"success": False, "message": "Invalid session"}
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """
        Validate session token
        
        Args:
            session_token (str): Session token
        
        Returns:
            dict: User data if valid, None otherwise
        """
        if not session_token or session_token not in self.users["sessions"]:
            return None
        
        session = self.users["sessions"][session_token]
        last_activity = datetime.fromisoformat(session["last_activity"])
        
        # Check if session has expired
        if datetime.now() - last_activity > timedelta(seconds=self.session_timeout):
            del self.users["sessions"][session_token]
            self.save_users()
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now().isoformat()
        
        # Get user data
        username = session["username"]
        if username in self.users["users"]:
            user_data = self.users["users"][username]
            return {
                "username": username,
                "email": user_data["email"],
                "risk_profile": user_data["risk_profile"],
                "preferences": user_data.get("preferences", {})
            }
        
        return None
    
    def update_user_preferences(self, username: str, preferences: Dict) -> Dict:
        """
        Update user preferences
        
        Args:
            username (str): Username
            preferences (dict): New preferences
        
        Returns:
            dict: Update result
        """
        if username not in self.users["users"]:
            return {"success": False, "message": "User not found"}
        
        user_data = self.users["users"]
        if "preferences" not in user_data[username]:
            user_data[username]["preferences"] = {}
        
        user_data[username]["preferences"].update(preferences)
        self.save_users()
        
        return {"success": True, "message": "Preferences updated"}
    
    def get_user_stats(self, username: str) -> Dict:
        """
        Get user statistics
        
        Args:
            username (str): Username
        
        Returns:
            dict: User statistics
        """
        if username not in self.users["users"]:
            return {}
        
        user_data = self.users["users"][username]
        
        # Calculate account age
        created_at = datetime.fromisoformat(user_data["created_at"])
        account_age = datetime.now() - created_at
        
        return {
            "username": username,
            "email": user_data["email"],
            "risk_profile": user_data["risk_profile"],
            "account_age_days": account_age.days,
            "last_login": user_data.get("last_login"),
            "is_active": user_data.get("is_active", True),
            "preferences": user_data.get("preferences", {})
        }
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for token, session in self.users["sessions"].items():
            last_activity = datetime.fromisoformat(session["last_activity"])
            if current_time - last_activity > timedelta(seconds=self.session_timeout):
                expired_sessions.append(token)
        
        for token in expired_sessions:
            del self.users["sessions"][token]
        
        if expired_sessions:
            self.save_users()
    
    def get_all_users(self) -> List[Dict]:
        """Get list of all users (admin function)"""
        users_list = []
        for username, user_data in self.users["users"].items():
            users_list.append({
                "username": username,
                "email": user_data["email"],
                "risk_profile": user_data["risk_profile"],
                "created_at": user_data["created_at"],
                "last_login": user_data.get("last_login"),
                "is_active": user_data.get("is_active", True)
            })
        
        return users_list

# Streamlit integration functions
def init_auth_state():
    """Initialize authentication state in Streamlit"""
    if 'auth_system' not in st.session_state:
        st.session_state.auth_system = AuthSystem()
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None

def require_auth():
    """Require authentication to access page"""
    init_auth_state()
    
    # Validate existing session
    if st.session_state.session_token:
        user_data = st.session_state.auth_system.validate_session(st.session_state.session_token)
        if user_data:
            st.session_state.current_user = user_data
            return True
        else:
            # Session expired
            st.session_state.current_user = None
            st.session_state.session_token = None
            st.error("Session expired. Please login again.")
    
    return False

def login_page():
    """Display login page"""
    st.title("🔐 Login to Crypto AI Dashboard")
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if username and password:
                result = st.session_state.auth_system.login_user(username, password)
                if result["success"]:
                    st.session_state.current_user = result["user_data"]
                    st.session_state.session_token = result["session_token"]
                    st.success(result["message"])
                    st.rerun()
                else:
                    st.error(result["message"])
            else:
                st.error("Please enter username and password")

def register_page():
    """Display registration page"""
    st.title("📝 Register for Crypto AI Dashboard")
    
    with st.form("register_form"):
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        risk_profile = st.selectbox("Risk Profile", ["conservative", "moderate", "aggressive"])
        submitted = st.form_submit_button("Register")
        
        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match")
            elif username and email and password:
                result = st.session_state.auth_system.register_user(username, email, password, risk_profile)
                if result["success"]:
                    st.success(result["message"])
                    st.info("Please login with your new credentials")
                else:
                    st.error(result["message"])
            else:
                st.error("Please fill all fields")

def logout():
    """Logout current user"""
    if st.session_state.session_token:
        st.session_state.auth_system.logout_user(st.session_state.session_token)
        st.session_state.current_user = None
        st.session_state.session_token = None
        st.success("Logged out successfully")
        st.rerun()
