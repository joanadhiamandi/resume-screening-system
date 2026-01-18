# CLD6000 - Weekly Project Log
**Student:** Ioanna Diamanti  
**Project:** AI-Based Resume Screening System  
**Start Date:** October 2025

---

## Week 1 (Oct 6-12, 2025)
**Phase:** Research & Proposal Preparation

### Activities:
- Conducted literature review on NLP for HR automation
- Researched existing resume screening tools (Greenhouse, Workday)
- Identified Kaggle dataset (11,000+ resumes) for testing
- Drafted initial project proposal

### Technical Setup:
- None yet (research phase)

### Challenges:
- Choosing between spaCy vs Sentence Transformers for NLP
- Deciding UI framework: Streamlit vs React

### Hours Logged: 12 hours

---

## Week 2 (Oct 13-19, 2025)
**Phase:** Proposal Finalization & Design

### Activities:
- Finalized research question: "80% overlap with human selection"
- Created system architecture flowchart
- Designed database schema (MySQL)
- Prepared proposal presentation slides

### Technical Setup:
- Installed Python 3.13, MySQL Workbench
- Set up virtual environment

### Deliverables:
-  Project proposal submitted

### Hours Logged: 15 hours

---

## Week 3 (Oct 20-26, 2025)
**Phase:** Environment Setup & Data Exploration

### Activities:
- Set up Python virtual environment
- Installed core libraries: FastAPI, PyPDF2, pandas
- Downloaded Kaggle dataset (AI_Resume_Screening.csv)
- Created MySQL database schema

### Technical Setup:
- Created `database.py` with connection logic
- Built `load_dataset.py` to import Kaggle data

### Challenges:
- MySQL connection issues (fixed with pymysql)
- Kaggle dataset had inconsistent formats

### Hours Logged: 14 hours

---

## Week 4 (Oct 27 - Nov 2, 2025)
**Phase:** Backend Development Begins

### Activities:
- Built FastAPI server (`main.py`)
- Implemented PDF text extraction with PyPDF2
- Created initial `/upload` endpoint for single resume

### Code Progress:
- `main.py` - 150 lines
- `database.py` - 80 lines
- Basic API working on localhost:8000

### Hours Logged: 18 hours

---

## Week 5 (Nov 3-9, 2025)
**Phase:** NLP Implementation

### Activities:
- Researched Sentence Transformers vs spaCy
- Decided on `all-MiniLM-L6-v2` model
- Implemented semantic similarity scoring
- Created fallback keyword matching algorithm

### Technical Achievements:
- AI model loads at server startup
- Cosine similarity calculation working
- Match scores range 0-100%

### Challenges:
- Model loading time (3-4 seconds)
- Memory usage with large model

### Hours Logged: 16 hours

---

## Week 6 (Nov 10-16, 2025)
**Phase:** Database Integration

### Activities:
- Created `save_screening_result()` function
- Built history retrieval endpoint
- Tested data persistence

### Testing:
- Tested with 5 sample PDFs
- Verified scores saved correctly to MySQL

### Hours Logged: 12 hours

---

## Week 7 (Nov 17-23, 2025)
**Phase:** Batch Processing Implementation

### Activities:
- Refactored `/upload` endpoint for multiple files
- Implemented batch processing loop
- Added error handling for invalid PDFs

### Technical Achievements:
- System now processes up to 10 resumes at once
- 3-5 seconds per resume processing time

### Hours Logged: 15 hours

---

## Week 8 (Nov 24-30, 2025)
**Phase:** Frontend Development Begins

### Activities:
- Decided to use React instead of Streamlit (better for portfolio)
- Created React app with `create-react-app`
- Built `UploadForm.js` component
- Implemented drag-and-drop file upload

### Technical Stack:
- React 18, Axios for API calls
- CSS styling with gradients

### Challenges:
- CORS issues (fixed with FastAPI middleware)
- File upload FormData formatting

### Hours Logged: 20 hours

---

## Week 9 (Dec 1-7, 2025)
**Phase:** Results Display Development

### Activities:
- Built `ResultsDisplay.js` component
- Created `ResultsTable.js` for batch results
- Implemented sortable table columns
- Added CSV export functionality

### UI Features:
- Color-coded badges (PASS/REVIEW/FAIL)
- Matched vs missing skills display
- Sortable columns by score, name, etc.

### Hours Logged: 18 hours

---

## Week 10 (Dec 8-14, 2025)
**Phase:** UI/UX Improvements

### Activities:
- Redesigned UI to look like enterprise HR software
- Studied designs from Workday, BambooHR, Smartsheet
- Implemented professional color scheme
- Added animations and transitions

### Design Choices:
- Clean white cards on gray background
- Blue gradient header (#1e40af to #3b82f6)
- Professional typography (Inter font)

### Hours Logged: 16 hours

---

## Week 11 (Dec 15-21, 2025)
**Phase:** Testing & Bug Fixes

### Activities:
- Tested with 20+ different resume PDFs
- Fixed PDF parsing errors
- Improved error messages
- Added loading states

### Issues Found & Fixed:
- Some PDFs couldn't be parsed (added error handling)
- Frontend didn't handle batch results correctly
- Database connection timeouts (added connection pooling)

### Hours Logged: 14 hours

---

## Week 12 (Dec 22-28, 2025)
**Phase:** Holiday Break & Code Cleanup

### Activities:
- Code refactoring and commenting
- Removed unused files
- Updated README documentation
- Prepared GitHub repository

### Hours Logged: 8 hours

---

## Week 13 (Dec 29 - Jan 4, 2026)
**Phase:** Final Testing & Documentation

### Activities:
- Created comprehensive README with setup instructions
- Tested full workflow end-to-end
- Prepared demo screenshots
- Started writing final report

### System Performance:
- Processing speed: ~4 seconds per resume
- AI matching accuracy: 75-85% (needs more testing)
- UI responsive on desktop and mobile

### Hours Logged: 15 hours

---

## Week 14 (Jan 5-11, 2026)
**Phase:** Evaluation & Report Writing

### Activities:
- Analyzing system performance metrics
- Writing methodology section
- Creating evaluation charts
- Comparing AI vs manual screening times

### Preliminary Results:
- Time saved: ~60% vs manual screening
- Need to test "Gold Standard" overlap metric

### Hours Logged: 18 hours

---

## Week 15 (Jan 12-18, 2026)
**Phase:** Final Report & Submission Prep

### Activities:
- Finalizing report document
- Creating presentation slides
- Pushing final code to GitHub
- Preparing demo video

### Hours Logged: 20 hours (ongoing)

---

## Total Hours: ~231 hours
## Status:  Prototype Complete |  Report in Progress
