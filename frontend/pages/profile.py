# frontend/pages/profile.py
import streamlit as st
import requests
from auth import auth

def show_profile_page():
    st.title("👤 My Profile")
    
    # Get current user info
    try:
        headers = auth.get_auth_header()
        response = requests.get(
            f"{auth.api_url}/api/users/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            
            # Display user info
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Info")
                st.write(f"**Username:** {user_data['username']}")
                st.write(f"**Role:** {user_data['role']}")
                st.write(f"**Member since:** {user_data['created_at'][:10]}")
            
            with col2:
                # Update profile form
                with st.expander("📝 Update Profile", expanded=False):
                    with st.form("update_profile_form"):
                        new_email = st.text_input("Email", value=user_data.get('email', ''))
                        new_full_name = st.text_input("Full Name", value=user_data.get('full_name', ''))
                        
                        if st.form_submit_button("Update Profile"):
                            update_data = {}
                            if new_email != user_data.get('email'):
                                update_data['email'] = new_email
                            if new_full_name != user_data.get('full_name'):
                                update_data['full_name'] = new_full_name
                            
                            if update_data:
                                update_response = requests.put(
                                    f"{auth.api_url}/api/users/me",
                                    headers=headers,
                                    json=update_data
                                )
                                
                                if update_response.status_code == 200:
                                    st.success("Profile updated successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to update profile")
            
            # Password change section
            st.markdown("---")
            st.subheader("🔒 Change Password")
            
            with st.form("change_password_form"):
                current_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password", 
                                           help="Minimum 6 characters")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Change Password"):
                    if not current_password or not new_password or not confirm_password:
                        st.error("All fields are required")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    elif len(new_password) < 6:
                        st.error("New password must be at least 6 characters")
                    else:
                        try:
                            change_response = requests.post(
                                f"{auth.api_url}/api/users/change-password",
                                headers=headers,
                                json={
                                    "current_password": current_password,
                                    "new_password": new_password
                                }
                            )
                            
                            if change_response.status_code == 200:
                                st.success("✅ Password changed successfully!")
                                # Clear the form
                                st.session_state['change_password_form'] = {}
                            elif change_response.status_code == 400:
                                error_data = change_response.json()
                                st.error(f"Password change failed: {error_data.get('detail', 'Unknown error')}")
                            else:
                                st.error(f"Password change failed with status {change_response.status_code}")
                                
                        except Exception as e:
                            st.error(f"Connection error: {str(e)}")
            
            # Admin actions (only for admins)
            if auth.has_role('admin'):
                st.markdown("---")
                st.subheader("👑 Admin Actions")
                
                with st.expander("User Management", expanded=False):
                    # List all users
                    users_response = requests.get(
                        f"{auth.api_url}/api/users",
                        headers=headers
                    )
                    
                    if users_response.status_code == 200:
                        all_users = users_response.json()
                        
                        for user in all_users:
                            col_a, col_b, col_c = st.columns([3, 2, 2])
                            with col_a:
                                st.write(f"**{user['username']}** ({user['role']})")
                            with col_b:
                                st.write("Active" if user['is_active'] else "Inactive")
                            with col_c:
                                if st.button("Toggle", key=f"toggle_{user['id']}"):
                                    # Implement activate/deactivate
                                    pass
                    else:
                        st.info("User management requires additional endpoints")
        
        else:
            st.error("Failed to load profile information")
            
    except Exception as e:
        st.error(f"Error loading profile: {str(e)}")