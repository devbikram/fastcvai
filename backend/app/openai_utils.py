import openai
import os
import json
from typing import Tuple, Dict, List, Any

def get_openai_client():
    """Get OpenAI client with API key from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return openai.OpenAI(api_key=api_key)

def analyze_cv(cv_text: str, job_title: str, job_desc: str) -> Tuple[int, list, str]:
    """Analyze CV against job description using OpenAI API with enhanced analysis."""
    prompt = f"""
You are an expert HR professional and career advisor. Analyze the following CV against the job requirements and provide a comprehensive assessment.

**CV Content:**
{cv_text}

**Target Position:**
Job Title: {job_title}
Job Description: {job_desc}

Please provide a detailed analysis in JSON format with these exact keys:

1. "score": integer between 0 and 100 (overall match score)
2. "missing_skills": array of specific technical and soft skills that are missing
3. "strengths": array of candidate's key strengths that match the job
4. "experience_gaps": array of experience areas that need improvement
5. "recommendations": array of specific recommendations to improve the CV
6. "summary": comprehensive analysis summary (2-3 sentences)

Consider:
- Technical skills alignment
- Experience level match
- Industry relevance
- Soft skills indicators
- Career progression
- Education relevance
"""
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert HR professional with 15+ years of experience in talent acquisition and career development. Provide detailed, actionable feedback in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1500
        )
        content = response.choices[0].message.content.strip()
        
        # Clean up the response to ensure it's valid JSON
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        result = json.loads(content)
        
        # Ensure all required keys exist
        required_keys = ["score", "missing_skills", "strengths", "experience_gaps", "recommendations", "summary"]
        for key in required_keys:
            if key not in result:
                result[key] = [] if key != "score" and key != "summary" else (50 if key == "score" else "Analysis incomplete")
        
        return (
            result["score"], 
            result["missing_skills"], 
            result["summary"],
            result.get("strengths", []),
            result.get("experience_gaps", []),
            result.get("recommendations", [])
        )
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {content if 'content' in locals() else 'No content'}")
        return (
            50, 
            ["Analysis parsing failed"], 
            "Could not parse AI analysis response",
            ["Please try again"],
            ["Technical issue occurred"],
            ["Contact support if problem persists"]
        )
    except Exception as e:
        # Return default values if OpenAI API fails
        print(f"OpenAI API error: {e}")
        return (
            50, 
            ["Unable to analyze - API error"], 
            f"Analysis failed: {str(e)}",
            [],
            [],
            ["Please check your OpenAI API key and try again"]
        )

def generate_cv_improvement_suggestions(cv_text: str, additional_info: str, missing_skills: List[str]) -> Dict[str, Any]:
    """Generate specific suggestions for CV improvement using OpenAI."""
    prompt = f"""
You are a professional CV writer and career coach. Based on the original CV and additional information provided, generate specific improvement suggestions.

**Original CV:**
{cv_text}

**Additional Information:**
{additional_info}

**Missing Skills Identified:**
{', '.join(missing_skills)}

Please provide improvement suggestions in JSON format with these keys:

1. "enhanced_summary": A professional summary that incorporates the additional information
2. "skill_additions": Specific ways to present the new skills effectively
3. "experience_enhancements": How to better highlight existing experience
4. "formatting_suggestions": CV structure and formatting improvements
5. "keyword_optimization": Industry keywords to include
6. "achievement_focus": How to quantify and highlight achievements better

Focus on making the CV more ATS-friendly and appealing to hiring managers.
"""
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional CV writer with expertise in ATS optimization and modern hiring practices. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        content = response.choices[0].message.content.strip()
        
        # Clean up the response to ensure it's valid JSON
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        return json.loads(content)
    except Exception as e:
        print(f"CV improvement suggestions error: {e}")
        return {
            "enhanced_summary": "Professional with diverse experience and growing skill set.",
            "skill_additions": ["Present new skills with context and examples"],
            "experience_enhancements": ["Quantify achievements with numbers and metrics"],
            "formatting_suggestions": ["Use consistent formatting and clear section headers"],
            "keyword_optimization": ["Include industry-specific keywords from job descriptions"],
            "achievement_focus": ["Highlight impact and results achieved"],
            "error": f"Enhancement failed: {str(e)}"
        }

