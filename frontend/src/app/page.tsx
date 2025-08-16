'use client';

import { useState } from 'react';
import axios from 'axios';

// Types for our application
interface AnalysisResult {
  originalScore: number;
  missingSkills: string[];
  missingExperience: string[];
  recommendations: string[];
}

interface EnhancedResult {
  newScore: number;
  improvements: string[];
  downloadUrl: string;
  enhancedSections: {
    skills: string[];
    experience: string[];
    achievements: string[];
  };
}

export default function CVAnalyzer() {
  // State management
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [missingInfo, setMissingInfo] = useState({
    skills: '',
    experience: '',
    achievements: ''
  });
  const [enhanced, setEnhanced] = useState<EnhancedResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // File upload handler
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      // Validate file type
      const allowedTypes = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/jpg',
        'image/png'
      ];
      
      if (allowedTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please upload a PDF, DOCX, JPG, or PNG file.');
        setFile(null);
      }
    }
  };

  // CV Analysis submission
  const handleAnalyze = async () => {
    if (!file || !jobTitle || !jobDescription) {
      setError('Please fill all fields and upload a CV file.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('current_job_title', jobTitle);
      formData.append('target_job_title', ''); // Optional field
      formData.append('job_description', jobDescription);

      const response = await axios.post('/api/analyze-cv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        // Map FastAPI response to our frontend format
        const analysis = response.data.analysis;
        setAnalysis({
          originalScore: analysis.original_score,
          missingSkills: analysis.missing_skills || [],
          missingExperience: analysis.experience_gaps || [],
          recommendations: analysis.recommendations || []
        });
      } else {
        setError('Failed to analyze CV');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during analysis');
    } finally {
      setLoading(false);
    }
  };

  // Enhanced CV submission
  const handleEnhance = async () => {
    if (!analysis) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/cv/enhance', {
        missingInfo: {
          skills: missingInfo.skills.split(',').map(s => s.trim()).filter(s => s),
          experience: missingInfo.experience.split(',').map(s => s.trim()).filter(s => s),
          achievements: missingInfo.achievements.split(',').map(s => s.trim()).filter(s => s)
        },
        originalAnalysis: analysis
      });

      if (response.data.success) {
        setEnhanced(response.data.enhanced);
      } else {
        setError('Failed to enhance CV');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'An error occurred during enhancement');
    } finally {
      setLoading(false);
    }
  };

  // Download enhanced CV
  const handleDownload = async () => {
    if (!enhanced?.downloadUrl) return;

    try {
      window.open(enhanced.downloadUrl, '_blank');
    } catch (err) {
      setError('Failed to download enhanced CV');
    }
  };

  // Reset form
  const handleReset = () => {
    setFile(null);
    setJobTitle('');
    setJobDescription('');
    setAnalysis(null);
    setMissingInfo({ skills: '', experience: '', achievements: '' });
    setEnhanced(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            CV Analyzer
          </h1>
          <p className="text-xl text-gray-600">
            Upload your CV and get personalized recommendations to match your target job
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Upload Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            1. Upload Your CV
          </h2>
          
          <div className="space-y-6">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                CV File (PDF, DOCX, JPG, PNG)
              </label>
              <input
                type="file"
                accept=".pdf,.docx,.jpg,.jpeg,.png"
                onChange={handleFileUpload}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              {file && (
                <p className="mt-2 text-sm text-green-600">
                  ✓ {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </p>
              )}
            </div>

            {/* Job Title */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Job Title
              </label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g., Senior Software Engineer"
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Job Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Description
              </label>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                rows={6}
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={loading || !file || !jobTitle || !jobDescription}
              className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Analyze CV'}
            </button>
          </div>
        </div>

        {/* Analysis Results */}
        {analysis && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">
              2. Analysis Results
            </h2>

            {/* Original Score */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-lg font-medium text-gray-700">Original CV Score</span>
                <span className="text-3xl font-bold text-blue-600">{analysis.originalScore}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                  style={{ width: `${analysis.originalScore}%` }}
                ></div>
              </div>
            </div>

            {/* Missing Skills */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Missing Skills</h3>
              <div className="flex flex-wrap gap-2">
                {analysis.missingSkills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Missing Experience */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Missing Experience</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {analysis.missingExperience.map((exp, index) => (
                  <li key={index}>{exp}</li>
                ))}
              </ul>
            </div>

            {/* Recommendations */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Recommendations</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {analysis.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Missing Information Form */}
        {analysis && !enhanced && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">
              3. Fill Missing Information
            </h2>

            <div className="space-y-6">
              {/* Additional Skills */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Skills (comma-separated)
                </label>
                <textarea
                  value={missingInfo.skills}
                  onChange={(e) => setMissingInfo({ ...missingInfo, skills: e.target.value })}
                  placeholder="Python, Machine Learning, AWS, Docker, ..."
                  rows={3}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Additional Experience */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Experience (comma-separated)
                </label>
                <textarea
                  value={missingInfo.experience}
                  onChange={(e) => setMissingInfo({ ...missingInfo, experience: e.target.value })}
                  placeholder="Team leadership, Project management, Cross-functional collaboration, ..."
                  rows={3}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Additional Achievements */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Additional Achievements (comma-separated)
                </label>
                <textarea
                  value={missingInfo.achievements}
                  onChange={(e) => setMissingInfo({ ...missingInfo, achievements: e.target.value })}
                  placeholder="Increased performance by 20%, Led a team of 5 developers, Implemented CI/CD pipeline, ..."
                  rows={3}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              {/* Enhance Button */}
              <button
                onClick={handleEnhance}
                disabled={loading}
                className="w-full bg-green-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Enhancing...' : 'Generate Enhanced CV'}
              </button>
            </div>
          </div>
        )}

        {/* Enhanced Results */}
        {enhanced && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">
              4. Enhanced CV Results
            </h2>

            {/* New Score */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-lg font-medium text-gray-700">Enhanced CV Score</span>
                <span className="text-3xl font-bold text-green-600">{enhanced.newScore}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-green-600 h-3 rounded-full transition-all duration-300"
                  style={{ width: `${enhanced.newScore}%` }}
                ></div>
              </div>
              <p className="text-sm text-green-600 mt-2">
                ↗ Improved by {enhanced.newScore - (analysis?.originalScore || 0)} points!
              </p>
            </div>

            {/* Improvements */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Improvements Made</h3>
              <ul className="list-disc list-inside space-y-1 text-gray-700">
                {enhanced.improvements.map((improvement, index) => (
                  <li key={index}>{improvement}</li>
                ))}
              </ul>
            </div>

            {/* Download Button */}
            <button
              onClick={handleDownload}
              className="w-full bg-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
            >
              📥 Download Enhanced CV (DOCX)
            </button>
          </div>
        )}

        {/* Reset Button */}
        {(analysis || enhanced) && (
          <div className="text-center">
            <button
              onClick={handleReset}
              className="bg-gray-600 text-white py-2 px-6 rounded-lg font-semibold hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Start Over
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
