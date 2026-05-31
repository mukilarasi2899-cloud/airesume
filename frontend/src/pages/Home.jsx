import React from 'react';
import { Link } from 'react-router-dom';
import { DocumentTextIcon, ChatBubbleLeftRightIcon, ChartBarIcon } from '@heroicons/react/24/outline';

const Home = () => {
  const features = [
    {
      icon: DocumentTextIcon,
      title: 'Resume Analyzer',
      description: 'Get your resume analyzed with AI-powered ATS scoring, skill extraction, and personalized feedback.',
      link: '/resume',
      color: 'bg-blue-500'
    },
    {
      icon: ChatBubbleLeftRightIcon,
      title: 'Mock Interview',
      description: 'Practice interviews with AI-generated questions and receive detailed feedback on your answers.',
      link: '/interview',
      color: 'bg-green-500'
    },
    {
      icon: ChartBarIcon,
      title: 'Dashboard',
      description: 'Track your progress, view past analyses, and monitor your improvement over time.',
      link: '/dashboard',
      color: 'bg-purple-500'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="container mx-auto px-4 py-20">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-6">
              AI-Powered Resume & Interview Platform
            </h1>
            <p className="text-xl mb-8 text-blue-100">
              Enhance your job search with intelligent resume analysis and realistic mock interviews. 
              Get personalized feedback and improve your chances of landing your dream job.
            </p>
            <div className="flex gap-4 justify-center">
              <Link
                to="/resume"
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition"
              >
                Analyze Resume
              </Link>
              <Link
                to="/interview"
                className="bg-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-400 transition border-2 border-white"
              >
                Start Interview
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
          Everything You Need to Succeed
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition">
              <div className={`${feature.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-2 text-gray-800">{feature.title}</h3>
              <p className="text-gray-600 mb-4">{feature.description}</p>
              <Link
                to={feature.link}
                className="text-blue-600 font-semibold hover:text-blue-800 transition"
              >
                Learn more →
              </Link>
            </div>
          ))}
        </div>
      </div>

      {/* Benefits Section */}
      <div className="bg-gray-100 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
            Why Choose Our Platform?
          </h2>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="flex items-start">
              <div className="bg-green-500 rounded-full p-2 mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg mb-2">ATS-Optimized Analysis</h3>
                <p className="text-gray-600">
                  Ensure your resume passes Applicant Tracking Systems with our advanced scoring algorithm.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="bg-green-500 rounded-full p-2 mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg mb-2">Intelligent Feedback</h3>
                <p className="text-gray-600">
                  Receive actionable recommendations to improve your resume and interview skills.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="bg-green-500 rounded-full p-2 mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg mb-2">Role-Specific Questions</h3>
                <p className="text-gray-600">
                  Practice with questions tailored to your target job role and industry.
                </p>
              </div>
            </div>

            <div className="flex items-start">
              <div className="bg-green-500 rounded-full p-2 mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 className="font-bold text-lg mb-2">No API Costs</h3>
                <p className="text-gray-600">
                  Completely free to use with no hidden costs or API charges.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Boost Your Career?</h2>
          <p className="text-xl mb-8 text-indigo-100">
            Start analyzing your resume and practicing interviews today.
          </p>
          <Link
            to="/resume"
            className="bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition inline-block"
          >
            Get Started Free
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home;
