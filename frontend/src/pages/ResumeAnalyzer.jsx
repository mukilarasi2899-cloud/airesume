import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { DocumentTextIcon, CloudArrowUpIcon } from '@heroicons/react/24/outline';
import { resumeService } from '../services/resumeService';
import Loader from '../components/common/Loader';

const ResumeAnalyzer = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [jobRole, setJobRole] = useState('');

  const onDrop = useCallback(async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await resumeService.uploadResume(file, jobRole || null);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze resume');
    } finally {
      setLoading(false);
    }
  }, [jobRole]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 5242880, // 5MB
    multiple: false,
  });

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Resume Analyzer</h1>
        <p className="text-gray-600 mb-8">
          Upload your resume to get AI-powered analysis, ATS scoring, and personalized feedback
        </p>

        {/* Job Role Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Job Role (Optional)
          </label>
          <input
            type="text"
            value={jobRole}
            onChange={(e) => setJobRole(e.target.value)}
            placeholder="e.g., Software Engineer, Data Scientist"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        {/* Upload Area */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
            isDragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400'
          }`}
        >
          <input {...getInputProps()} />
          <CloudArrowUpIcon className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          {isDragActive ? (
            <p className="text-lg text-blue-600">Drop your resume here...</p>
          ) : (
            <div>
              <p className="text-lg text-gray-700 mb-2">
                Drag & drop your resume here, or click to select
              </p>
              <p className="text-sm text-gray-500">
                Supports PDF and DOCX files (max 5MB)
              </p>
            </div>
          )}
        </div>

        {/* Loading */}
        {loading && <Loader text="Analyzing your resume..." />}

        {/* Error */}
        {error && (
          <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="mt-8 space-y-6">
            {/* ATS Score */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">ATS Score</h2>
              <div className="flex items-center justify-between mb-6">
                <div className="text-center">
                  <div className="text-5xl font-bold text-blue-600">
                    {result.ats_score?.overall_score?.toFixed(1) || 0}
                  </div>
                  <div className="text-gray-600">Overall Score</div>
                </div>
                <div className="text-gray-600">
                  {result.ats_score?.score_interpretation || ''}
                </div>
              </div>

              {/* Component Scores */}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {Object.entries(result.ats_score?.component_scores || {}).map(([key, value]) => (
                  <div key={key} className="bg-gray-50 rounded p-3">
                    <div className="text-lg font-bold text-gray-800">{value.toFixed(1)}</div>
                    <div className="text-sm text-gray-600 capitalize">
                      {key.replace(/_/g, ' ')}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Skills */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Extracted Skills</h2>
              <div className="flex flex-wrap gap-2">
                {result.parsed_data?.skills?.all_skills?.slice(0, 20).map((skill, idx) => (
                  <span
                    key={idx}
                    className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Feedback */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Feedback & Recommendations</h2>
              
              {result.ats_score?.analysis?.strengths?.length > 0 && (
                <div className="mb-4">
                  <h3 className="font-bold text-green-700 mb-2">Strengths</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.ats_score.analysis.strengths.map((item, idx) => (
                      <li key={idx} className="text-gray-700">{item}</li>
                    ))}
                  </ul>
                </div>
              )}

              {result.ats_score?.analysis?.recommendations?.length > 0 && (
                <div>
                  <h3 className="font-bold text-blue-700 mb-2">Improvements</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {result.ats_score.analysis.recommendations.map((item, idx) => (
                      <li key={idx} className="text-gray-700">{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Recommended Roles */}
            {result.recommended_roles?.length > 0 && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Recommended Job Roles</h2>
                <div className="space-y-3">
                  {result.recommended_roles.slice(0, 5).map((role, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                      <span className="font-medium">{role.role}</span>
                      <span className="text-blue-600 font-bold">{role.match_score.toFixed(1)}% match</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResumeAnalyzer;
