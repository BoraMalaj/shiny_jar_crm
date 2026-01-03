# frontend/pages/register.py
import streamlit as st
import requests
import re
from auth import auth

def show_register_page():
    st.title("👤 Register New User")
    
    with st.form("register_form"):
        st.subheader("Create Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username *", help="Unique username for login")
            full_name = st.text_input("Full Name")
        
        with col2:
            email = st.text_input("Email")
            password = st.text_input("Password *", type="password", 
                                   help="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        role = st.selectbox(
            "Role *",
            ["user", "customer", "supplier", "admin"],
            help="Admin role requires special permissions"
        )
        
        submitted = st.form_submit_button("Register")
        
        if submitted:
            # Validation
            errors = []
            
            if not username:
                errors.append("Username is required")
            if not password:
                errors.append("Password is required")
            if password != confirm_password:
                errors.append("Passwords do not match")
            if len(password) < 6:
                errors.append("Password must be at least 6 characters")
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Invalid email format")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                try:
                    # Call registration API
                    response = requests.post(
                        f"{auth.api_url}/api/users/register",
                        json={
                            "username": username,
                            "email": email if email else None,
                            "full_name": full_name,
                            "password": password,
                            "role": role
                        }
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Account created successfully!")
                        st.info("You can now login with your credentials")
                        
                        # Auto-fill login form
                        st.session_state['register_username'] = username
                        st.session_state['register_password'] = password
                        
                        # Switch to login
                        st.button("Go to Login", on_click=lambda: st.session_state.update({'page': 'login'}))
                        
                    elif response.status_code == 400:
                        error_data = response.json()
                        st.error(f"Registration failed: {error_data.get('detail', 'Unknown error')}")
                    else:
                        st.error(f"Registration failed with status {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                    st.info("Make sure the backend server is running")
    
    # Admin note
    if auth.get_user_role() == 'admin':
        st.markdown("---")
        st.info("💡 **Admin Note:** New users will have limited access until approved.")