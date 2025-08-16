"use client";

import { useEffect, useState } from "react";
import CVAnalyzer from "./cv-analyzer";

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading CV Analyzer...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <h1 className="text-3xl font-bold text-gray-900">AI-Powered CV Analyzer</h1>
          <p className="text-gray-600 mt-1">
            Upload your CV and get personalized enhancement recommendations powered by OpenAI
          </p>
        </div>
      </header>

      {/* Main Content */}
      <div className="py-8">
        <CVAnalyzer />
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <p className="text-center text-gray-600">
            © 2025 CV Analyzer. Enhance your career prospects with AI-powered CV analysis.
          </p>
        </div>
      </footer>
    </div>
  );
}
