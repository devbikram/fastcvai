# CV Analyzer FastAPI Backend

A streamlined FastAPI backend service for analyzing CVs against job descriptions using AI with persistent SQLite database storage.

## Features

1. **One-Step Analysis**: Upload CV file and get complete AI analysis in a single API call
2. **Multi-Format Support**: Supports PDF, DOCX, TXT, JPG, and PNG files
3. **OCR Technology**: Automatic text extraction from images using Tesseract OCR
4. **AI-Powered Analysis**: Uses OpenAI GPT-4o-mini for comprehensive CV evaluation
5. **Persistent Storage**: SQLite database stores all analysis sessions and results
6. **RESTful API**: Clean, documented endpoint with CORS support
7. **Comprehensive Results**: Detailed scoring, skills analysis, and improvement recommendations

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Initialize database**:
   ```bash
   python db_manager.py create
   ```

4. **Tesseract OCR is already installed** (for image text extraction):
   - ✅ Tesseract 5.5.1 detected and working
   - Image files (JPG, PNG) are fully supported

5. **Run the server**:
   
   **Option A: Using VS Code Task**
   - Open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
   - Run: "Tasks: Run Task"
   - Select: "Start CV Analyzer API"
   
   **Option B: Using Terminal**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Core Functionality
- `POST /api/analyze-cv` - **Complete CV analysis** (upload file + analyze against job description in one step)
- `GET /` - Health check endpoint

That's it! Simple and focused.

## Data Storage

All CV analysis sessions are automatically stored in SQLite database (`cv_analyzer.db`) with:
- Complete CV text and file information
- Job requirements and analysis results
- AI-generated scores, skills gaps, and recommendations
- Session timestamps for tracking

## Database Management

Optional database management using the `db_manager.py` script:

```bash
# View database statistics
python db_manager.py stats

# List all sessions
python db_manager.py list

# Reset database (WARNING: Deletes all data)
python db_manager.py reset
```

## Usage Workflow

**Simple One-Step Process:**
1. **POST** to `/api/analyze-cv` with CV file and job details
2. **Receive** comprehensive analysis with scores, skills gaps, and recommendations
3. **Use** the session_id for future reference if needed

**That's it!** No multi-step process, no complex workflow - just one API call.

### API Endpoint Details

#### `POST /api/analyze-cv`
**Description**: Complete CV analysis in one step - upload CV file and get AI analysis results.

**Form Parameters**:
- `file` (file, required): CV file in PDF, DOCX, TXT, JPG, or PNG format
- `current_job_title` (string, required): Current job title (e.g., "Software Engineer")
- `target_job_title` (string, optional): Target job title (e.g., "Senior Software Engineer")
- `job_description` (string, required): Full job description text

**Response**:
```json
**Response**:
```json
{
  "success": true,
  "session_id": "unique_session_id",
  "analysis": {
    "original_score": 75,
    "job_title": "Senior Software Engineer",
    "current_job_title": "Software Engineer",
    "target_job_title": "Senior Software Engineer", 
    "summary": "Analysis summary...",
    "strengths": ["List of strengths"],
    "missing_skills": ["Skills to improve"],
    "experience_gaps": ["Experience gaps"],
    "recommendations": ["Action items"]
  },
  "extracted_data": {
    "full_text": "Complete extracted CV text...",
    "file_type": "pdf",
    "file_name": "uploaded_cv.pdf",
    "text_length": 1234,
    "text_preview": "First 500 characters of CV text..."
  },
  "cv_info": {
    "file_type": "pdf",
    "text_preview": "CV content preview..."
  },
  "next_steps": {
    "can_enhance": true,
    "enhancement_url": "/add-missing-info",
    "download_url": "/download-cv/{session_id}"
  }
}
```
```

## Data Persistence

- All CV sessions are stored in SQLite database (`cv_analyzer.db`)
- Original uploaded files are preserved in temporary storage
- Full analysis history and results are maintained
- Session IDs allow future reference to analysis results

## Environment Variables

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./cv_analyzer.db
```

Visit http://127.0.0.1:8000/docs for interactive API documentation.

## Testing the API

Use the included test scripts to verify functionality:

```bash
# Test basic CV upload, analysis, and enhancement
python test_api.py

# Test job listing, filtering, and statistics
python test_jobs_api.py
```

The test scripts demonstrate the complete workflow and validate all endpoints.
