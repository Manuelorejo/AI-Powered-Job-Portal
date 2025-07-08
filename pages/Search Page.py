import streamlit as st
import json
import sys
import os
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity




# Add the parent directory to the path to import the scraper modules correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import scraping functions
from Linkedln import linkedln
from Jobsguru import Jobsguru
from MyJobMag import MyJobMag
from hotnigerianjobs import hotnigerianjobs
from Jobberman import jobberman
from main import tailor_resume


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 You must be logged in to access this page.")
    st.stop()
    

    
model = SentenceTransformer('all-MiniLM-L6-v2')

if st.session_state.resume:
    resume = st.session_state.resume

# Set page title
st.set_page_config(
    page_title="Search Jobs - Nigerian Job Search Aggregator",
    page_icon="🔍",
    layout="wide"
)

# Enhanced CSS for styling with updated colors and borders
st.markdown("""
<style>
    body {
        background-color: #f5f5f5;
    }
    .job-card {
        background-color: #f0f0f0;
        border: 2px solid #000000;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        border-color: #333333;
    }
    .job-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 12px;
        color: #000000;
    }
    .job-meta {
        font-size: 15px;
        margin: 8px 0;
        color: #444444;
    }
    .job-source {
        font-weight: 500;
        color: #000000;
        background-color: #ffffff;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
    }
    .job-mode {
        font-weight: 500;
        color: #000000;
        background-color: #e6f7ff;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-left: 10px;
    }
    .apply-btn {
        background-color: #d3d3d3;
        color: black;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 15px;
        margin-top: 15px;
        border-radius: 5px;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }
    .apply-btn:hover {
        background-color: #c0c0c0;
    }
    .main-title {
        text-align: center;
        padding: 25px 0;
        margin-bottom: 35px;
        background: #000000;
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .search-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    .nav-btn {
        background-color: #f0f0f0;
        color: #333;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        margin-bottom: 20px;
        display: inline-block;
        text-decoration: none;
    }
    .nav-btn:hover {
        background-color: #e0e0e0;
    }
    .scraper-logo {
        width: 24px;
        height: 24px;
        margin-right: 8px;
        vertical-align: middle;
    }
    .scraper-status {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }
    .pulse {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #4CAF50;
        margin-right: 10px;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(76, 175, 80, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
        }
    }
    .search-animation {
        text-align: center;
        margin: 20px 0;
    }
    .search-animation i {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #333;
        margin: 0 5px;
    }
    .search-animation i:nth-child(1) {
        animation: bounce 1.5s ease-in-out infinite;
    }
    .search-animation i:nth-child(2) {
        animation: bounce 1.5s ease-in-out 0.2s infinite;
    }
    .search-animation i:nth-child(3) {
        animation: bounce 1.5s ease-in-out 0.4s infinite;
    }
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    .site-label {
        font-weight: 500;
        width: 120px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

def rank_by_similarity(resume: str, job_list: list):
    
    
    resume_embeddings = model.encode([resume])[0]
    
    
    job_descriptions = [job['job_description'] for job in job_list]
    
    job_embeddings = model.encode(job_descriptions)
    
    similarities = cosine_similarity([resume_embeddings],job_embeddings)[0]
    
    sorted_indices = np.argsort(similarities)[::-1]
    
    ranked_jobs = []
    for idx in sorted_indices:
        job = job_list[idx]
        ranked_jobs.append(job)
    return ranked_jobs

def normalize_value(value):
    """Convert empty or 'Not Specified' values to empty string for display"""
    if not value or value == "Not Specified":
        return ""
    return value

def search_jobs(search_term, location):
    """Search for jobs across all platforms with visual progress indicators"""
    
    # Create a status container for the overall process
    with st.status("Searching for jobs across multiple platforms...", expanded=True) as status:
        
        # Display animated searching indicator
        st.markdown("""
        <div class="search-animation">
            <i></i><i></i><i></i>
        </div>
        """, unsafe_allow_html=True)
        
        # Create progress trackers for each site
        st.write("Scraping progress:")
        
        # Initialize progress containers for each site
        linkedin_progress = st.empty()
        jobsguru_progress = st.empty()
        myjobmag_progress = st.empty()
        hotnigerianjobs_progress = st.empty()
        jobberman_progress = st.empty()
        
        # Initialize results
        linkedln_results = []
        jobsguru_results = []
        myjobmag_results = []
        hotnigerianjobs_results = []
        jobberman_results = []
        
        # LinkedIn scraping
        linkedin_progress.markdown('<div class="scraper-status"><div class="pulse"></div><span class="site-label">LinkedIn:</span> Starting search...</div>', unsafe_allow_html=True)
        try:
            linkedln_results = linkedln(search_term, location)
            linkedin_progress.markdown(f'<div class="scraper-status">✅ <span class="site-label">LinkedIn:</span> Found {len(linkedln_results or [])} jobs</div>', unsafe_allow_html=True)
        except Exception as e:
            linkedin_progress.markdown(f'<div class="scraper-status">❌ <span class="site-label">LinkedIn:</span> Error: {str(e)}</div>', unsafe_allow_html=True)
        
        # JobsGuru scraping
        jobsguru_progress.markdown('<div class="scraper-status"><div class="pulse"></div><span class="site-label">JobsGuru:</span> Starting search...</div>', unsafe_allow_html=True)
        try:
            jobsguru_results = Jobsguru(search_term)
            jobsguru_progress.markdown(f'<div class="scraper-status">✅ <span class="site-label">JobsGuru:</span> Found {len(jobsguru_results or [])} jobs</div>', unsafe_allow_html=True)
        except Exception as e:
            jobsguru_progress.markdown(f'<div class="scraper-status">❌ <span class="site-label">JobsGuru:</span> Error: {str(e)}</div>', unsafe_allow_html=True)
        
        # MyJobMag scraping
        myjobmag_progress.markdown('<div class="scraper-status"><div class="pulse"></div><span class="site-label">MyJobMag:</span> Starting search...</div>', unsafe_allow_html=True)
        try:
            myjobmag_results = MyJobMag(search_term, location)
            myjobmag_progress.markdown(f'<div class="scraper-status">✅ <span class="site-label">MyJobMag:</span> Found {len(myjobmag_results or [])} jobs</div>', unsafe_allow_html=True)
        except Exception as e:
            myjobmag_progress.markdown(f'<div class="scraper-status">❌ <span class="site-label">MyJobMag:</span> Error: {str(e)}</div>', unsafe_allow_html=True)
        
        # HotNigerianJobs scraping
        hotnigerianjobs_progress.markdown('<div class="scraper-status"><div class="pulse"></div><span class="site-label">HotNigerianJobs:</span> Starting search...</div>', unsafe_allow_html=True)
        try:
            hotnigerianjobs_results = hotnigerianjobs(search_term)
            hotnigerianjobs_progress.markdown(f'<div class="scraper-status">✅ <span class="site-label">HotNigerianJobs:</span> Found {len(hotnigerianjobs_results or [])} jobs</div>', unsafe_allow_html=True)
        except Exception as e:
            hotnigerianjobs_progress.markdown(f'<div class="scraper-status">❌ <span class="site-label">HotNigerianJobs:</span> Error: {str(e)}</div>', unsafe_allow_html=True)
        
        # Jobberman scraping
        jobberman_progress.markdown('<div class="scraper-status"><div class="pulse"></div><span class="site-label">Jobberman:</span> Starting search...</div>', unsafe_allow_html=True)
        try:
            jobberman_results = jobberman(search_term, location)
            jobberman_progress.markdown(f'<div class="scraper-status">✅ <span class="site-label">Jobberman:</span> Found {len(jobberman_results or [])} jobs</div>', unsafe_allow_html=True)
        except Exception as e:
            jobberman_progress.markdown(f'<div class="scraper-status">❌ <span class="site-label">Jobberman:</span> Error: {str(e)}</div>', unsafe_allow_html=True)
        
        # Combine all results
        job_list = []
        job_list.extend(linkedln_results or [])
        job_list.extend(jobsguru_results or [])
        job_list.extend(myjobmag_results or [])
        job_list.extend(hotnigerianjobs_results or [])
        job_list.extend(jobberman_results or [])
        
        # Format the job list into a standardized structure
        formatted_jobs = []
        for job in job_list:
            formatted_job = {
                "job_title": normalize_value(job.get('Job Title')),
                "job_location": normalize_value(job.get('Job Location')),
                "job_link": normalize_value(job.get('Job Link')),
                "job_mode": normalize_value(job.get('Job Mode', job.get('Job_Mode'))),
                "job_description": normalize_value(job.get('Job Description')),
                "job_source": normalize_value(job.get('Job Source', job.get('Source')))
            }
            formatted_jobs.append(formatted_job)
        
        # Update status to complete
        time.sleep(0.5)  # Small delay for better UX
        status.update(label="Search completed!", state="complete", expanded=False)
        
        
        formatted_jobs = rank_by_similarity(resume, formatted_jobs)
        
        return {"jobs": formatted_jobs}

def display_job_card(job):
    """Display a job listing as a card with HTML styling"""
    # Start the job card
    html = f"""
    <div class="job-card">
        <div class="job-title">{job["job_title"]}</div>
        <div>
            <span class="job-source">Source: {job["job_source"]}</span>
    """
    
    # Add job mode if available
    if job["job_mode"]:
        html += f'<span class="job-mode">📆 {job["job_mode"]}</span>'
    
    # Close the div and add location if available
    html += "</div>"
    
    if job["job_location"]:
        html += f'<div class="job-meta">📍 {job["job_location"]}</div>'
    
    # Add apply button if link is available
    if job["job_link"]:
        html += f'<a href="{job["job_link"]}" target="_blank" class="apply-btn">Apply Now</a>'
    
   
    
    # Close the job card div
    html += "</div>"
    
    #AI Tailored resume
    resume = st.session_state.resume

        
    
    # Render the complete HTML
    st.markdown(html, unsafe_allow_html=True)

# Back to home button
if st.button("← Back to Home", key="back_to_home"):
    st.switch_page("Home.py")

# App title and description
st.markdown('<div class="main-title"><h1>Job Search</h1><p>Find your dream job by searching multiple Nigerian job portals in one place</p></div>', unsafe_allow_html=True)

# Search form in a container with styling
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 3, 1])

with col1:
    search_term = st.text_input("Job Title or Keywords", placeholder="e.g., Software Engineer, Data Analyst")

with col2:
    location = st.text_input("Location", placeholder="e.g., Lagos, Remote")

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search_button = st.button("🔍 Search")
st.markdown('</div>', unsafe_allow_html=True)

# Search for jobs when button is clicked
if search_button:
    if not search_term:
        st.error("Please enter a job title or keywords.")
    else:
        # Perform the search with visual progress indicators
        results = search_jobs(search_term, location)
        jobs = results["jobs"]
        
        # Display results
        if not jobs:
            st.warning("No jobs found matching your criteria. Try different keywords or location.")
        else:
            st.success(f"Found {len(jobs)} jobs matching your search criteria.")
            
            # Display each job as a card
            for job in jobs:
                display_job_card(job)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>© 2025 Nigerian Job Search Aggregator | Data from LinkedIn, Jobberman, JobsGuru, HotNigerianJobs, and MyJobMag</p>
</div>
""", unsafe_allow_html=True)
