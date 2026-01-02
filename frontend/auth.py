# frontend/auth.py - FIXED VERSION (No st.query_params)
import streamlit as st
import requests
import time
import base64
from pathlib import Path

class AuthManager:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize all session state variables"""
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
            'auth_header': {},
            'login_mode': 'backend'  # Added login mode to session state
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def login(self, username, password, use_backend=True):
        """Authenticate user - tries real API or demo based on choice"""
        if use_backend:
            return self._backend_login(username, password)
        else:
            return self._demo_login(username, password)
    
    def _backend_login(self, username, password):
        """Authenticate with FastAPI backend using OAuth2"""
        try:
            # Use the standard OAuth2 /token endpoint
            response = requests.post(
                f"{self.api_url}/token",
                data={"username": username, "password": password},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self._save_login_data(data, username, real_api=True)
                return True
            else:
                # Try the /api/login endpoint as fallback
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
                    st.error(f"❌ Login failed: {response.status_code}")
                    return False
                
        except requests.exceptions.ConnectionError:
            st.warning("🔌 Backend API not available. Switch to demo mode.")
            return False
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")
            return False
    
    def _demo_login(self, username, password):
        """Demo authentication"""
        demo_users = {
            "bora_malaj": {
                "password": "admin123", 
                "role": "admin",
                "user_id": 1,
                "email": "bora@shinyjar.com",
                "full_name": "Bora Malaj",
                "business_id": 1
            },
            "gerta_tirana": {
                "password": "admin123",
                "role": "supplier", 
                "supplier_id": 1,
                "email": "gerta@silverworld.com",
                "full_name": "Gerta Tirana",
                "company": "Silver World Inc."
            },
            "arsjana_shehaj": {
                "password": "admin123",
                "role": "customer",
                "customer_id": 101,  # Assuming she's customer ID 101
                "email": "arsjana@email.com",
                "full_name": "Arsjana Shehaj",
                "total_spent": 1850.75
            },
            # Keep original demo users as backup
            "admin": {
                "password": "admin123", 
                "role": "admin",
                "user_id": 1,
                "email": "admin@shinyjar.com",
                "full_name": "Admin User"
            },
            "customer1": {
                "password": "customer123",
                "role": "customer", 
                "customer_id": 1,
                "email": "maria@email.com",
                "full_name": "Maria Silva"
            },
            "supplier1": {
                "password": "supplier123",
                "role": "supplier",
                "supplier_id": 1,
                "email": "john@supplier.com",
                "full_name": "John Supplier"
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
        keys_to_keep = ['api_url', 'login_mode']  # Keep API URL and login mode
        
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

# ====================== Image converstion section - Test for logo.png ======================================
# Check also /frontend/assets/image.py file
# Method to convert my logo image to base64 string
def img_to_bytes(img_path):
    """Converts an image file to a Base64 string."""
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# Create a dummy PNG file for demonstration purposes (replace with your actual file)
# In a real scenario, ensure 'my_image.png' exists in your directory
try:
    from PIL import Image
    import numpy as np
    img_data = np.zeros((150, 200, 3), dtype=np.uint8)
    img_data[25:125, 25:175] = [255, 0, 0] # Red rectangle
    img = Image.fromarray(img_data, 'RGB')
    img.save('my_image.png')
except ImportError:
    st.warning("Install Pillow (`pip install Pillow`) to run the dummy image creation part.")

png_path = 'logo.png'
png_base64 = img_to_bytes(png_path)

svg_string = f"""
<svg width="200" height="150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image href="data:image/png;base64,{png_base64}" x="0" y="0" width="100%" height="100%"/>
</svg>
"""
# =============================== End of Image convertion section ==============================================

# Create global instance
auth = AuthManager()

def show_login_page():
    """Login page with backend/demo toggle - SIMPLIFIED VERSION"""
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Hide sidebar and center everything */
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
        max-width: 500px !important;
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
    
    /* Logo section */
    .logo-section {
        text-align: center !important;
        margin-bottom: 30px !important;
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
    
    /* Mode selector */
    .mode-selector {
        margin-bottom: 25px !important;
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
    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 17px !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }
    
    .stButton > button:hover {
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
    
    # Use columns to center
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Display the logo image with specified size and style
        col1, col2 = st.columns([0.1, 0.9])  # Adjust columns for spacing

        # with col1:
        #     # st.image("logo.png", caption="", width=64)
        #     st.markdown('<div class="logo-section"><div class="logo-icon">💎</div></div>', unsafe_allow_html=True)

        # with col2:
        #     st.markdown('''
        #     <div class="logo-section">
        #         <div class="logo-title">Shiny Jar</div>
        #         <p class="logo-subtitle">Professional Jewelry CRM</p>
        #     </div>
        #     ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="logo-section">
            <div class="logo-icon">💎</div>            
            <div class="logo-title">Shiny Jar</div>
            <p class="logo-subtitle">Professional Jewelry CRM</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Mode selection
        st.markdown('<div class="mode-selector">', unsafe_allow_html=True)
        login_mode = st.radio(
            "Select Login Mode:",
            ["🔌 Backend Mode (Real Database)", "🎮 Demo Mode (Sample Data)"],
            index=0 if st.session_state.get('login_mode', 'backend') == 'backend' else 1,
            horizontal=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show current mode info
        if "Backend" in login_mode:
            st.info("🔌 **Backend Mode**: Connect to FastAPI server at http://localhost:8000")
            use_backend = True
            st.session_state.login_mode = 'backend'
        else:
            st.info("🎮 **Demo Mode**: Using local demo accounts")
            use_backend = False
            st.session_state.login_mode = 'demo'
        
        # Login form
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
            
            submitted = st.form_submit_button(
                f"{'🔌 Login with Backend' if use_backend else '🎮 Login with Demo'}",
                use_container_width=True
            )
        
        # Handle login outside the form to avoid callback issues
        if submitted:
            if not username or not password:
                st.error("❌ Please enter both username and password")
            else:
                with st.spinner(f"{'🔌 Authenticating with backend...' if use_backend else '🎮 Loading demo mode...'}"):
                    if auth.login(username, password, use_backend=use_backend):
                        st.success("✅ Login successful! Redirecting...")
                        time.sleep(1.2)
                        st.rerun()
                    else:
                        if use_backend:
                            st.error("❌ Login failed. Check:")
                            st.markdown("""
                            - Backend server is running: `uvicorn app.main:app --reload`
                            - Database is running: `docker-compose up -d`
                            - API is accessible: http://localhost:8000/docs
                            - Username/password exist in database
                            """)
                            
                            # Add a separate button to switch mode (not in form)
                            if st.button("🔄 Switch to Demo Mode", key="switch_to_demo"):
                                st.session_state.login_mode = 'demo'
                                st.rerun()
                        else:
                            st.error("❌ Invalid demo credentials")
        
        # Demo credentials (always show)
        st.markdown('''
        <div class="demo-section">
            <div class="demo-title">
                <span>📋</span>
                <span>Demo Accounts (Use in Demo Mode)</span>
            </div>
            
            <div class="demo-account">
                <div class="demo-role">
                    <span>👑</span>
                    <span>Business Owner / Admin</span>
                </div>
                <div class="demo-credentials">
                    <div class="demo-field">
                        <div class="demo-label">Username</div>
                        <div class="demo-value">bora_malaj</div>
                    </div>
                    <div class="demo-field">
                        <div class="demo-label">Password</div>
                        <div class="demo-value">admin123</div>
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
                        <div class="demo-value">gerta_tirana</div>
                    </div>
                    <div class="demo-field">
                        <div class="demo-label">Password</div>
                        <div class="demo-value">admin123</div>
                    </div>
                </div>
            </div>
            
            <div class="demo-account">
                <div class="demo-role">
                    <span>👤</span>
                    <span>Customer</span>
                </div>
                <div class="demo-credentials">
                    <div class="demo-field">
                        <div class="demo-label">Username</div>
                        <div class="demo-value">arsjana_shehaj</div>
                    </div>
                    <div class="demo-field">
                        <div class="demo-label">Password</div>
                        <div class="demo-value">admin123</div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 15px; font-size: 0.9rem; color: #94A3B8; text-align: center;">
                💡 <em>For Backend Mode, use your actual database users</em>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Footer
        st.markdown('''
        <div class="login-footer">
            💎 New York University Project • Jewelry Business CRM • Bora Malaj<br>
            <small>Backend: FastAPI | Frontend: Streamlit | Database: PostgreSQL</small>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close login card
        st.markdown('</div>', unsafe_allow_html=True)  # Close login container