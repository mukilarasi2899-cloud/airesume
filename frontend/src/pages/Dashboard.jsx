import React, { useState, useEffect } from 'react';
import { DocumentTextIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';
import { resumeService } from '../services/resumeService';
import { interviewService } from '../services/interviewService';
import Loader from '../components/common/Loader';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [resumes, setResumes] = useState([]);
  const [interviews, setInterviews] = useState([]);
  const [userId] = useState('demo-user'); // In production, get from auth

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [resumesData, interviewsData] = await Promise.all([
        resumeService.getUserResumes(userId, 5),
        interviewService.getUserInterviews(userId, 5),
      ]);
      setResumes(resumesData.data.resumes || []);
      setInterviews(interviewsData.data.interviews || []);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loader text="Loading dashboard..." />;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Dashboard</h1>
        <p className="text-gray-600 mb-8">Track your progress and view your history</p>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Recent Resumes */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Recent Resumes</h2>
              <DocumentTextIcon className="w-8 h-8 text-blue-600" />
            </div>

            {resumes.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No resumes analyzed yet</p>
            ) : (
              <div className="space-y-4">
                {resumes.map((resume) => (
                  <div
                    key={resume.resume_id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-800">{resume.file_name}</h3>
                      <span className="text-2xl font-bold text-blue-600">
                        {resume.overall_score?.toFixed(0)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>{resume.job_role || 'General Analysis'}</span>
                      <span>{new Date(resume.upload_date).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Interviews */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-800">Recent Interviews</h2>
              <ChatBubbleLeftRightIcon className="w-8 h-8 text-green-600" />
            </div>

            {interviews.length === 0 ? (
              <p className="text-gray-500 text-center py-8">No interviews completed yet</p>
            ) : (
              <div className="space-y-4">
                {interviews.map((interview) => (
                  <div
                    key={interview.interview_id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-green-300 transition"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-gray-800">{interview.job_role}</h3>
                      <span className="text-2xl font-bold text-green-600">
                        {interview.overall_score?.toFixed(0)}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm text-gray-600">
                      <span className="capitalize">{interview.status}</span>
                      <span>{new Date(interview.date).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Statistics */}
        <div className="mt-8 grid md:grid-cols-4 gap-6">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white">
            <div className="text-3xl font-bold mb-2">{resumes.length}</div>
            <div className="text-blue-100">Resumes Analyzed</div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white">
            <div className="text-3xl font-bold mb-2">{interviews.length}</div>
            <div className="text-green-100">Interviews Completed</div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
            <div className="text-3xl font-bold mb-2">
              {resumes.length > 0
                ? (resumes.reduce((sum, r) => sum + r.overall_score, 0) / resumes.length).toFixed(0)
                : 0}
            </div>
            <div className="text-purple-100">Avg Resume Score</div>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg shadow-lg p-6 text-white">
            <div className="text-3xl font-bold mb-2">
              {interviews.length > 0
                ? (interviews.reduce((sum, i) => sum + (i.overall_score || 0), 0) / interviews.length).toFixed(0)
                : 0}
            </div>
            <div className="text-orange-100">Avg Interview Score</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
