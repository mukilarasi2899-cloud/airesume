# AI-Powered Resume Analyzer & Mock Interview System

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 5.0+
- 4GB RAM minimum

### Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-resume-interview-system
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_lg

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URI and settings

# Create necessary directories
mkdir uploads logs

# Run the backend
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

#### 4. Database Setup
```bash
# Start MongoDB (if not using Docker)
mongod --dbpath /path/to/data

# Or install MongoDB from: https://www.mongodb.com/try/download/community
```

### Using Docker (Recommended for Production)

```bash
# Build and start all services
docker-compose up --build

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- MongoDB: localhost:27017

## 📚 Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_resume_parser.py

# Run with coverage
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## 🎯 Usage Guide

### 1. Resume Analysis
1. Navigate to "Resume Analyzer" page
2. Select target job role (optional)
3. Upload your resume (PDF or DOCX, max 5MB)
4. View ATS score, extracted skills, and recommendations
5. Download detailed analysis report

### 2. Mock Interview
1. Navigate to "Mock Interview" page
2. Select job role from dropdown
3. Configure number of technical and HR questions
4. Click "Start Interview"
5. Answer each question in the text area
6. Submit answers and view detailed evaluation
7. Review overall performance and recommendations

### 3. Dashboard
1. Navigate to "Dashboard" to view:
   - Recent resume analyses
   - Completed interviews
   - Average scores
   - Performance trends

## 🔧 Configuration

### Backend Environment Variables (.env)
```
MONGODB_URI=mongodb://localhost:27017/ai_resume_interview
UPLOAD_DIR=./uploads
LOG_DIR=./logs
SPACY_MODEL=en_core_web_lg
MAX_UPLOAD_SIZE=5242880
```

### Frontend Environment Variables (.env)
```
VITE_API_URL=http://localhost:8000/api/v1
```

## 🏗️ Architecture Overview

### Backend Structure
```
backend/
├── app/
│   ├── api/v1/          # API routes
│   ├── services/        # Business logic
│   ├── database/        # MongoDB layer
│   ├── schemas/         # Pydantic models
│   ├── core/           # Core utilities
│   └── utils/          # Helper functions
├── tests/              # Test files
├── uploads/            # Uploaded files
└── logs/               # Application logs
```

### Frontend Structure
```
frontend/
├── src/
│   ├── pages/          # Main pages
│   ├── components/     # Reusable components
│   ├── services/       # API integration
│   └── styles/         # CSS files
└── public/             # Static assets
```

## 🛠️ Technology Stack

**Backend:**
- FastAPI 0.109.0 - High-performance web framework
- spaCy 3.7.2 - NLP processing
- scikit-learn 1.4.0 - ML algorithms
- MongoDB + Motor - Async database
- PyPDF2, python-docx - Document processing

**Frontend:**
- React 18.2 - UI framework
- TailwindCSS 3.4 - Styling
- React Router 6.20 - Navigation
- Axios 1.6 - API calls
- Recharts 2.10 - Data visualization

## 📋 API Endpoints

### Resume Endpoints
- `POST /api/v1/resume/upload` - Upload and analyze resume
- `GET /api/v1/resume/{resume_id}` - Get resume details
- `GET /api/v1/resume/user/{user_id}` - Get user resumes
- `DELETE /api/v1/resume/{resume_id}` - Delete resume

### Interview Endpoints
- `POST /api/v1/interview/start` - Start new interview
- `POST /api/v1/interview/{id}/answer` - Submit answer
- `POST /api/v1/interview/{id}/complete` - Complete interview
- `GET /api/v1/interview/{id}` - Get interview details
- `GET /api/v1/interview/user/{user_id}` - Get user interviews
- `GET /api/v1/interview/roles/available` - Get available roles

## 🔍 Features

### Resume Analyzer
✅ PDF and DOCX support
✅ Automatic text extraction
✅ Skills, education, experience parsing
✅ ATS score calculation (TF-IDF + Cosine Similarity)
✅ Missing keyword detection
✅ Improvement recommendations
✅ Job role recommendations
✅ Grammar and formatting analysis

### Mock Interview System
✅ 5 job roles (Software Engineer, Data Scientist, Frontend, DevOps, Full Stack)
✅ 100+ curated questions
✅ Technical + HR questions
✅ Difficulty levels (Easy, Medium, Hard)
✅ Real-time answer evaluation
✅ Keyword coverage analysis
✅ Semantic similarity scoring
✅ Communication quality assessment
✅ STAR method feedback for HR questions
✅ Overall performance grading

## 🚦 Troubleshooting

### Backend Issues
**spaCy model not found:**
```bash
python -m spacy download en_core_web_lg
```

**MongoDB connection error:**
- Check if MongoDB is running: `mongod --version`
- Verify MONGODB_URI in .env file

**Upload errors:**
- Ensure `uploads/` directory exists
- Check file size < 5MB
- Verify file format (PDF or DOCX)

### Frontend Issues
**API connection failed:**
- Check backend is running on port 8000
- Verify VITE_API_URL in .env

**Build errors:**
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📊 Performance Optimization

- Backend uses async/await for non-blocking I/O
- NLPEngine singleton prevents multiple model loads
- TF-IDF vectorization cached for repeated operations
- MongoDB indexes on frequently queried fields
- Frontend lazy loading for code splitting

## 🔐 Security Considerations

- File upload validation (type, size)
- Input sanitization for all user inputs
- CORS configuration for API access
- Environment variables for sensitive data
- MongoDB authentication enabled in production

## 🚀 Deployment

### Production Checklist
- [ ] Set DEBUG=False in backend
- [ ] Use production MongoDB instance
- [ ] Configure proper CORS origins
- [ ] Set up SSL certificates
- [ ] Enable MongoDB authentication
- [ ] Use production-grade WSGI server (gunicorn)
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy

### Deployment Platforms
- **Heroku:** Deploy with Procfile
- **AWS:** EC2 + RDS MongoDB
- **DigitalOcean:** App Platform
- **Docker:** Use docker-compose.yml

## 📝 Future Improvements

1. **User Authentication:** Add login/register with JWT
2. **Interview Recording:** Video interview with webcam
3. **Advanced Analytics:** Performance trends over time
4. **More Job Roles:** Add 10+ additional roles
5. **Resume Builder:** Template-based resume creation
6. **Collaboration:** Share interviews with mentors
7. **Mobile App:** React Native version
8. **AI Improvements:** Fine-tune models on domain data
9. **Multi-language:** Support resumes in multiple languages
10. **Integration:** LinkedIn profile import

## 📄 License

This project was built as a final year academic project for educational purposes.

## 👥 Support

For issues and questions:
1. Check troubleshooting section
2. Review API documentation at /docs
3. Check backend logs in `logs/` directory
4. Review browser console for frontend errors

## 🎓 Academic Project Information

**Project Type:** Final Year Major Project
**Domain:** Artificial Intelligence, NLP, Web Development
**Technologies:** Python, React, MongoDB, spaCy, Machine Learning
**Features:** Resume ATS Scoring, Mock Interview System, Performance Analytics

**Innovation Points:**
- No dependency on paid external APIs
- Offline NLP processing with spaCy
- Custom ATS scoring algorithm
- Intelligent interview question generation
- Multi-component answer evaluation

---

**Built with ❤️ using FastAPI, React, and spaCy**
