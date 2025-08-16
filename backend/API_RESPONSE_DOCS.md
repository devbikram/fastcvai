# CV Analyzer API Response Documentation

## POST /api/analyze-cv Response Structure

The API now returns comprehensive extracted data along with the analysis results.

### Response Format

```json
{
  "success": true,
  "session_id": "unique_session_identifier",
  
  "analysis": {
    "original_score": 75,
    "job_title": "Senior Software Engineer",
    "current_job_title": "Software Engineer",
    "target_job_title": "Senior Software Engineer",
    "summary": "Comprehensive analysis summary of the CV match",
    "strengths": [
      "5 years of experience as a Full Stack Developer",
      "Experience leading a team of developers",
      "Strong technical skills in modern frameworks"
    ],
    "missing_skills": [
      "7+ years of experience in full-stack development",
      "Cloud architecture expertise",
      "Advanced DevOps practices"
    ],
    "experience_gaps": [
      "Senior-level project management",
      "Technical leadership at scale"
    ],
    "recommendations": [
      "Gain more experience in cloud architecture",
      "Develop senior-level leadership skills",
      "Obtain cloud platform certifications"
    ]
  },
  
  "extracted_data": {
    "full_text": "Complete extracted text from the CV file...",
    "file_type": "pdf|docx|txt|image",
    "file_name": "uploaded_cv.pdf",
    "text_length": 1234,
    "text_preview": "First 500 characters of the extracted text..."
  },
  
  "cv_info": {
    "file_type": "pdf|docx|txt|image",
    "text_preview": "First 500 characters preview..."
  },
  
  "next_steps": {
    "can_enhance": true,
    "enhancement_url": "/add-missing-info",
    "download_url": "/download-cv/{session_id}",
    "recommendations_url": "/get-recommendations/{session_id}"
  }
}
```

### Field Descriptions

#### extracted_data
- **full_text**: Complete text extracted from the uploaded CV file
- **file_type**: Type of file processed (pdf, docx, txt, image)
- **file_name**: Original filename of the uploaded file
- **text_length**: Total character count of extracted text
- **text_preview**: First 500 characters for quick preview

#### analysis
- **original_score**: AI-calculated match score (0-100)
- **job_title**: Job title used for analysis (target or current)
- **current_job_title**: User's current job title
- **target_job_title**: User's target job title (if provided)
- **summary**: AI-generated analysis summary
- **strengths**: Array of identified candidate strengths
- **missing_skills**: Array of skills/requirements the candidate lacks
- **experience_gaps**: Array of experience areas needing improvement
- **recommendations**: Array of specific improvement suggestions

### File Type Support

| Format | Extension | Extraction Method |
|--------|-----------|-------------------|
| PDF | .pdf | pdfplumber library |
| Word Document | .docx | python-docx library |
| Text File | .txt | Direct file reading |
| Image | .jpg, .jpeg, .png | Tesseract OCR |

### Example Usage

```javascript
// Frontend JavaScript example
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('current_job_title', 'Software Engineer');
formData.append('target_job_title', 'Senior Software Engineer');
formData.append('job_description', 'Job description text...');

fetch('/api/analyze-cv', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Extracted CV Text:', data.extracted_data.full_text);
        console.log('Analysis Score:', data.analysis.original_score);
        console.log('Strengths:', data.analysis.strengths);
        console.log('Missing Skills:', data.analysis.missing_skills);
    }
});
```

### Error Responses

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common error scenarios:
- Unsupported file format
- File processing errors
- AI analysis failures
- Missing required form fields
