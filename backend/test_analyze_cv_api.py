#!/usr/bin/env python3
"""
Test script for the new /api/analyze-cv endpoint
This endpoint handles both upload and analysis in one step.
"""

import requests
import json

def test_analyze_cv_api():
    """Test the complete CV analysis API endpoint."""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing /api/analyze-cv endpoint...")
    print("="*60)
    
    # Create a sample CV content
    sample_cv_content = """
    John Doe
    Software Engineer
    
    Experience:
    - 3 years as Junior Developer at TechCorp
    - Built web applications using Python and JavaScript
    - Worked with databases and API development
    
    Skills:
    - Python, JavaScript, HTML, CSS
    - MySQL, PostgreSQL
    - Git, Linux
    
    Education:
    - Bachelor's in Computer Science
    """
    
    # Test data matching your UI form
    test_data = {
        'current_job_title': 'Software Engineer',
        'target_job_title': 'Senior Software Engineer',
        'job_description': '''
        We are looking for a Senior Software Engineer to join our team.
        
        Requirements:
        - 5+ years of software development experience
        - Proficiency in Python, JavaScript, and modern frameworks
        - Experience with cloud platforms (AWS, Azure)
        - Knowledge of containerization (Docker, Kubernetes)
        - Experience with microservices architecture
        - Strong problem-solving skills
        - Bachelor's degree in Computer Science or related field
        
        Responsibilities:
        - Design and develop scalable software solutions
        - Mentor junior developers
        - Lead technical discussions and architecture decisions
        - Collaborate with cross-functional teams
        '''
    }
    
    # Create a temporary CV file
    cv_filename = "sample_cv.txt"
    with open(cv_filename, "w") as f:
        f.write(sample_cv_content)
    
    try:
        # Test the new API endpoint
        with open(cv_filename, "rb") as cv_file:
            files = {'file': ('sample_cv.txt', cv_file, 'text/plain')}
            
            response = requests.post(
                f"{base_url}/api/analyze-cv",
                files=files,
                data=test_data
            )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ Analysis completed successfully!")
            print("-" * 40)
            
            # Display session info
            print(f"🆔 Session ID: {result['session_id']}")
            
            # Display analysis results
            analysis = result['analysis']
            print(f"\n📊 Analysis Results:")
            print(f"   Original Score: {analysis['original_score']}/100")
            print(f"   Current Job: {analysis['current_job_title']}")
            print(f"   Target Job: {analysis['target_job_title']}")
            print(f"   Summary: {analysis['summary'][:100]}...")
            
            # Display skills analysis
            print(f"\n🎯 Skills Analysis:")
            if analysis['strengths']:
                print(f"   Strengths ({len(analysis['strengths'])}):")
                for strength in analysis['strengths'][:3]:
                    print(f"     • {strength}")
            
            if analysis['missing_skills']:
                print(f"   Missing Skills ({len(analysis['missing_skills'])}):")
                for skill in analysis['missing_skills'][:3]:
                    print(f"     • {skill}")
            
            # Display recommendations
            if analysis['recommendations']:
                print(f"\n💡 Top Recommendations:")
                for i, rec in enumerate(analysis['recommendations'][:2], 1):
                    print(f"   {i}. {rec}")
            
            # Display CV info
            cv_info = result['cv_info']
            print(f"\n📄 CV Information:")
            print(f"   File Type: {cv_info['file_type']}")
            print(f"   Text Preview: {cv_info['text_preview'][:100]}...")
            
            # Display next steps
            next_steps = result['next_steps']
            print(f"\n🔗 Next Steps Available:")
            print(f"   Can Enhance: {next_steps['can_enhance']}")
            print(f"   Enhancement URL: {next_steps['enhancement_url']}")
            print(f"   Download URL: {next_steps['download_url']}")
            
        else:
            print(f"\n❌ Request failed!")
            try:
                error = response.json()
                print(f"Error: {error.get('detail', 'Unknown error')}")
            except:
                print(f"Error: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the FastAPI server is running on http://localhost:8000")
        print("Run: uvicorn app.main:app --reload")
    
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    finally:
        # Clean up test file
        import os
        if os.path.exists(cv_filename):
            os.remove(cv_filename)
    
    # Test image support (new addition)
    print("\n" + "="*60)
    print("🖼️ Testing Image OCR Support...")
    print("="*60)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import tempfile
        
        # Create a test image with CV text
        img = Image.new('RGB', (600, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a system font, fall back to default
        try:
            font = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 16)
        except:
            font = ImageFont.load_default()
        
        # Add CV text to image
        cv_text = "Jane Smith\nData Scientist\n\nExperience:\n• 2 years in Python and Machine Learning\n• Worked with pandas, numpy, sklearn"
        draw.text((20, 20), cv_text, fill='black', font=font)
        
        # Save as temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_img:
            img.save(tmp_img.name, 'PNG')
            img_filename = tmp_img.name
        
        # Test the API with image
        with open(img_filename, "rb") as img_file:
            files = {'file': ('cv_image.png', img_file, 'image/png')}
            test_data_img = {
                'current_job_title': 'Data Scientist',
                'target_job_title': 'Senior Data Scientist',
                'job_description': 'Looking for an experienced data scientist with Python and ML skills.'
            }
            
            response = requests.post(
                f"{base_url}/api/analyze-cv",
                files=files,
                data=test_data_img
            )
        
        print(f"📡 Image Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Image OCR analysis successful!")
            print(f"   File Type: {result['cv_info']['file_type']}")
            print(f"   Extracted Text: {result['cv_info']['text_preview'][:100]}...")
            print(f"   Score: {result['analysis']['original_score']}/100")
        else:
            error = response.json()
            print(f"❌ Image analysis failed: {error.get('detail', 'Unknown error')}")
        
        # Clean up image file
        os.remove(img_filename)
        
    except ImportError:
        print("⚠️ PIL not available for image testing")
    except Exception as e:
        print(f"⚠️ Image test error: {str(e)}")
        if 'img_filename' in locals() and os.path.exists(img_filename):
            os.remove(img_filename)

if __name__ == "__main__":
    test_analyze_cv_api()
