# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 13:30:35 2025

@author: Oreoluwa
"""

import streamlit as st
from pypdf import PdfReader
from groq import Groq
from auth import get_connection


st.title("AI-Powered Resumer Analyzer")

api_key = os.getenv("api_key")
def upload_resume():
    resume = st.file_uploader("Please upload your resume (PDF or DOCX)")
    if resume:
        reader = PdfReader(resume)
        
        for i in range(0,len(reader.pages)):
            page = reader.pages[i]
            content = ''.join(page.extract_text())
            return content

def save_resume(resume,id):
    with get_connection() as conn:
        conn.execute("UPDATE users SET resume=? WHERE id=?",(resume,id))
        conn.commit()


 
#Fuction to analyze resumes   
def analyze(content):    
    response = ''
    client = Groq(api_key= api_key)
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
          {
            "role": "user",
            "content": f"Please analyze this resume {content} and only give me tips on how to improve it"
          }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
        
    st.write(response)
    
 
#Function to create corrected resumes
def correct(content):
    response = ''
    client = Groq(api_key= api_key)
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
          {
            "role": "system",
            "content": f"Please help me create an improved version of this resume {content}. Don't add any greetings or acknowledgments at all or anything apart from the improved resume in the output"
          }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
        
    return response


def tailor_resume(resume,description):
    response = ''
    client = Groq(api_key= api_key)
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
          {
            "role": "system",
            "content": f"Please help me tailor this resume {resume} to this job description {description}. Don't add any greetings or acknowledgments at all or anything apart from the tailored resume in the output"
          }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    for chunk in completion:
        if chunk.choices[0].delta.content:
            response += chunk.choices[0].delta.content
        
    return response

        
def main_app():
    
        st.session_state.page = "main"
    
        
        if not st.session_state.resume:
            content = upload_resume()
            st.session_state.resume = content
            save_resume(content, st.session_state.user['id'])
            st.success("Resume saved successfully")
            
            
        
        choice = st.selectbox("What do you want to do",["Analyze your resume","Correct your resume"])
        submitted = st.button("SUBMIT")
        
        if submitted:
            if choice == "Analyze your resume":
                analyze(content)
                
            elif choice == "Correct your resume":
                new_resume = correct(content)
                st.write(new_resume)
                
                try:
                    download = st.download_button("Download corrected resume", new_resume, "corrected_resume.pdf", "pdf")
                    if download:
                        st.write("Download successful")
                except:
                    st.write("Download Failed")
                    

                    
 
            
if __name__ == "__main__":
    main_app()
