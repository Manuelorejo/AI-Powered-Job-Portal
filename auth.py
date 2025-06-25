# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 09:30:26 2025

@author: Oreoluwa
"""

import streamlit as st
import sqlite3
import hashlib
import re


def get_connection():
    return sqlite3.connect('TempUsers.db',check_same_thread = False)
    

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern,email)


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def create_users_table():
    
    with get_connection() as conn:
        cursor = conn.cursor()
    
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            resume TEXT)
            ''')
            
        conn.commit()
    

def Login_user(email,password):
    email = email.lower()
    password = hash_password(password)
                 
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM users WHERE email = (?) and password = (?)''',(email,password))
        user = cursor.fetchone()
        
        
        
                    
                    
        if user:
            return { 'id': user[0], 'username': user[1], 'email': user[2], 'password': user[3],'resume':user[4]}
                
                            
        else:
            return None
        
                        
                

        
  
def Register_user(email,username,password):
    
    email = email.lower()
    
    password = hash_password(password)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO users(username,email,password) VALUES(?,?,?)''',(username,email,password))
            conn.commit()
            return True,"Registration Successful"
        
        except sqlite3.IntegrityError:
            return False,"Email already registered"
            
       