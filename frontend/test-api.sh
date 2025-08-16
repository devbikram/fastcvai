#!/bin/bash

echo "Testing /analyze-cv API endpoint..."
echo ""

# Test with hardcoded values
curl -X POST "http://0.0.0.0:8000/analyze-cv" \
-H "Content-Type: application/json" \
-d '{
  "session_id": "test-session-123",
  "job_title": "Software Engineer",
  "job_description": "Looking for a skilled software engineer with experience in React and Node.js. Must have 5+ years experience."
}' \
-w "\n\nHTTP Status: %{http_code}\n" \
-v

echo ""
echo "Test completed."
