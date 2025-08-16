import React, { useState, ChangeEvent, FormEvent, useEffect } from "react";
import dynamic from 'next/dynamic';

// Allowed file types for upload
const ALLOWED_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "image/jpeg",
  "image/png",
];

// Types for the new API response
type AnalysisData = {
  original_score: number;
  job_title: string;
  current_job_title: string;
  target_job_title: string;
  summary: string;
  strengths: string[];
  missing_skills: string[];
  experience_gaps: string[];
  recommendations: string[];
};

type NextSteps = {
  can_enhance: boolean;
  enhancement_url: string;
  download_url: string;
  recommendations_url: string;
};

type ExtractedData = {
  full_text: string;
  file_type: string;
  file_name: string;
  text_length: number;
  text_preview: string;
};

type AnalysisResponse = {
  success: boolean;
  session_id: string;
  analysis: AnalysisData;
  extracted_data: ExtractedData;
  next_steps: NextSteps;
};

function CVAnalyzerComponent() {
  // State for form fields
  const [file, setFile] = useState<File | null>(null);
  const [currentJobTitle, setCurrentJobTitle] = useState<string>("");
  const [targetJobTitle, setTargetJobTitle] = useState<string>("");
  const [jobDescription, setJobDescription] = useState<string>("");
  const [analysisResult, setAnalysisResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  // Handle file selection
  function handleFileChange(e: ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (f && ALLOWED_TYPES.includes(f.type)) {
      setFile(f);
      setError("");
    } else {
      setFile(null);
      setError("Invalid file type. Please upload PDF, DOCX, JPG, or PNG.");
    }
  }

  // Handle initial analysis submit
  async function handleAnalyze(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!file || !currentJobTitle || !jobDescription) {
      setError("Please fill all required fields and upload a file.");
      return;
    }
    
    // Validate inputs
    if (currentJobTitle.trim() === "" || jobDescription.trim() === "") {
      setError("Job title and description cannot be empty.");
      return;
    }
    
    setLoading(true);
    setError("");
    setAnalysisResult(null);
    
    try {
      // Single API call that handles both upload and analysis
      const formData = new FormData();
      formData.append("file", file);
      formData.append("current_job_title", currentJobTitle.trim());
      formData.append("job_description", jobDescription.trim());
      
      // Add target job title if provided
      if (targetJobTitle.trim()) {
        formData.append("target_job_title", targetJobTitle.trim());
      }
      
      console.log("Submitting CV analysis with:", {
        file: file.name,
        current_job_title: currentJobTitle.trim(),
        target_job_title: targetJobTitle.trim() || 'None',
        job_description: jobDescription.slice(0, 100) + '...'
      });
      
      const response = await fetch("http://0.0.0.0:8000/api/analyze-cv", {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error("Analysis failed:", errorText);
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { message: errorText };
        }
        throw new Error(`Failed to analyze CV: ${response.status} ${response.statusText}. ${errorData.detail || errorData.message || ""}`);
      }
      
      const analysisData: AnalysisResponse = await response.json();
      console.log("Analysis response:", analysisData);
      setAnalysisResult(analysisData);
      
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message || "Error analyzing CV.");
      } else {
        setError("Error analyzing CV.");
      }
    } finally {
      setLoading(false);
    }
  }

  // Handle next steps actions
  function handleEnhanceCV() {
    if (analysisResult?.next_steps.enhancement_url) {
      // Navigate to enhancement page or open in new tab
      window.open(analysisResult.next_steps.enhancement_url, "_blank");
    }
  }

  function handleDownloadCV() {
    if (analysisResult?.next_steps.download_url) {
      window.open(analysisResult.next_steps.download_url, "_blank");
    }
  }

  function handleGetRecommendations() {
    if (analysisResult?.next_steps.recommendations_url) {
      window.open(analysisResult.next_steps.recommendations_url, "_blank");
    }
  }

  return (
    <main className="max-w-6xl mx-auto px-6 space-y-8">
      {/* Upload Section */}
      <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <div className="flex items-center mb-4">
          <div className="bg-blue-100 p-2 rounded-full mr-3">
            <span className="text-blue-600 font-bold text-lg">1</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900">Upload Your CV</h2>
        </div>
        <p className="text-gray-600 mb-6">
          Upload your CV and provide job details to get AI-powered analysis and recommendations.
        </p>
        {loading && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-center text-blue-800">
              <svg className="animate-spin h-4 w-4 mr-2" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span className="text-sm font-medium">
                Analyzing your CV with AI...
              </span>
            </div>
          </div>
        )}
        <form onSubmit={handleAnalyze} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              CV File (PDF, DOCX, JPG, PNG)
            </label>
            <input
              type="file"
              accept=".pdf,.docx,.jpg,.jpeg,.png"
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              required
            />
          </div>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Job Title
              </label>
              <input
                type="text"
                placeholder="e.g., Software Engineer"
                value={currentJobTitle}
                onChange={(e) => setCurrentJobTitle(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Job Title (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g., Senior Software Engineer"
                value={targetJobTitle}
                onChange={(e) => setTargetJobTitle(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description
            </label>
            <textarea
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={6}
              required
            />
          </div>
          <button
            type="submit"
            className="w-full md:w-auto bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition-colors"
            disabled={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing with AI...
              </span>
            ) : (
              "Analyze CV with AI"
            )}
          </button>
        </form>
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <svg className="h-5 w-5 text-red-400 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-red-800 text-sm font-medium">{error}</p>
            </div>
          </div>
        )}
      </section>

      {/* Data Extraction Section - Step 2 */}
      {analysisResult && (
        <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <div className="flex items-center mb-6">
            <div className="bg-blue-100 p-2 rounded-full mr-3">
              <span className="text-blue-600 font-bold text-lg">2</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Data Extraction Results</h2>
          </div>
          
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-3">File Information</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">File Name:</span>
                  <span className="font-medium text-gray-800 font-mono text-sm">{analysisResult.extracted_data.file_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">File Type:</span>
                  <span className="font-medium text-gray-800">{analysisResult.extracted_data.file_type.toUpperCase()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Session ID:</span>
                  <span className="font-medium text-gray-800 font-mono text-sm">{analysisResult.session_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Upload Status:</span>
                  <span className="flex items-center text-green-600">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                    </svg>
                    Successfully Processed
                  </span>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg">
              <h3 className="font-semibold text-gray-700 mb-3">Text Extraction Details</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Text Length:</span>
                  <span className="font-medium text-gray-800">{analysisResult.extracted_data.text_length.toLocaleString()} characters</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Preview Length:</span>
                  <span className="font-medium text-gray-800">{analysisResult.extracted_data.text_preview.length.toLocaleString()} characters</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Extraction Status:</span>
                  <span className="flex items-center text-green-600">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                    </svg>
                    Complete
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Job Title Information */}
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg mb-6">
            <h3 className="font-semibold text-gray-700 mb-3">Identified Job Information</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Current Job Title:</span>
                  <span className="font-medium text-gray-800">{analysisResult.analysis.current_job_title}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Target Job Title:</span>
                  <span className="font-medium text-gray-800">{analysisResult.analysis.target_job_title}</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Analysis Status:</span>
                  <span className="flex items-center text-green-600">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                    </svg>
                    Ready for Analysis
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Data Quality:</span>
                  <span className="flex items-center text-blue-600">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" clipRule="evenodd"></path>
                    </svg>
                    {analysisResult.extracted_data.text_length > 100 ? 'High' : analysisResult.extracted_data.text_length > 50 ? 'Medium' : 'Low'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* CV Preview Section */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold text-gray-700 mb-3">Extracted Text Preview</h3>
            <div className="bg-white p-4 rounded border border-gray-200 max-h-64 overflow-y-auto">
              {analysisResult.extracted_data.text_preview && analysisResult.extracted_data.text_preview.trim() ? (
                <pre className="text-sm text-gray-700 whitespace-pre-wrap font-mono">{analysisResult.extracted_data.text_preview}</pre>
              ) : (
                <div className="text-center py-8">
                  <div className="text-gray-400 mb-3">
                    <svg className="w-12 h-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v8a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2H4zm0 2h12v8H4V6z" clipRule="evenodd"></path>
                    </svg>
                  </div>
                  <p className="text-gray-500 font-medium">Text preview not available</p>
                  <p className="text-gray-400 text-sm mt-1">
                    {analysisResult.extracted_data.file_type === 'docx' 
                      ? 'DOCX files may not display text preview. The analysis was still performed successfully.'
                      : 'Text preview could not be extracted from this file.'
                    }
                  </p>
                  <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-blue-700 text-sm">
                      <strong>Note:</strong> Text extraction completed. The analysis will proceed with available data.
                    </p>
                  </div>
                </div>
              )}
            </div>
            {analysisResult.extracted_data.text_preview && analysisResult.extracted_data.text_preview.length > 500 && (
              <div className="mt-3 p-2 bg-blue-50 rounded border border-blue-200">
                <p className="text-blue-700 text-xs text-center">
                  <strong>Note:</strong> This is a preview (first 500 characters). Full text length: {analysisResult.extracted_data.text_length.toLocaleString()} characters
                </p>
              </div>
            )}
          </div>
        </section>
      )}

      {/* Analysis Results Section - Step 3 */}
      {analysisResult && (
        <>
          {/* Score and Overview Section */}
          <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-6">
              <div className="bg-green-100 p-2 rounded-full mr-3">
                <span className="text-green-600 font-bold text-lg">3</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
            </div>
            
            {/* Score and Job Titles */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg text-center">
                <h3 className="font-semibold text-gray-700 mb-2">CV Score</h3>
                <div className="flex items-center justify-center mb-3">
                  <div className="text-4xl font-bold text-blue-600">{analysisResult.analysis.original_score}</div>
                  <div className="text-gray-500 ml-2 text-lg">/ 100</div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div 
                    className="bg-blue-600 h-3 rounded-full transition-all duration-300" 
                    style={{ width: `${analysisResult.analysis.original_score}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg text-center">
                <h3 className="font-semibold text-gray-700 mb-2">Current Role</h3>
                <p className="text-lg font-medium text-green-700">{analysisResult.analysis.current_job_title}</p>
              </div>
              
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg text-center">
                <h3 className="font-semibold text-gray-700 mb-2">Target Role</h3>
                <p className="text-lg font-medium text-purple-700">{analysisResult.analysis.target_job_title}</p>
              </div>
            </div>

            {/* Summary */}
            <div className="bg-gray-50 p-6 rounded-lg mb-6">
              <h3 className="font-semibold text-gray-700 mb-3">Executive Summary</h3>
              <p className="text-gray-700 leading-relaxed">{analysisResult.analysis.summary}</p>
            </div>
          </section>

          {/* Strengths Section */}
          <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="bg-green-100 p-2 rounded-full mr-3">
                <span className="text-green-600 font-bold text-lg">4</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Your Strengths</h2>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {analysisResult.analysis.strengths.map((strength, index) => (
                <div key={index} className="flex items-start p-4 bg-green-50 rounded-lg border border-green-200">
                  <svg className="w-5 h-5 text-green-600 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
                  </svg>
                  <span className="text-gray-700">{strength}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Areas for Improvement */}
          {(analysisResult.analysis.missing_skills.length > 0 || analysisResult.analysis.experience_gaps.length > 0) && (
            <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
              <div className="flex items-center mb-4">
                <div className="bg-yellow-100 p-2 rounded-full mr-3">
                  <span className="text-yellow-600 font-bold text-lg">5</span>
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Areas for Improvement</h2>
              </div>
              
              {/* Missing Skills */}
              {analysisResult.analysis.missing_skills.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-700 mb-3">Missing Skills</h3>
                  <div className="grid md:grid-cols-2 gap-3">
                    {analysisResult.analysis.missing_skills.map((skill, index) => (
                      <div key={index} className="flex items-start p-3 bg-red-50 rounded-lg border border-red-200">
                        <svg className="w-4 h-4 text-red-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
                        </svg>
                        <span className="text-gray-700 text-sm">{skill}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Experience Gaps */}
              {analysisResult.analysis.experience_gaps.length > 0 && (
                <div>
                  <h3 className="font-semibold text-gray-700 mb-3">Experience Gaps</h3>
                  <div className="grid md:grid-cols-2 gap-3">
                    {analysisResult.analysis.experience_gaps.map((gap, index) => (
                      <div key={index} className="flex items-start p-3 bg-orange-50 rounded-lg border border-orange-200">
                        <svg className="w-4 h-4 text-orange-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
                        </svg>
                        <span className="text-gray-700 text-sm">{gap}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </section>
          )}

          {/* Recommendations Section */}
          {analysisResult.analysis.recommendations.length > 0 && (
            <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
              <div className="flex items-center mb-4">
                <div className="bg-blue-100 p-2 rounded-full mr-3">
                  <span className="text-blue-600 font-bold text-lg">6</span>
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Recommendations</h2>
              </div>
              <div className="space-y-4">
                {analysisResult.analysis.recommendations.map((recommendation, index) => (
                  <div key={index} className="flex items-start p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0">
                      {index + 1}
                    </div>
                    <span className="text-gray-700">{recommendation}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Next Steps Section */}
          <section className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center mb-6">
              <div className="bg-purple-100 p-2 rounded-full mr-3">
                <span className="text-purple-600 font-bold text-lg">7</span>
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Next Steps</h2>
            </div>
            
            <div className="grid md:grid-cols-3 gap-6">
              {analysisResult.next_steps.can_enhance && (
                <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-lg border border-green-200">
                  <div className="bg-green-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd"></path>
                    </svg>
                  </div>
                  <h3 className="font-semibold text-gray-700 mb-2">Enhance Your CV</h3>
                  <p className="text-gray-600 text-sm mb-4">Add missing information to improve your score</p>
                  <button
                    onClick={handleEnhanceCV}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                  >
                    Enhance CV
                  </button>
                </div>
              )}

              <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg border border-blue-200">
                <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd"></path>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-700 mb-2">Download CV</h3>
                <p className="text-gray-600 text-sm mb-4">Get your analyzed CV in PDF format</p>
                <button
                  onClick={handleDownloadCV}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                >
                  Download CV
                </button>
              </div>

              <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg border border-purple-200">
                <div className="bg-purple-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"></path>
                  </svg>
                </div>
                <h3 className="font-semibold text-gray-700 mb-2">Get Recommendations</h3>
                <p className="text-gray-600 text-sm mb-4">Receive personalized career advice</p>
                <button
                  onClick={handleGetRecommendations}
                  className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
                >
                  Get Advice
                </button>
              </div>
            </div>
          </section>


        </>
      )}
    </main>
  );
}

// Export with dynamic import to prevent hydration issues
export default dynamic(() => Promise.resolve(CVAnalyzerComponent), {
  ssr: false,
  loading: () => (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading CV Analyzer...</p>
      </div>
    </div>
  ),
});
