from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import PyPDF2
import io
from datetime import datetime
from sentence_transformers import SentenceTransformer, util


# Import our database functions
from database import (
    save_screening_result, 
    get_all_screenings,
    get_job_description
)


# Create FastAPI app
app = FastAPI(
    title="Resume Screening System",
    description="AI-powered resume screening with semantic matching",
    version="2.0.0"
)


# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load AI model at startup 
print(" Loading AI model for semantic matching...")
try:
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    print("✅ AI model loaded successfully!")
except Exception as e:
    print(f"⚠️  Warning: Could not load AI model: {e}")
    model = None


# ==================== UTILITY FUNCTIONS ====================


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")


def calculate_ai_match_score(resume_text: str, job_description: str) -> float:
    """
    AI-powered semantic matching using sentence transformers
    Returns a score between 0 and 100
    """
    if model is None:
        # Fallback to simple matching if model not loaded
        print("⚠️  AI model not available, using simple matching")
        return calculate_simple_match_score(resume_text, job_description)
    
    try:
        # Get embeddings 
        resume_embedding = model.encode(resume_text, convert_to_tensor=True)
        job_embedding = model.encode(job_description, convert_to_tensor=True)
        
        # Calculate cosine similarity 
        similarity = util.cos_sim(resume_embedding, job_embedding)
        
        # Convert to percentage score (0-100)
        score = float(similarity.item()) * 100
        
        print(f"🤖 AI Match Score: {score:.2f}%")
        return round(score, 2)
    except Exception as e:
        print(f"⚠️  AI matching error: {e}")
        # Fallback to simple keyword matching
        return calculate_simple_match_score(resume_text, job_description)


def calculate_simple_match_score(resume_text: str, job_description: str) -> float:
    """
    Simple keyword matching algorithm (fallback method)
    Returns a score between 0 and 100
    """
    # Convert to lowercase for comparison
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    # Common tech skills to look for
    skills = [
        'python', 'java', 'javascript', 'react', 'sql', 'mysql',
        'fastapi', 'docker', 'aws', 'git', 'html', 'css',
        'machine learning', 'ai', 'data analysis', 'frontend',
        'backend', 'full stack', 'api', 'database', 'tensorflow',
        'pytorch', 'nlp', 'deep learning', 'cybersecurity', 'networking',
        'linux', 'c++', 'c#', 'php', 'node', 'angular', 'vue'
    ]
    
    # Count how many skills from JD are in resume
    jd_skills = [skill for skill in skills if skill in jd_lower]
    matched_skills = [skill for skill in jd_skills if skill in resume_lower]
    
    # Calculate score
    if len(jd_skills) == 0:
        return 50.0  # No skills to match, return neutral score
    
    score = (len(matched_skills) / len(jd_skills)) * 100
    print(f"📊 Simple Match Score: {score:.2f}%")
    return round(score, 2)


def get_matched_and_missing_skills(resume_text: str, job_description: str):
    """Find which skills matched and which are missing"""
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    skills = [
        'python', 'java', 'javascript', 'react', 'sql', 'mysql',
        'fastapi', 'docker', 'aws', 'git', 'html', 'css',
        'machine learning', 'ai', 'data analysis', 'frontend',
        'backend', 'full stack', 'api', 'database', 'tensorflow',
        'pytorch', 'nlp', 'deep learning', 'cybersecurity', 'networking',
        'linux', 'c++', 'c#', 'php', 'node', 'angular', 'vue'
    ]
    
    jd_skills = [skill for skill in skills if skill in jd_lower]
    matched = [skill for skill in jd_skills if skill in resume_lower]
    missing = [skill for skill in jd_skills if skill not in resume_lower]
    
    return matched, missing


def get_recommendation(score: float) -> str:
    """Determine recommendation based on score"""
    if score >= 80:
        return "PASS"
    elif score >= 60:
        return "REVIEW"
    else:
        return "FAIL"


# ==================== API ENDPOINTS ====================


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Resume Screening System API",
        "status": "running",
        "ai_model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/v1/screening/upload")
async def upload_resume(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    """
    Upload and screen one or multiple resumes against a job description
    
    - **files**: One or more PDF resume files (max 10)
    - **job_description**: The job description text to match against
    """
    
    # Validate file count
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed at once")
    
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    print(f"\n📦 Batch processing {len(files)} resume(s)...")
    
    # Process all resumes
    results = []
    
    for uploaded_file in files:
        # Validate file type
        if not uploaded_file.filename.endswith('.pdf'):
            results.append({
                "file_name": uploaded_file.filename,
                "candidate_name": "Error",
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "recommendation": "ERROR",
                "error": "Only PDF files are supported",
                "ai_powered": False
            })
            print(f"❌ Skipped {uploaded_file.filename}: Not a PDF")
            continue
        
        try:
            # Read file content
            file_content = await uploaded_file.read()
            
            # Extract text from PDF
            resume_text = extract_text_from_pdf(file_content)
            
            if not resume_text.strip():
                results.append({
                    "file_name": uploaded_file.filename,
                    "candidate_name": "Error",
                    "match_score": 0,
                    "matched_skills": [],
                    "missing_skills": [],
                    "recommendation": "ERROR",
                    "error": "Could not extract text from PDF",
                    "ai_powered": False
                })
                print(f"❌ Failed {uploaded_file.filename}: No text extracted")
                continue
            
            print(f"📄 Processing: {uploaded_file.filename}")
            
            # Calculate match score using AI
            match_score = calculate_ai_match_score(resume_text, job_description)
            
            # Get matched and missing skills
            matched_skills, missing_skills = get_matched_and_missing_skills(
                resume_text, 
                job_description
            )
            
            # Get recommendation
            recommendation = get_recommendation(match_score)
            
            # Extract candidate name 
            candidate_name = resume_text.split('\n')[0][:100].strip() if resume_text else "Unknown"
            
            # Save to database
            result_id = save_screening_result(
                job_id=1,
                candidate_name=candidate_name,
                file_name=uploaded_file.filename,
                match_score=match_score,
                matched_skills=", ".join(matched_skills) if matched_skills else "None",
                missing_skills=", ".join(missing_skills) if missing_skills else "None",
                recommendation=recommendation
            )
            
            # Add to results
            results.append({
                "id": result_id,
                "candidate_name": candidate_name,
                "file_name": uploaded_file.filename,
                "match_score": match_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "recommendation": recommendation,
                "ai_powered": model is not None
            })
            
            print(f"✅ {uploaded_file.filename}: {match_score}% - {recommendation}")
            
        except Exception as e:
            print(f"❌ Error processing {uploaded_file.filename}: {str(e)}")
            results.append({
                "file_name": uploaded_file.filename,
                "candidate_name": "Error",
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "recommendation": "ERROR",
                "error": str(e),
                "ai_powered": False
            })
    
    print(f"✅ Batch processing complete! {len(results)} resume(s) processed.\n")
    
    # Return batch results
    return {
        "total_processed": len(results),
        "results": results,
        "message": f"Successfully processed {len(results)} resume(s)!"
    }


@app.get("/api/v1/screening/history")
async def get_screening_history():
    """Get all past screening results"""
    screenings = get_all_screenings()
    return {
        "total": len(screenings),
        "screenings": screenings
    }


@app.get("/api/v1/screening/{screening_id}")
async def get_screening_by_id(screening_id: int):
    """Get a specific screening result by ID"""
    screenings = get_all_screenings()
    screening = next((s for s in screenings if s['id'] == screening_id), None)
    
    if not screening:
        raise HTTPException(status_code=404, detail="Screening result not found")
    
    return screening


# ==================== RUN SERVER ====================


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Resume Screening System API...")
    print("📝 API Documentation: http://127.0.0.1:8000/docs")
    print("🔗 API Root: http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
