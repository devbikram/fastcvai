#!/bin/bash

# Test script for CV Analyzer FastAPI Backend
# This script tests the FastAPI backend endpoints

BASE_URL="http://localhost:4000"
API_URL="$BASE_URL/api"

echo "🧪 Testing CV Analyzer FastAPI Backend"
echo "====================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health check (root endpoint)
echo -e "\n${YELLOW}Test 1: Health Check (Root)${NC}"
response=$(curl -s -w "HTTPSTATUS:%{http_code}" "$BASE_URL/")
body=$(echo $response | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
status=$(echo $response | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')

if [ "$status" -eq 200 ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    echo "Response: $body"
else
    echo -e "${RED}✗ Health check failed (Status: $status)${NC}"
fi

# Test 2: CV Analysis (without file)
echo -e "\n${YELLOW}Test 2: CV Analysis (Error Test - No File)${NC}"
response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST "$API_URL/analyze-cv" \
    -F "current_job_title=Software Engineer" \
    -F "job_description=We need a skilled developer")

body=$(echo $response | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
status=$(echo $response | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')

if [ "$status" -eq 422 ]; then
    echo -e "${GREEN}✓ CV analysis validation working (missing file)${NC}"
    echo "Response: $body"
else
    echo -e "${RED}✗ CV analysis validation failed (Status: $status)${NC}"
fi

# Test 3: Create a dummy text file and test upload
echo -e "\n${YELLOW}Test 3: CV Analysis with Text File${NC}"
# Create a temporary dummy CV file
cat > /tmp/dummy-cv.txt << 'EOF'
John Doe
Software Engineer

EXPERIENCE:
- 3 years as Software Developer at TechCorp
- Built web applications using JavaScript and React
- Worked with MySQL databases
- Led a team of 2 junior developers

SKILLS:
- JavaScript, React, HTML, CSS
- Node.js, Express
- MySQL, MongoDB
- Git, GitHub

EDUCATION:
- Bachelor's in Computer Science from State University

ACHIEVEMENTS:
- Improved application performance by 30%
- Successfully delivered 5+ projects on time
EOF

response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST "$API_URL/analyze-cv" \
    -F "file=@/tmp/dummy-cv.txt" \
    -F "current_job_title=Software Developer" \
    -F "target_job_title=Senior Software Engineer" \
    -F "job_description=We are looking for a Senior Software Engineer with experience in Python, React, AWS, Docker, and leadership skills. The ideal candidate should have 5+ years of experience and strong problem-solving abilities.")

body=$(echo $response | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
status=$(echo $response | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')

if [ "$status" -eq 200 ]; then
    echo -e "${GREEN}✓ CV analysis successful${NC}"
    echo "Response: $body" | jq '.' 2>/dev/null || echo "Response: $body"
    
    # Extract session_id for further tests
    session_id=$(echo "$body" | jq -r '.session_id' 2>/dev/null || echo "")
    if [ -n "$session_id" ] && [ "$session_id" != "null" ]; then
        echo -e "${GREEN}Session ID extracted: $session_id${NC}"
    fi
else
    echo -e "${RED}✗ CV analysis failed (Status: $status)${NC}"
    echo "Response: $body"
fi

# Clean up
rm -f /tmp/dummy-cv.txt

# Test 4: Create a dummy PDF for testing (if available)
echo -e "\n${YELLOW}Test 4: Test with Invalid File Type${NC}"
# Create a dummy file with wrong extension
echo "This is not a real PDF" > /tmp/fake.pdf

response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST "$API_URL/analyze-cv" \
    -F "file=@/tmp/fake.pdf" \
    -F "current_job_title=Software Engineer" \
    -F "job_description=Test job description")

body=$(echo $response | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
status=$(echo $response | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')

if [ "$status" -eq 400 ] || [ "$status" -eq 422 ]; then
    echo -e "${GREEN}✓ File validation working${NC}"
    echo "Response: $body"
else
    echo -e "${YELLOW}⚠ File validation may need improvement (Status: $status)${NC}"
    echo "Response: $body"
fi

# Clean up
rm -f /tmp/fake.pdf

# Test 5: Test missing required fields
echo -e "\n${YELLOW}Test 5: Missing Required Fields${NC}"
response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
    -X POST "$API_URL/analyze-cv" \
    -F "current_job_title=Software Engineer")

body=$(echo $response | sed -E 's/HTTPSTATUS\:[0-9]{3}$//')
status=$(echo $response | tr -d '\n' | sed -E 's/.*HTTPSTATUS:([0-9]{3})$/\1/')

if [ "$status" -eq 422 ]; then
    echo -e "${GREEN}✓ Required field validation working${NC}"
    echo "Response: $body"
else
    echo -e "${RED}✗ Required field validation failed (Status: $status)${NC}"
fi

echo -e "\n${YELLOW}====================================="
echo -e "🏁 FastAPI Testing Complete${NC}"
echo -e "\n${YELLOW}Available Endpoints:${NC}"
echo "- GET  $BASE_URL/ (Health check)"
echo "- POST $API_URL/analyze-cv (CV Analysis)"
echo "- Additional endpoints may be available in the FastAPI backend"
