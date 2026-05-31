import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="font-bold text-lg mb-4">AI Resume Interview System</h3>
            <p className="text-gray-400">
              Empowering job seekers with AI-driven resume analysis and interview preparation.
            </p>
          </div>
          
          <div>
            <h3 className="font-bold text-lg mb-4">Features</h3>
            <ul className="space-y-2 text-gray-400">
              <li>Resume ATS Scoring</li>
              <li>Skill Extraction</li>
              <li>Mock Interviews</li>
              <li>Performance Analytics</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-bold text-lg mb-4">Technology</h3>
            <ul className="space-y-2 text-gray-400">
              <li>Python FastAPI</li>
              <li>React & TailwindCSS</li>
              <li>MongoDB</li>
              <li>spaCy NLP</li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2026 AI Resume Interview System. Built for final year project.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
