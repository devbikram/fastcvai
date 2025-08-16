#!/usr/bin/env python3
"""
Enhanced test script for CV Analyzer API endpoints with OpenAI integration.
Run this after starting the FastAPI server to test the enhanced functionality.
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_upload_cv():
    """Test CV upload with a more realistic sample CV."""
    print("Testing CV upload...")
    
    # Create a more realistic sample CV
    sample_cv = """
John Doe
Software Developer

Contact Information:
Email: john.doe@email.com
Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe

Professional Summary:
Experienced software developer with 3 years of expertise in Python web development. 
Passionate about creating efficient, scalable applications using modern frameworks.

Experience:
Software Developer | TechCorp Inc. | 2021-2024
- Developed REST APIs using FastAPI and Django
- Built responsive web applications with React
- Collaborated with cross-functional teams on agile projects
- Implemented automated testing with pytest

Junior Developer | StartupXYZ | 2020-2021
- Created web applications using Python and JavaScript
- Worked on database optimization with PostgreSQL
- Participated in code reviews and pair programming

Education:
Bachelor of Science in Computer Science
University of Technology | 2016-2020

Technical Skills:
- Programming Languages: Python, JavaScript, HTML, CSS
- Frameworks: FastAPI, Django, React
- Databases: PostgreSQL, MongoDB
- Tools: Git, Docker, VS Code

Projects:
- E-commerce API: Built a complete REST API for online store
- Task Management App: React-based project management tool
"""
    
    with open("sample_cv.txt", "w") as f:
        f.write(sample_cv)
    
    try:
        with open("sample_cv.txt", "rb") as f:
            files = {"file": ("sample_cv.txt", f, "text/plain")}
            response = requests.post(f"{BASE_URL}/upload-cv", files=files)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Session ID: {data.get('session_id')}")
            print(f"CV Text Preview: {data.get('cv_text')[:200]}...")
            return data.get('session_id')
        else:
            print(f"Error: {response.text}")
    
    finally:
        # Clean up
        if os.path.exists("sample_cv.txt"):
            os.remove("sample_cv.txt")
    
    print("-" * 50)
    return None

def test_enhanced_analyze_cv(session_id):
    """Test enhanced CV analysis with OpenAI."""
    if not session_id:
        print("Skipping CV analysis - no session ID")
        return
    
    print("Testing enhanced CV analysis...")
    
    data = {
        "session_id": session_id,
        "job_title": "Senior Python Developer",
        "job_description": """
        We are seeking a Senior Python Developer with 5+ years of experience to join our team.
        
        Required Skills:
        - Advanced Python programming (5+ years)
        - FastAPI, Django, or Flask experience
        - Cloud platforms (AWS, Azure, or GCP)
        - Database design and optimization
        - Microservices architecture
        - CI/CD pipelines
        - API design and development
        - Test-driven development
        - Agile methodologies
        
        Preferred Skills:
        - Kubernetes and Docker
        - Redis or other caching solutions
        - GraphQL
        - Machine Learning experience
        - Leadership or mentoring experience
        """
    }
    
    response = requests.post(f"{BASE_URL}/analyze-cv", data=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Score: {result.get('original_score')}/100")
        print(f"\nStrengths:")
        for strength in result.get('strengths', []):
            print(f"  • {strength}")
        print(f"\nMissing Skills:")
        for skill in result.get('missing_skills', []):
            print(f"  • {skill}")
        print(f"\nExperience Gaps:")
        for gap in result.get('experience_gaps', []):
            print(f"  • {gap}")
        print(f"\nRecommendations:")
        for rec in result.get('recommendations', []):
            print(f"  • {rec}")
        print(f"\nSummary: {result.get('summary')}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_get_recommendations(session_id):
    """Test getting detailed recommendations."""
    if not session_id:
        print("Skipping recommendations - no session ID")
        return
    
    print("Testing recommendation endpoint...")
    
    response = requests.get(f"{BASE_URL}/get-recommendations/{session_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        suggestions = result.get('improvement_suggestions', {})
        
        print(f"Current Score: {result.get('current_score')}/100")
        print(f"\nEnhanced Summary Suggestion:")
        print(f"  {suggestions.get('enhanced_summary', 'N/A')}")
        
        print(f"\nSkill Addition Tips:")
        for tip in suggestions.get('skill_additions', []):
            print(f"  • {tip}")
            
        print(f"\nKeyword Optimization:")
        for keyword in suggestions.get('keyword_optimization', []):
            print(f"  • {keyword}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_enhanced_cv_generation(session_id):
    """Test enhanced CV generation with additional info."""
    if not session_id:
        print("Skipping CV generation - no session ID")
        return
    
    print("Testing enhanced CV generation...")
    
    additional_info = """
    Additional Skills and Experience:
    
    Cloud Experience:
    - AWS EC2, S3, Lambda (2 years experience)
    - Docker containerization for microservices
    - Basic Kubernetes knowledge
    
    Recent Projects:
    - Led migration of monolithic application to microservices
    - Implemented CI/CD pipeline using GitHub Actions
    - Optimized database queries reducing response time by 40%
    
    Certifications:
    - AWS Certified Developer Associate (2023)
    - Certified Scrum Master (2022)
    
    Leadership Experience:
    - Mentored 2 junior developers
    - Led code review processes
    - Presented technical solutions to stakeholders
    """
    
    data = {
        "session_id": session_id,
        "additional_info": additional_info
    }
    
    response = requests.post(f"{BASE_URL}/add-missing-info", data=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Original Score: {result.get('original_score')}/100")
        print(f"New Score: {result.get('new_score')}/100")
        print(f"Improvement: +{result.get('new_score', 0) - result.get('original_score', 0)} points")
        print(f"Download Link: {result.get('download_link')}")
        
        suggestions = result.get('improvement_suggestions', {})
        if suggestions:
            print(f"\nCV Enhancement Suggestions:")
            print(f"Enhanced Summary: {suggestions.get('enhanced_summary', 'N/A')[:100]}...")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("Enhanced CV Analyzer API Test Script")
    print("=" * 60)
    
    # Test enhanced functionality
    test_health_check()
    session_id = test_upload_cv()
    
    if session_id:
        test_enhanced_analyze_cv(session_id)
        test_get_recommendations(session_id)
        test_enhanced_cv_generation(session_id)
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("Make sure your OPENAI_API_KEY is set in the .env file")
    print("for full OpenAI integration functionality.")
