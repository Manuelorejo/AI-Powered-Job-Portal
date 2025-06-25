# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 11:47:39 2025

@author: Oreoluwa
"""

from auth import create_users_table,Login_user,Register_user, validate_email,hash_password
from main import main_app
import streamlit as st


def show_register():
    st.subheader("📝Register")
    with st.form("Registration Form"):
        email = st.text_input("Email: ")
        username = st.text_input("Username: ")
        password = st.text_input("Password: ", type = 'password')
        confirm = st.text_input('Confirm Password: ', type = 'password')
        
        
        submitted = st.form_submit_button("SUBMIT")
        
        if submitted:
            
            if email and username and password and confirm:
            
                if password == confirm:
                    
                    if validate_email(email):
                        registered,msg = Register_user(email, username, password)
                        if registered:
                            st.write(msg)
                        else:
                            st.error(msg)
                        
                    else:
                        st.error("Invalid Email")
        
                
                else:
                    st.error("Passwords don't match")
                    
            else:
                st.error("All fields are required")
  
                

def show_login():
    st.subheader("🔐Login")
    with st.form("Login Form"):
        email = st.text_input("Email: ")
        password = st.text_input("Password: ",type='password')
    
        submitted = st.form_submit_button("SUBMIT")
        
        if submitted:
            
            if email and password:
                user = Login_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.resume = user['resume']
                    st.rerun()
                    #st.write(f"Welcome {user['username']}")
                    
                else:
                    st.write("Invalid Credentials")
                    
            else:
                st.error("All fields are required")
        
                

def main():
    create_users_table()
    
    
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    
    
    if st.session_state.logged_in:
        
        with st.sidebar:
            st.markdown(f"Welcome {st.session_state.user['username']}")
            
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.user = {}
                st.rerun()
                
        main_app()
        
            
    else:
        
        page = st.sidebar.radio("Select Page",['Login','Register'])
        if page == 'Login':
            show_login()
            
        elif page == 'Register':
            show_register()
        
        
        
        
            
            

if __name__ == "__main__":
    main()
    