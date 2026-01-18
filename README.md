# AI-Based Resume Screening Syste

An intelligent AI-powered resume screening system that leverages Natural Language Processing (NLP) and semantic matching to automate and accelerate the candidate shortlisting process for HR departments.

##  Table of Contents

- [Problem Statement](#problem-statement)
- [Research Question](#research-question)
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Installation](#installation)
- [Author](#author)

---

##  Problem Statement

HR departments spend **excessive time** manually screening resumes, often processing hundreds of applications per job posting. This manual process is:
- **Time-consuming**: 10+ minutes per resume
- **Inconsistent**: Subject to human bias and fatigue
- **Inefficient**: Limits the number of candidates that can be evaluated
- **Costly**: Diverts HR resources from strategic activities

---

## Research Question

> **"Can an AI resume screener reduce candidate shortlisting time by 99% while maintaining selection quality above 80% accuracy?"**

### Research Objectives:
1. Develop an NLP-based semantic matching system for resume screening
2. Measure time efficiency gains vs. traditional manual screening
3. Evaluate system accuracy against human HR decisions
4. Validate the system using a large-scale dataset (1,000+ resumes)

---

##  Project Overview

This system uses **advanced NLP techniques** to automatically screen resumes against job descriptions, providing:
- **Semantic Matching**: Understanding context and meaning, not just keywords
- **Automated Scoring**: AI-generated compatibility scores (0-100%)
- **Skill Analysis**: Extraction and matching of technical and soft skills
- **Batch Processing**: Screen multiple resumes simultaneously
- **Interactive Dashboard**: Professional React-based user interface

### Key Innovation:
Unlike traditional Applicant Tracking Systems (ATS) that rely on exact keyword matching, this system uses **Sentence Transformers** for semantic similarity, capturing conceptual relationships between job requirements and candidate qualifications.

---

##  Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **FastAPI**: High-performance REST API framework
- **Sentence Transformers**: Semantic text embedding (`all-MiniLM-L6-v2`)
- **PyPDF2**: PDF text extraction
- **spaCy**: Advanced NLP preprocessing
- **scikit-learn**: Machine learning utilities

### Frontend
- **React 18**: Modern UI framework
- **Axios**: HTTP client for API communication
- **CSS3**: Custom styling and responsive design

### Database
- **MySQL 8.0**: Relational database for persistent storage
- **SQLAlchemy**: Python ORM for database operations

### Data & Evaluation
- **Kaggle Resume Dataset**: 11,000+ resumes for training/testing
- **Pandas & NumPy**: Data manipulation and analysis

---

---

##  Features

### Core Functionality
-  **Semantic Resume Matching**: Advanced NLP using transformer models
-  **Batch Processing**: Upload multiple resumes (PDF format)
-  **Real-time Scoring**: Instant compatibility scores (0-100%)
-  **Skill Analysis**: Automatic extraction and matching of skills
-  **Database Integration**: Persistent storage of all screening results
-  **Export Functionality**: Download results as CSV
-  **Sorting & Filtering**: Interactive results table

### AI/NLP Capabilities
- **Text Similarity**: Cosine similarity between embeddings
- **Keyword Extraction**: Identification of technical and soft skills
- **Context Understanding**: Semantic relatedness (not just keyword matching)
- **Preprocessing**: Tokenization, lemmatization, stopword removal

### User Experience
- **Responsive Design**: Works on desktop and tablet devices
- **Drag-and-Drop Upload**: Intuitive file upload interface
- **Visual Feedback**: Loading states and error handling
- **Detailed Results**: Matched skills, missing skills, and overall score

---

##  Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16+ and npm
- MySQL 8.0 or higher
- Git

###  Clone the Repository

git clone https://github.com/joanadhiamandi/resume-screening-system.git
cd ai-resume-screening

---

### Create and Activate Virtual Environment
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

---

### Install Python Dependencies

pip install -r requirements.txt

### Download spaCy Language Model
bash
python -m spacy download en_core_web_sm

### Frontend Setup
bash
cd ../frontend
npm install

### Usage
Starting the Backend Server
bash
cd backend

### Activate virtual environment (if not already active)
 Windows:
venv\Scripts\activate
 macOS/Linux:
source venv/bin/activate

### Start FastAPI server
python main.py
Backend will run on: http://localhost:8000

API Documentation: http://localhost:8000/docs

### Starting the Frontend
Open a new terminal:

bash
cd frontend
npm start
Frontend will run on: http://localhost:3000

Using the Application
Enter Job Description

Paste the job description text in the provided field

Add required skills (comma-separated)

Upload Resumes

Click "Choose Files" or drag and drop PDF files

Upload single or multiple resumes (batch processing supported)

Start Screening

Click "Screen Resumes" button

AI processes each resume (~4 seconds per resume)

Review Results

View candidate rankings sorted by compatibility score

Review matched skills (green) and missing skills (red)

Sort by score, name, or skills

Export results as CSV for further analysis

----
### Author
Ioanna Diamanti

Student: Computing, University of Greater Manchester

Institution: New York College Athens

Course: CLD6000 - Contemporary Problem Analysis

