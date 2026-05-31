import React from 'react';
import { Link } from 'react-router-dom';
import { HomeIcon, DocumentTextIcon, ChatBubbleLeftRightIcon, ChartBarIcon } from '@heroicons/react/24/outline';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="bg-blue-600 text-white p-2 rounded-lg">
              <DocumentTextIcon className="w-6 h-6" />
            </div>
            <span className="font-bold text-xl text-gray-800">AI Resume Interview</span>
          </Link>
          
          <div className="flex space-x-6">
            <Link
              to="/"
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition"
            >
              <HomeIcon className="w-5 h-5" />
              <span>Home</span>
            </Link>
            
            <Link
              to="/resume"
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition"
            >
              <DocumentTextIcon className="w-5 h-5" />
              <span>Resume</span>
            </Link>
            
            <Link
              to="/interview"
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition"
            >
              <ChatBubbleLeftRightIcon className="w-5 h-5" />
              <span>Interview</span>
            </Link>
            
            <Link
              to="/dashboard"
              className="flex items-center space-x-1 text-gray-600 hover:text-blue-600 transition"
            >
              <ChartBarIcon className="w-5 h-5" />
              <span>Dashboard</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
