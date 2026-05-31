import React, { useState, useEffect } from 'react';
import { interviewService } from '../services/interviewService';
import Loader from '../components/common/Loader';

const MockInterview = () => {
  const [step, setStep] = useState('setup'); // setup, interview, results
  const [roles, setRoles] = useState([]);
  const [selectedRole, setSelectedRole] = useState('');
  const [numTechnical, setNumTechnical] = useState(5);
  const [numHr, setNumHr] = useState(3);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [interviewId, setInterviewId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [results, setResults] = useState(null);

  useEffect(() => {
    loadRoles();
  }, []);

  const loadRoles = async () => {
    try {
      const response = await interviewService.getAvailableRoles();
      setRoles(response.data.roles);
    } catch (err) {
      console.error('Failed to load roles:', err);
    }
  };

  const startInterview = async () => {
    if (!selectedRole) {
      setError('Please select a job role');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await interviewService.startInterview(
        selectedRole,
        numTechnical,
        numHr
      );
      setInterviewId(response.data.interview_id);
      setQuestions(response.data.questions);
      setStep('interview');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start interview');
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      setError('Please provide an answer');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await interviewService.submitAnswer(
        interviewId,
        questions[currentQuestionIndex].question_id,
        answer
      );

      // Move to next question or complete
      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
        setAnswer('');
      } else {
        await completeInterview();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit answer');
    } finally {
      setLoading(false);
    }
  };

  const completeInterview = async () => {
    setLoading(true);
    try {
      const response = await interviewService.completeInterview(interviewId);
      setResults(response.data);
      setStep('results');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to complete interview');
    } finally {
      setLoading(false);
    }
  };

  const resetInterview = () => {
    setStep('setup');
    setSelectedRole('');
    setInterviewId(null);
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setAnswer('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Setup Step */}
        {step === 'setup' && (
          <>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Mock Interview</h1>
            <p className="text-gray-600 mb-8">
              Practice your interview skills with AI-generated questions
            </p>

            <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Select Job Role *
                </label>
                <select
                  value={selectedRole}
                  onChange={(e) => setSelectedRole(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Choose a role...</option>
                  {roles.map((role) => (
                    <option key={role} value={role}>
                      {role}
                    </option>
                  ))}
                </select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Technical Questions
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={numTechnical}
                    onChange={(e) => setNumTechnical(parseInt(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    HR Questions
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={numHr}
                    onChange={(e) => setNumHr(parseInt(e.target.value))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              <button
                onClick={startInterview}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
              >
                {loading ? 'Starting...' : 'Start Interview'}
              </button>
            </div>
          </>
        )}

        {/* Interview Step */}
        {step === 'interview' && questions[currentQuestionIndex] && (
          <>
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <h2 className="text-2xl font-bold text-gray-800">
                  Question {currentQuestionIndex + 1} of {questions.length}
                </h2>
                <span className="text-sm text-gray-600">
                  {questions[currentQuestionIndex].question_type === 'technical' ? 'Technical' : 'HR'}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    {questions[currentQuestionIndex].category}
                  </span>
                  <span className="text-gray-600">
                    Difficulty: <span className="font-medium capitalize">{questions[currentQuestionIndex].difficulty}</span>
                  </span>
                </div>
                
                <h3 className="text-xl font-bold text-gray-800 mb-4">
                  {questions[currentQuestionIndex].question_text}
                </h3>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Your Answer
                </label>
                <textarea
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  rows="8"
                  placeholder="Type your answer here..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                ></textarea>
              </div>

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <p className="text-red-800">{error}</p>
                </div>
              )}

              <button
                onClick={submitAnswer}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
              >
                {loading ? 'Submitting...' : currentQuestionIndex < questions.length - 1 ? 'Next Question' : 'Complete Interview'}
              </button>
            </div>
          </>
        )}

        {/* Results Step */}
        {step === 'results' && results && (
          <>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Interview Results</h1>
            <p className="text-gray-600 mb-8">Here's how you performed</p>

            <div className="space-y-6">
              {/* Overall Performance */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold mb-4">Overall Performance</h2>
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-blue-600">
                      {results.overall_performance?.overall_score?.toFixed(1) || 0}
                    </div>
                    <div className="text-gray-600">Overall Score</div>
                  </div>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-green-600">
                      {results.overall_performance?.technical_score?.toFixed(1) || 0}
                    </div>
                    <div className="text-gray-600">Technical</div>
                  </div>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-purple-600">
                      {results.overall_performance?.hr_score?.toFixed(1) || 0}
                    </div>
                    <div className="text-gray-600">HR</div>
                  </div>
                </div>
                <div className="mt-4 text-center">
                  <span className="text-lg font-medium text-gray-700">
                    Performance Level: <span className="text-blue-600">{results.overall_performance?.performance_level}</span>
                  </span>
                </div>
              </div>

              {/* Recommendations */}
              {results.recommendations?.length > 0 && (
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h2 className="text-2xl font-bold mb-4">Recommendations</h2>
                  <ul className="list-disc list-inside space-y-2">
                    {results.recommendations.map((rec, idx) => (
                      <li key={idx} className="text-gray-700">{rec}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button
                onClick={resetInterview}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
              >
                Start New Interview
              </button>
            </div>
          </>
        )}

        {loading && step === 'interview' && <Loader text="Processing your answer..." />}
      </div>
    </div>
  );
};

export default MockInterview;
