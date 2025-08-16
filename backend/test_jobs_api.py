#!/usr/bin/env python3
"""
Test script for the new jobs listing endpoints.
Demonstrates the /jobs, /jobs/stats, and /jobs/{id}/details endpoints.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def format_json(data):
    """Pretty print JSON data."""
    return json.dumps(data, indent=2, default=str)

def test_jobs_list():
    """Test the jobs listing endpoint with various filters."""
    print("🔍 Testing Jobs List Endpoint")
    print("=" * 50)
    
    # Test basic listing
    print("\n1. Basic jobs list:")
    response = requests.get(f"{BASE_URL}/jobs")
    if response.status_code == 200:
        data = response.json()
        print(f"Total jobs: {data['total_count']}")
        print(f"Returned: {data['returned_count']}")
        print(f"Has more: {data['has_more']}")
        
        for job in data['jobs']:
            print(f"  • {job['session_id']}: {job['job_title']} - Score: {job['original_score']}/100")
            if job['score_improvement']:
                print(f"    Improvement: +{job['score_improvement']} points")
            print(f"    Skills missing: {job['missing_skills_count']}, Strengths: {job['strengths_count']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    # Test filtering
    print("\n2. Filtering by job title:")
    response = requests.get(f"{BASE_URL}/jobs?job_title=Python")
    if response.status_code == 200:
        data = response.json()
        print(f"Python jobs found: {data['returned_count']}")
        
    # Test score filtering
    print("\n3. Filtering by score range:")
    response = requests.get(f"{BASE_URL}/jobs?min_score=50&max_score=70")
    if response.status_code == 200:
        data = response.json()
        print(f"Jobs with score 50-70: {data['returned_count']}")

def test_jobs_stats():
    """Test the jobs statistics endpoint."""
    print("\n📊 Testing Jobs Statistics Endpoint")
    print("=" * 50)
    
    response = requests.get(f"{BASE_URL}/jobs/stats")
    if response.status_code == 200:
        stats = response.json()
        
        print("\nOverview:")
        overview = stats['overview']
        print(f"  Total jobs: {overview['total_jobs']}")
        print(f"  Analyzed jobs: {overview['analyzed_jobs']}")
        print(f"  Enhanced jobs: {overview['enhanced_jobs']}")
        print(f"  Completion rate: {overview['completion_rate']}%")
        
        print("\nScore Analysis:")
        scores = stats['scores']
        print(f"  Average original score: {scores['average_original_score']}")
        print(f"  Average enhanced score: {scores['average_enhanced_score']}")
        print(f"  Average improvement: {scores['average_improvement']}")
        print(f"  Score range: {scores['min_original_score']} - {scores['max_original_score']}")
        
        print("\nFile Types:")
        for file_type, count in stats['file_types'].items():
            print(f"  {file_type}: {count}")
        
        print("\nTop Job Titles:")
        for job_title in stats['top_job_titles']:
            print(f"  {job_title['title']}: {job_title['count']} applications")
        
        print("\nRecent Activity:")
        activity = stats['recent_activity']
        print(f"  Last 7 days: {activity['jobs_last_7_days']} jobs")
        print(f"  Last 30 days: {activity['jobs_last_30_days']} jobs")
        
        print("\nPerformance Metrics:")
        metrics = stats['performance_metrics']
        print(f"  High performing (≥80): {metrics['high_performing_jobs']}")
        print(f"  Low performing (<50): {metrics['low_performing_jobs']}")
        print(f"  Most improved (≥20): {metrics['most_improved_jobs']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_job_details():
    """Test the job details endpoint."""
    print("\n📋 Testing Job Details Endpoint")
    print("=" * 50)
    
    # First get a job ID
    response = requests.get(f"{BASE_URL}/jobs?limit=1")
    if response.status_code != 200:
        print("No jobs found to test details")
        return
    
    jobs = response.json()['jobs']
    if not jobs:
        print("No jobs available for testing")
        return
    
    job_id = jobs[0]['session_id']
    print(f"\nGetting details for job: {job_id}")
    
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/details")
    if response.status_code == 200:
        details = response.json()
        
        print("\nJob Information:")
        job_info = details['job_info']
        print(f"  Session ID: {job_info['session_id']}")
        print(f"  Job Title: {job_info['job_title']}")
        print(f"  File Type: {job_info['file_type']}")
        print(f"  Created: {job_info['created_at']}")
        
        print("\nCV Content:")
        cv_content = details['cv_content']
        print(f"  Text Length: {cv_content['full_text_length']} characters")
        print(f"  Preview: {cv_content['cv_text_preview'][:100]}...")
        
        print("\nAnalysis Results:")
        analysis = details['analysis_results']
        if analysis['is_analyzed']:
            print(f"  Original Score: {analysis['original_score']}/100")
            if analysis['new_score']:
                print(f"  Enhanced Score: {analysis['new_score']}/100")
                print(f"  Improvement: +{analysis['score_improvement']} points")
            if analysis['summary']:
                print(f"  Summary: {analysis['summary'][:100]}...")
        else:
            print("  Status: Not yet analyzed")
        
        print("\nSkills Analysis:")
        skills = details['skills_analysis']
        if skills['missing_skills']:
            print(f"  Missing Skills ({len(skills['missing_skills'])}):")
            for skill in skills['missing_skills'][:3]:
                print(f"    • {skill}")
        if skills['strengths']:
            print(f"  Strengths ({len(skills['strengths'])}):")
            for strength in skills['strengths'][:3]:
                print(f"    • {strength}")
        if not skills['missing_skills'] and not skills['strengths']:
            print("  No skills analysis available yet")
        
        print("\nEnhancement Status:")
        enhancement = details['enhancement']
        print(f"  Has Additional Info: {enhancement['has_additional_info']}")
        print(f"  Has Enhanced CV: {enhancement['has_enhanced_cv']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    print("🚀 CV Analyzer Jobs Endpoint Testing")
    print("=" * 60)
    
    try:
        test_jobs_list()
        test_jobs_stats()
        test_job_details()
        
        print("\n" + "=" * 60)
        print("✅ All endpoint tests completed successfully!")
        print("Try these URLs in your browser:")
        print(f"  • {BASE_URL}/jobs - List all jobs")
        print(f"  • {BASE_URL}/jobs/stats - Job statistics")
        print(f"  • {BASE_URL}/jobs?job_title=Python - Filter by job title")
        print(f"  • {BASE_URL}/docs - API documentation")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure the FastAPI server is running on localhost:8000")
