# frontend/auth.py - PROPERLY CENTERED LOGIN PAGE
import streamlit as st
import requests
import time

class AuthManager:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self._init_session_state()
    
    def _init_session_state(self):
        defaults = {
            'token': None,
            'user': None,
            'role': 'guest',
            'api_url': self.api_url,
            'logged_in': False,
            'customer_id': None,
            'supplier_id': None,
            'user_id': None,
            'username': 'Guest',
            'api_mode': 'demo',
            'auth_header': {}
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def login(self, username, password):
        """Authenticate with REAL backend API"""
        try:
            # Try real backend login first
            response = requests.post(
                f"{self.api_url}/api/login",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self._save_login_data(data, username, real_api=True)
                return True
            else:
                # If backend returns error, try demo login
                return self._demo_login(username, password)
                
        except requests.exceptions.ConnectionError:
            # Backend not available, use demo mode
            st.warning("🔌 Backend API not available. Using demo mode.")
            return self._demo_login(username, password)
        except Exception as e:
            st.error(f"❌ Login error: {str(e)}")
            return False
    
    def _demo_login(self, username, password):
        """Demo authentication when backend is unavailable"""
        demo_users = {
            "admin": {
                "password": "admin123", 
                "role": "admin",
                "user_id": 1,
                "email": "admin@shinyjar.com",
                "full_name": "Admin User",
                "business_id": 1
            },
            "customer1": {
                "password": "customer123",
                "role": "customer", 
                "customer_id": 1,
                "email": "maria@email.com",
                "full_name": "Maria Silva",
                "total_spent": 1250.75
            },
            "supplier1": {
                "password": "supplier123",
                "role": "supplier",
                "supplier_id": 1,
                "email": "john@supplier.com",
                "full_name": "John Supplier",
                "company": "Silver World Inc."
            },
            "customer2": {
                "password": "customer123",
                "role": "customer", 
                "customer_id": 2,
                "email": "john@email.com",
                "full_name": "John Doe",
                "total_spent": 890.50
            }
        }
        
        if username in demo_users and demo_users[username]["password"] == password:
            user_data = demo_users[username]
            
            mock_data = {
                "access_token": f"demo_token_{username}",
                "token_type": "bearer",
                "user": {
                    "username": username,
                    "role": user_data["role"],
                    "email": user_data["email"],
                    "full_name": user_data["full_name"],
                    **{k: v for k, v in user_data.items() if k not in ["password", "role"]}
                }
            }
            
            self._save_login_data(mock_data, username, real_api=False)
            return True
        
        return False
    
    def _save_login_data(self, data, username, real_api=True):
        """Save login data to session state"""
        st.session_state.token = data['access_token']
        st.session_state.user = data.get('user', {})
        st.session_state.role = data['user'].get('role', 'user')
        st.session_state.logged_in = True
        st.session_state.username = username
        
        # Store IDs for role-based features
        user_data = data['user']
        st.session_state.customer_id = user_data.get('customer_id')
        st.session_state.supplier_id = user_data.get('supplier_id')
        st.session_state.user_id = user_data.get('user_id')
        
        # Store API mode and auth header
        st.session_state.api_mode = "real" if real_api else "demo"
        
        # Create auth header for API calls
        if real_api:
            st.session_state.auth_header = {"Authorization": f"Bearer {data['access_token']}"}
        else:
            st.session_state.auth_header = {}
    
    def logout(self):
        """Clear all session state and logout"""
        keys_to_keep = ['api_url']  # Keep API URL
        
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        
        self._init_session_state()
        st.rerun()
    
    def is_authenticated(self):
        return st.session_state.get('logged_in', False)
    
    def get_user_role(self):
        return st.session_state.get('role', 'guest')
    
    def get_username(self):
        return st.session_state.get('username', 'Guest')
    
    def get_user_data(self):
        return st.session_state.get('user', {})
    
    def has_role(self, required_roles):
        if not isinstance(required_roles, list):
            required_roles = [required_roles]
        
        current_role = self.get_user_role()
        return current_role in required_roles
    
    def get_auth_header(self):
        return st.session_state.get('auth_header', {})
    
    def is_demo_mode(self):
        return st.session_state.get('api_mode', 'demo') == 'demo'

# Create global instance
auth = AuthManager()

def show_login_page():
    """Beautiful, perfectly centered login page"""
    
    # Hide sidebar and center everything
    st.markdown("""
    <style>
    /* Hide everything except login form */
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    #MainMenu,
    footer,
    header {
        display: none !important;
    }
    
    /* Center the main content */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }
    
    /* Full screen background */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 100%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 20px !important;
    }
    
    /* Login container */
    .login-container {
        width: 100% !important;
        max-width: 450px !important;
        margin: 0 auto !important;
        animation: fadeIn 0.6s ease-out !important;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Login card */
    .login-card {
        background: rgba(30, 41, 59, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 40px 35px !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Logo section - TOP POSITION */
    .logo-section {
        text-align: center !important;
        margin-bottom: 35px !important;
    }
    
    .logo-icon {
        font-size: 4.5rem !important;
        background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin-bottom: 15px !important;
        animation: float 3s ease-in-out infinite !important;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .logo-title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #F1F5F9 0%, #94A3B8 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin: 0 0 8px 0 !important;
        line-height: 1.2 !important;
    }
    
    .logo-subtitle {
        color: #94A3B8 !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
        font-weight: 400 !important;
    }
    
    /* Form styling */
    .form-group {
        margin-bottom: 20px !important;
    }
    
    .form-label {
        display: block !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
        font-size: 1rem !important;
    }
    
    /* Input fields */
    .stTextInput input {
        width: 100% !important;
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        font-size: 1.05rem !important;
        color: #F1F5F9 !important;
        transition: all 0.3s ease !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput input:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
        outline: none !important;
    }
    
    /* Login button */
    .login-button {
        width: 100% !important;
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 17px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }
    
    .login-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%) !important;
    }
    
    /* Demo section */
    .demo-section {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin-top: 30px !important;
        border-left: 4px solid #8B5CF6 !important;
    }
    
    .demo-title {
        color: #8B5CF6 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 15px !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }
    
    .demo-account {
        background: rgba(139, 92, 246, 0.1) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .demo-account:hover {
        background: rgba(139, 92, 246, 0.15) !important;
    }
    
    .demo-role {
        color: #8B5CF6 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }
    
    .demo-credentials {
        display: flex !important;
        gap: 15px !important;
    }
    
    .demo-field {
        flex: 1 !important;
    }
    
    .demo-label {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        margin-bottom: 5px !important;
    }
    
    .demo-value {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #F1F5F9 !important;
        padding: 10px 12px !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
        border: 1px solid #334155 !important;
    }
    
    /* Footer */
    .login-footer {
        text-align: center !important;
        color: #64748B !important;
        font-size: 0.9rem !important;
        margin-top: 25px !important;
        padding-top: 20px !important;
        border-top: 1px solid #334155 !important;
    }
    
    /* Placeholder */
    ::placeholder {
        color: #64748B !important;
        font-size: 1rem !important;
    }
    
    /* Error/Success messages */
    .stAlert {
        border-radius: 12px !important;
        margin-bottom: 15px !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .login-container {
            padding: 15px !important;
        }
        
        .login-card {
            padding: 30px 25px !important;
        }
        
        .logo-title {
            font-size: 2.2rem !important;
        }
        
        .logo-icon {
            font-size: 3.5rem !important;
        }
        
        .demo-credentials {
            flex-direction: column !important;
            gap: 10px !important;
        }
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #8B5CF6 transparent transparent transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use columns to center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo section - AT THE TOP
        st.markdown('''
        <div class="logo-section">
            <div class="logo-icon">💎</div>
            <div class="logo-title">Shiny Jar</div>
            <p class="logo-subtitle">Professional Jewelry CRM</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">👤 Username</label>', unsafe_allow_html=True)
            username = st.text_input(
                "",
                placeholder="Enter username",
                label_visibility="collapsed",
                key="login_username"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">🔒 Password</label>', unsafe_allow_html=True)
            password = st.text_input(
                "",
                type="password",
                placeholder="Enter password",
                label_visibility="collapsed",
                key="login_password"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🚀 Login to Dashboard", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                else:
                    with st.spinner("🔐 Authenticating..."):
                        if auth.login(username, password):
                            st.success("✅ Login successful! Redirecting...")
                            time.sleep(1.2)
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
        
        # Demo credentials
        st.markdown('''
        <div class="demo-section">
            <div class="demo-title">
                <span>📋</span>
                <span>Demo Accounts</span>
            </div>
            
            <div class="demo-account">
                <div class="demo-role">
                    <span>👑</span>
                    <span>Administrator</span>
                </div>
                <div class="demo-credentials">
                    <div class="demo-field">
                        <div class="demo-label">Username</div>
                        <div class="demo-value">admin</div>
                    </div>
                    <div class="demo-field">
                        <div class="demo-label">Password</div>
                        <div class="demo-value">admin123</div>
                    </div>
                </div>
            </div>
            
            <div class="demo-account">
                <div class="demo-role">
                    <span>👥</span>
                    <span>Customer</span>
                </div>
                <div class="demo-credentials">
                    <div class="demo-field">
                        <div class="demo-label">Username</div>
                        <div class="demo-value">customer1</div>
                    </div>
                    <div class="demo-field">
                        <div class="demo-label">Password</div>
                        <div class="demo-value">customer123</div>
                    </div>
                </div>
            </div>
            
            <div class="demo-account">
                <div class="demo-role">
                    <span>🏭</span>
                    <span>Supplier</span>
                </div>
                <div class="demo-credentials">
                    <div class="demo-field">
                        <div class="demo-label">Username</div>
                        <div class="demo-value">supplier1</div>
                    </div>
                    <div class="demo-field">
                        <div class="demo-label">Password</div>
                        <div class="demo-value">supplier123</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 15px; font-size: 0.9rem; color: #94A3B8; text-align: center;">
                💡 <em>Demo mode active. Connect to backend for real data.</em>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Footer
        st.markdown('''
        <div class="login-footer">
            💎 University Project • Jewelry Business CRM<br>
            <small>Built with FastAPI & Streamlit</small>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close login card
        st.markdown('</div>', unsafe_allow_html=True)  # Close login container