
# FastAPI backend for CV Analyzer
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from . import utils, openai_utils
from .database import get_db, create_tables
from .crud import CVSessionCRUD

# Load environment variables
load_dotenv()

app = FastAPI(title="CV Analyzer API", version="1.0.0")

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Allow CORS for frontend integration (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze-cv")
async def analyze_cv_complete(
    file: UploadFile = File(...),
    current_job_title: str = Form(...),
    target_job_title: str = Form(""),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Complete CV analysis endpoint that handles upload and analysis in one step.
    
    Supported file formats: PDF, DOCX, TXT, JPG, PNG
    Uses Tesseract OCR for image text extraction.
    """
    try:
        # Step 1: Upload and extract text from CV
        temp_path = utils.save_temp_file(file)
        text, filetype = utils.extract_text(temp_path)
        session_id = os.path.basename(temp_path)
        
        # Step 2: Store in database
        cv_session = CVSessionCRUD.create_session(
            db=db,
            session_id=session_id,
            cv_text=text,
            cv_file_type=filetype,
            cv_file_path=temp_path
        )
        
        # Step 3: Analyze CV with AI
        job_title_to_use = target_job_title if target_job_title.strip() else current_job_title
        analysis_result = openai_utils.analyze_cv(text, job_title_to_use, job_description)
        
        # Unpack the tuple result from analyze_cv function
        (score, missing_skills, summary, strengths, experience_gaps, recommendations) = analysis_result
        
        # Step 4: Update session with analysis results
        cv_session = CVSessionCRUD.update_analysis(
            db=db,
            session_id=session_id,
            job_title=job_title_to_use,
            job_description=job_description,
            original_score=score,
            missing_skills=missing_skills,
            strengths=strengths,
            experience_gaps=experience_gaps,
            recommendations=recommendations,
            summary=summary
        )
        
        # Step 5: Return comprehensive response
        return {
            "success": True,
            "session_id": session_id,
            "analysis": {
                "original_score": score,
                "job_title": job_title_to_use,
                "current_job_title": current_job_title,
                "target_job_title": target_job_title,
                "summary": summary,
                "strengths": strengths,
                "missing_skills": missing_skills,
                "experience_gaps": experience_gaps,
                "recommendations": recommendations
            },
            "extracted_data": {
                "full_text": text,
                "file_type": filetype,
                "file_name": file.filename,
                "text_length": len(text),
                "text_preview": text[:500] + "..." if len(text) > 500 else text
            },
            "cv_info": {
                "file_type": filetype,
                "text_preview": text[:500] + "..." if len(text) > 500 else text
            },
            "next_steps": {
                "can_enhance": True,
                "enhancement_url": f"/add-missing-info",
                "download_url": f"/download-cv/{session_id}",
                "recommendations_url": f"/get-recommendations/{session_id}"
            }
        }
        
    except ValueError as ve:
        # Clean up temp file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        # ValueError usually indicates file format or processing issues
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Health check
@app.get("/")
def read_root():
    return {"message": "CV Analyzer API is running."}
