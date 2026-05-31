# AI-Powered Resume Analyzer with Intelligent Mock Interview System

## 🎯 Project Overview

A comprehensive AI-driven platform that helps job seekers by:
1. **Analyzing resumes** with ATS scoring, skill extraction, and improvement suggestions
2. **Conducting mock interviews** with dynamic question generation and intelligent answer evaluation

**Tech Stack**: Python FastAPI + React + MongoDB + spaCy + scikit-learn

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       CLIENT LAYER                          │
│  React Frontend (UI Components, State Management, API)     │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API (HTTP/JSON)
┌────────────────────▼────────────────────────────────────────┐
│                    API GATEWAY LAYER                        │
│           FastAPI (Routing, Validation, Auth)              │
└───────┬──────────────────────────────────────────┬─────────┘
        │                                          │
┌───────▼──────────────────┐          ┌───────────▼──────────┐
│  RESUME ANALYZER MODULE  │          │  INTERVIEW MODULE    │
├──────────────────────────┤          ├──────────────────────┤
│ • PDF/DOCX Parser        │          │ • Question Generator │
│ • Text Extractor         │          │ • Answer Evaluator   │
│ • Entity Recognizer      │          │ • Scoring Engine     │
│ • ATS Scorer (TF-IDF)    │          │ • Feedback Generator │
│ • Skill Clustering       │          │ • NLP Similarity     │
│ • Feedback Generator     │          └──────────────────────┘
└──────────────────────────┘
        │                                          │
        └──────────────┬───────────────────────────┘
                       │
┌──────────────────────▼────────────────────────────────────┐
│                   DATA LAYER                              │
│  MongoDB (Users, Resumes, Interviews, Questions, Jobs)    │
└───────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Modularity**: Each feature is a separate module with clear boundaries
2. **Separation of Concerns**: Business logic, data access, and presentation are separated
3. **Scalability**: Stateless API design allows horizontal scaling
4. **Maintainability**: Clean code with type hints and comprehensive documentation
5. **Testability**: Dependency injection and mock-friendly design

---

## 📁 Project Structure

```
ai-resume-interview-system/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Configuration management
│   │   │
│   │   ├── api/                       # API Routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── resume.py          # Resume endpoints
│   │   │   │   ├── interview.py       # Interview endpoints
│   │   │   │   └── analytics.py       # Analytics endpoints
│   │   │
│   │   ├── core/                      # Core utilities
│   │   │   ├── __init__.py
│   │   │   ├── security.py            # Authentication helpers
│   │   │   ├── logging.py             # Logging configuration
│   │   │   └── exceptions.py          # Custom exceptions
│   │   │
│   │   ├── models/                    # MongoDB models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── interview.py
│   │   │   └── job.py
│   │   │
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── resume.py
│   │   │   ├── interview.py
│   │   │   └── response.py
│   │   │
│   │   ├── services/                  # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── resume_parser.py       # Resume parsing logic
│   │   │   ├── ats_scorer.py          # ATS scoring engine
│   │   │   ├── skill_extractor.py     # Skill identification
│   │   │   ├── question_generator.py  # Interview questions
│   │   │   ├── answer_evaluator.py    # Answer scoring
│   │   │   └── nlp_engine.py          # NLP utilities
│   │   │
│   │   ├── database/                  # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── connection.py          # MongoDB connection
│   │   │   └── repositories/          # Data access layer
│   │   │       ├── __init__.py
│   │   │       ├── resume_repo.py
│   │   │       └── interview_repo.py
│   │   │
│   │   └── utils/                     # Utilities
│   │       ├── __init__.py
│   │       ├── file_handler.py        # File operations
│   │       ├── text_cleaner.py        # Text preprocessing
│   │       └── validators.py          # Input validation
│   │
│   ├── data/                          # Static data
│   │   ├── job_descriptions/          # Sample JDs
│   │   ├── interview_questions/       # Question templates
│   │   └── skills_taxonomy.json       # Skills database
│   │
│   ├── tests/                         # Test suite
│   │   ├── __init__.py
│   │   ├── test_resume_parser.py
│   │   ├── test_ats_scorer.py
│   │   └── test_interview.py
│   │
│   ├── requirements.txt               # Python dependencies
│   └── .env.example                   # Environment template
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── components/                # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   └── Loader.jsx
│   │   │   ├── resume/
│   │   │   │   ├── ResumeUpload.jsx
│   │   │   │   ├── ATSScore.jsx
│   │   │   │   └── Feedback.jsx
│   │   │   └── interview/
│   │   │       ├── RoleSelector.jsx
│   │   │       ├── QuestionPanel.jsx
│   │   │       └── AnswerInput.jsx
│   │   │
│   │   ├── pages/                     # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── ResumeAnalyzer.jsx
│   │   │   ├── MockInterview.jsx
│   │   │   └── Dashboard.jsx
│   │   │
│   │   ├── services/                  # API integration
│   │   │   ├── api.js
│   │   │   ├── resumeService.js
│   │   │   └── interviewService.js
│   │   │
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useResume.js
│   │   │   └── useInterview.js
│   │   │
│   │   ├── utils/                     # Frontend utilities
│   │   │   ├── formatters.js
│   │   │   └── validators.js
│   │   │
│   │   ├── styles/                    # CSS modules
│   │   │   ├── global.css
│   │   │   └── theme.js
│   │   │
│   │   ├── App.jsx                    # Root component
│   │   └── index.js                   # Entry point
│   │
│   ├── package.json
│   └── .env.example
│
├── docker-compose.yml                 # Container orchestration
├── .gitignore
└── ARCHITECTURE.md                    # This file
```

---

## 🔄 Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [x] Project structure setup
- [x] Backend FastAPI skeleton
- [x] MongoDB connection
- [x] Basic file upload handling

### Phase 2: Resume Analyzer (Week 2)
- [x] PDF/DOCX text extraction
- [x] NLP entity recognition (spaCy)
- [x] Skill extraction and clustering
- [x] ATS scoring with TF-IDF
- [x] Feedback generation

### Phase 3: Interview System (Week 3)
- [x] Question bank creation
- [x] Dynamic question generator
- [x] Answer evaluation engine
- [x] Similarity scoring
- [x] Performance analytics

### Phase 4: Frontend (Week 4)
- [x] React component library
- [x] Resume upload interface
- [x] Interview simulation UI
- [x] Results dashboard

### Phase 5: Integration & Testing (Week 5)
- [x] End-to-end testing
- [x] Performance optimization
- [x] Error handling
- [x] Documentation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 5.0+
- 4GB RAM minimum

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
cp .env.example .env
# Edit .env with your MongoDB URI
python -m app.main
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with backend API URL
npm start
```

### Using Docker

```bash
docker-compose up -d
```

---

## 🧪 Testing Strategy

### Backend Testing
```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Testing
```bash
cd frontend
npm test
npm run test:e2e
```

### Test Coverage Goals
- Unit Tests: 80%+
- Integration Tests: 70%+
- E2E Tests: Critical paths

---

## 🔑 Key Design Decisions

### 1. **Why FastAPI over Flask/Django?**
- Async support for concurrent resume processing
- Automatic OpenAPI documentation
- Type validation with Pydantic
- Better performance for ML model serving

### 2. **Why MongoDB over PostgreSQL?**
- Flexible schema for varying resume formats
- Better handling of nested data (skills, experience)
- Easier to scale horizontally
- Natural fit for JSON-heavy API responses

### 3. **Why spaCy over NLTK?**
- Industrial-strength NLP models
- Better entity recognition
- Faster processing
- Pre-trained models for production use

### 4. **TF-IDF for ATS Scoring**
- No external API dependencies
- Proven technique for keyword matching
- Explainable results
- Fast computation

### 5. **Cosine Similarity for Answer Evaluation**
- Captures semantic similarity
- Works offline
- Computationally efficient
- Well-suited for comparing technical answers

---

## 📊 Database Schema Design

### Collections

#### 1. **users**
```json
{
  "_id": "ObjectId",
  "email": "string",
  "name": "string",
  "created_at": "datetime",
  "last_login": "datetime"
}
```

#### 2. **resumes**
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "file_name": "string",
  "upload_date": "datetime",
  "parsed_data": {
    "skills": ["string"],
    "education": [{"degree": "string", "institution": "string", "year": "int"}],
    "experience": [{"title": "string", "company": "string", "duration": "string"}],
    "projects": [{"name": "string", "description": "string"}],
    "certifications": ["string"]
  },
  "ats_score": {
    "overall_score": "float",
    "keyword_match": "float",
    "format_quality": "float",
    "experience_score": "float"
  },
  "feedback": {
    "weak_areas": ["string"],
    "improvements": ["string"],
    "missing_keywords": ["string"],
    "grammar_issues": ["string"],
    "recommended_roles": ["string"]
  }
}
```

#### 3. **interviews**
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "job_role": "string",
  "date": "datetime",
  "questions": [
    {
      "question_id": "string",
      "question_text": "string",
      "category": "string",
      "difficulty": "string",
      "user_answer": "string",
      "expected_keywords": ["string"],
      "score": {
        "correctness": "float",
        "keyword_coverage": "float",
        "similarity": "float"
      },
      "feedback": "string"
    }
  ],
  "overall_performance": {
    "total_score": "float",
    "technical_score": "float",
    "hr_score": "float",
    "communication_score": "float"
  }
}
```

#### 4. **job_descriptions**
```json
{
  "_id": "ObjectId",
  "title": "string",
  "category": "string",
  "required_skills": ["string"],
  "keywords": ["string"],
  "description": "string"
}
```

#### 5. **question_bank**
```json
{
  "_id": "ObjectId",
  "category": "string",
  "job_role": "string",
  "question_type": "string",
  "difficulty": "string",
  "question_text": "string",
  "expected_keywords": ["string"],
  "sample_answer": "string"
}
```

---

## 🔐 Security Considerations

1. **File Upload Security**
   - File size limits (5MB)
   - Extension whitelist (.pdf, .docx)
   - Virus scanning (optional)
   - Temporary file cleanup

2. **Input Validation**
   - Pydantic models for request validation
   - SQL injection prevention (NoSQL)
   - XSS protection

3. **Rate Limiting**
   - API rate limits per user
   - Resume upload throttling

4. **Data Privacy**
   - Resume data encryption at rest
   - User data isolation
   - GDPR-compliant deletion

---

## 🎯 Future Improvements

### Short-term (1-3 months)
- [ ] Real-time interview with speech-to-text
- [ ] LinkedIn profile integration
- [ ] Cover letter generator
- [ ] Email notifications for feedback
- [ ] Mobile responsive design

### Medium-term (3-6 months)
- [ ] Video interview simulation
- [ ] Industry-specific question banks
- [ ] Resume template library
- [ ] Multi-language support
- [ ] Performance analytics dashboard

### Long-term (6-12 months)
- [ ] Fine-tuned transformer models (BERT/RoBERTa)
- [ ] Behavioral interview analysis
- [ ] Company-specific interview prep
- [ ] Peer comparison metrics
- [ ] Career path recommendations
- [ ] Integration with job boards

### Technical Debt
- [ ] Add Redis caching layer
- [ ] Implement message queue (Celery)
- [ ] GraphQL API alternative
- [ ] Microservices architecture
- [ ] Advanced monitoring (Prometheus/Grafana)

---

## 📚 API Documentation

Once running, visit:
- FastAPI Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🤝 Contributing

1. Follow PEP 8 for Python code
2. Use ESLint/Prettier for JavaScript
3. Write tests for new features
4. Update documentation
5. Submit PR with clear description

---

## 📄 License

MIT License - feel free to use for academic or commercial projects

---

## 👨‍💻 Contact & Support

For questions or issues, please open a GitHub issue or contact the development team.
