# AI-Powered-Job-Portal
This is a smart, user-friendly web application that helps job seekers analyze and correct their resumes, match them with scraped job listings, and generate AI-tailored resumes to any of the aforemenstion job descriptions — all in one place.


Built with **Streamlit**, **LLMs (LLaMA-4 via Groq)**, **Sentence Transformers**, **SQLite**, and **Python NLP tools**.

---

## 🚀 Features

- 🔐 **User Authentication**: Register/Login system with secure password hashing
- 📄 **Resume Upload**: Upload `.pdf`, `.docx`, `.txt`, or `.csv` resumes
- 🧠 **Semantic Matching**: Match your resume with job descriptions using vector embeddings and cosine similarity
- 💼 **Job Scraper Integration**: Easily plug in job listings from your own scraping pipeline (JSON or API-ready)
- 🎯 **Tailored Resume Generation**: Generate personalized resumes per job using LLaMA-4 from Groq API
- 📥 **Download Tailored Resumes**: Get your resume customized and ready to download instantly


---

## 📁 Project Structure

├── main.py # Handles login/register, analyzing and correcting resumes and routing
├── auth.py # DB and login logic
├── linkedln.py # Web scraper for Linkedln.com
├── jobberman.py # Web scraper for Jobberman.com
├── myjobmag.py # Web scraper for MyJobMag.com
├── hotnigerianjobs.py # Web scraper for hotnigerianjobs.com
├── jobsguru.py # Web scraper for JobGurus.com
├── Users.db # SQLite DB for users
├── pages/
│ └── Search.py # Search page for job scrapers
└── requirements.txt


## 🛠️ Tech Stack

- 🧠 **LLM**: LLaMA 4 (via Groq API)
- 🔍 **Semantic Search**:SentenceTransformers
- 🔐 **Auth**: Streamlit + SQLite + SHA256
- 🧾 **Parsing**: `pdfplumber`, `docx`, `pandas`
- 💻 **Web UI**: Streamlit (Multi-page with sidebar)

---


🙌 Acknowledgments
Streamlit

Groq
