# Testing Strategy

## Overview
Comprehensive testing approach for the AI-Powered Resume Analyzer & Mock Interview System.

## Testing Levels

### 1. Unit Testing

#### Backend Unit Tests
**Location:** `backend/tests/`

**Coverage:**
- ✅ Resume Parser (test_resume_parser.py)
  - Education extraction
  - Skills identification
  - Experience parsing
  - Contact information extraction
  - Project listing
  
- ✅ ATS Scorer (test_ats_scorer.py)
  - Keyword matching algorithm
  - TF-IDF similarity calculation
  - Weighted scoring mechanism
  - Missing keyword identification
  - Improvement suggestion generation
  
- ✅ Interview System (test_interview.py)
  - Question generation
  - Answer evaluation
  - Keyword coverage analysis
  - Semantic similarity scoring
  - HR question evaluation (STAR method)

**Running Tests:**
```bash
cd backend
pytest tests/ -v
pytest tests/test_resume_parser.py --cov=app.services.resume_parser
pytest --cov=app tests/ --cov-report=html
```

#### Frontend Unit Tests
**Location:** `frontend/src/__tests__/`

**Coverage Areas:**
- Component rendering
- User interactions
- Form validation
- API service calls
- State management

**Running Tests:**
```bash
cd frontend
npm test
npm run test:coverage
```

### 2. Integration Testing

#### API Integration Tests
**Test Scenarios:**
- File upload flow (multipart/form-data)
- Resume analysis pipeline (upload → parse → score)
- Interview workflow (start → answer → complete)
- Database operations (CRUD operations)
- Error handling and validation

**Test Setup:**
```python
# backend/tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_resume_upload_flow():
    # Test complete resume upload and analysis
    pass

def test_interview_complete_flow():
    # Test full interview lifecycle
    pass
```

### 3. End-to-End Testing

#### User Journey Tests
1. **Resume Analysis Journey:**
   - User uploads resume
   - System extracts text
   - Parser identifies sections
   - ATS score calculated
   - Results displayed

2. **Interview Journey:**
   - User selects role
   - Questions generated
   - User submits answers
   - Evaluation performed
   - Results shown

**Tools:**
- Selenium for browser automation
- Playwright for modern e2e testing
- Cypress for React component testing

### 4. Performance Testing

#### Load Testing Scenarios
- Concurrent resume uploads (10, 50, 100 users)
- Large file processing (5MB PDFs)
- Multiple interview sessions
- Database query optimization

**Tools:**
- Locust for load testing
- Apache JMeter for stress testing

**Sample Locust Test:**
```python
# backend/tests/load_test.py
from locust import HttpUser, task, between

class ResumeUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def upload_resume(self):
        files = {'file': open('sample_resume.pdf', 'rb')}
        self.client.post('/api/v1/resume/upload', files=files)
```

### 5. Security Testing

#### Security Checklist
- [ ] File upload validation (type, size, content)
- [ ] Input sanitization (XSS prevention)
- [ ] SQL/NoSQL injection protection
- [ ] CORS configuration
- [ ] Environment variable protection
- [ ] API rate limiting
- [ ] Authentication and authorization (if implemented)

**Test Cases:**
```python
def test_file_upload_size_limit():
    # Test files > 5MB are rejected
    pass

def test_invalid_file_types():
    # Test .exe, .sh files are rejected
    pass

def test_xss_prevention():
    # Test malicious input sanitization
    pass
```

## Test Data

### Sample Resume Data
**Location:** `backend/tests/data/`

Files needed:
- `sample_resume_1.pdf` - Well-formatted resume
- `sample_resume_2.docx` - Resume with tables
- `sample_resume_3.pdf` - Resume with poor formatting
- `invalid_file.txt` - For negative testing

### Sample Job Descriptions
```python
# backend/tests/data/job_descriptions.py
SOFTWARE_ENGINEER_JD = """
Looking for Python developer with 3+ years experience...
"""

DATA_SCIENTIST_JD = """
Seeking data scientist with ML expertise...
"""
```

## Test Automation

### CI/CD Pipeline (GitHub Actions)
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mongodb:
        image: mongo:5.0
        ports:
          - 27017:27017
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          python -m spacy download en_core_web_lg
      
      - name: Run backend tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '16'
      
      - name: Install frontend dependencies
        run: |
          cd frontend
          npm install
      
      - name: Run frontend tests
        run: |
          cd frontend
          npm test
```

## Test Coverage Goals

### Target Coverage
- Backend: ≥ 80% code coverage
- Frontend: ≥ 70% code coverage
- Critical paths: 100% coverage
  - File upload and parsing
  - ATS scoring algorithm
  - Answer evaluation logic

### Coverage Reports
```bash
# Backend coverage
cd backend
pytest --cov=app tests/ --cov-report=html
open htmlcov/index.html

# Frontend coverage
cd frontend
npm run test:coverage
open coverage/lcov-report/index.html
```

## Manual Testing Checklist

### Resume Analyzer
- [ ] Upload PDF resume - verify parsing
- [ ] Upload DOCX resume - verify parsing
- [ ] Upload invalid file - verify error
- [ ] Upload file > 5MB - verify rejection
- [ ] Test with resume missing sections
- [ ] Test with resume in poor format
- [ ] Verify ATS score calculation
- [ ] Verify skill extraction accuracy
- [ ] Check improvement recommendations
- [ ] Test job role recommendations

### Mock Interview
- [ ] Select each job role - verify questions
- [ ] Test technical questions generation
- [ ] Test HR questions generation
- [ ] Submit empty answer - verify validation
- [ ] Submit detailed answer - verify evaluation
- [ ] Complete full interview - verify results
- [ ] Check score calculation accuracy
- [ ] Verify feedback quality
- [ ] Test difficulty level filtering

### Dashboard
- [ ] Verify resume list display
- [ ] Verify interview list display
- [ ] Check statistics calculation
- [ ] Test pagination (if > 10 items)
- [ ] Verify date formatting
- [ ] Test responsive design

### Cross-Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome)

### Responsive Design Testing
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

## Bug Tracking

### Bug Report Template
```
**Title:** Brief description

**Severity:** Critical / High / Medium / Low

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: Windows 10
- Browser: Chrome 120
- Backend Version: 1.0.0
- Frontend Version: 1.0.0

**Logs/Screenshots:**
Attach relevant information
```

## Regression Testing

### Test Before Each Release
1. Run full test suite (unit + integration)
2. Verify all endpoints with Postman/Swagger
3. Test critical user journeys
4. Check browser console for errors
5. Verify database operations
6. Test file upload/download
7. Check performance metrics

## Testing Tools & Frameworks

### Backend
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **pytest-asyncio** - Async test support
- **httpx** - Async HTTP client for testing
- **faker** - Generate test data

### Frontend
- **Jest** - Testing framework
- **React Testing Library** - Component testing
- **MSW** (Mock Service Worker) - API mocking
- **Cypress** - E2E testing

### API Testing
- **Postman** - Manual API testing
- **Swagger UI** - Interactive API docs
- **curl** - Command-line testing

## Continuous Improvement

### Metrics to Track
- Test coverage percentage
- Test execution time
- Number of bugs found in testing vs production
- Time to fix bugs
- API response times
- File processing times

### Regular Review
- Weekly: Review failed tests
- Monthly: Analyze coverage gaps
- Quarterly: Update test cases with new features
- Yearly: Comprehensive testing strategy review

---

**Testing Philosophy:** 
"Write tests that give you confidence, not just coverage numbers."

**Priority:** 
Critical business logic > User workflows > Edge cases > Nice-to-have features
