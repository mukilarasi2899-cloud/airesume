// Mock Interview JavaScript
let interviewState = {
    role: '',
    questions: [],
    currentIndex: 0,
    answers: [],
    startTime: null,
    questionStartTime: null
};

// Voice Recognition Variables
let recognition = null;
let isRecording = false;
let speechSynthesis = window.speechSynthesis;

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Update the answer textarea with transcribed text
        const currentAnswer = document.getElementById('answerInput').value;
        if (finalTranscript) {
            document.getElementById('answerInput').value = currentAnswer + finalTranscript;
        }
        
        // Show interim results in status
        if (interimTranscript) {
            document.getElementById('recordingStatus').textContent = 'Listening: ' + interimTranscript;
        }
    };
    
    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        document.getElementById('recordingStatus').textContent = 'Error: ' + event.error;
        stopRecording();
    };
    
    recognition.onend = function() {
        if (isRecording) {
            recognition.start(); // Restart if still recording
        }
    };
}

const questionBank = {
    software_engineer: [
        {
            question: "Explain the difference between var, let, and const in JavaScript.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["scope", "hoisting", "reassignment", "block"]
        },
        {
            question: "What is the time complexity of common sorting algorithms?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["O(n log n)", "quicksort", "mergesort", "bubble sort", "O(n²)"]
        },
        {
            question: "How would you design a scalable microservices architecture?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["distributed", "API gateway", "load balancing", "database", "communication"]
        },
        {
            question: "Describe your experience working in an Agile team.",
            difficulty: "Easy",
            category: "Behavioral",
            expectedKeywords: ["sprint", "standup", "collaboration", "team", "project"]
        },
        {
            question: "Tell me about a challenging bug you fixed and how you approached it.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["debugging", "problem-solving", "approach", "solution", "testing"]
        }
    ],
    data_scientist: [
        {
            question: "Explain the difference between supervised and unsupervised learning.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["labeled", "unlabeled", "classification", "clustering", "training"]
        },
        {
            question: "How do you handle imbalanced datasets?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["oversample", "undersample", "SMOTE", "weighted", "metrics"]
        },
        {
            question: "Explain the mathematics behind gradient descent.",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["derivative", "optimization", "learning rate", "convergence", "local minimum"]
        },
        {
            question: "How do you communicate complex data insights to non-technical stakeholders?",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["visualization", "simple", "story", "impact", "understand"]
        },
        {
            question: "Describe a data science project from start to finish.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["data collection", "preprocessing", "model", "evaluation", "deployment"]
        }
    ],
    frontend_developer: [
        {
            question: "What are React hooks and why are they useful?",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["useState", "useEffect", "functional", "state", "lifecycle"]
        },
        {
            question: "Explain the CSS box model.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["content", "padding", "border", "margin", "width"]
        },
        {
            question: "How do you optimize website performance?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["lazy loading", "minification", "caching", "CDN", "images"]
        },
        {
            question: "How do you ensure cross-browser compatibility?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["testing", "polyfills", "CSS prefixes", "browsers", "standards"]
        },
        {
            question: "Describe your approach to responsive web design.",
            difficulty: "Easy",
            category: "Behavioral",
            expectedKeywords: ["mobile-first", "breakpoints", "flexible", "media queries", "grid"]
        }
    ],
    devops_engineer: [
        {
            question: "Explain the benefits of containerization with Docker.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["isolation", "portability", "consistency", "lightweight", "images"]
        },
        {
            question: "What is the difference between continuous integration and continuous deployment?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["CI", "CD", "automated", "testing", "production", "pipeline"]
        },
        {
            question: "How would you set up monitoring and alerting for a production system?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["metrics", "logs", "Prometheus", "Grafana", "alerts", "threshold"]
        },
        {
            question: "Describe your experience with infrastructure as code.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["Terraform", "CloudFormation", "automation", "version control", "reproducible"]
        },
        {
            question: "How do you handle incidents and outages?",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["response", "communication", "root cause", "postmortem", "prevention"]
        }
    ],
    full_stack_developer: [
        {
            question: "Explain REST API design principles.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["HTTP", "endpoints", "GET", "POST", "stateless", "resources"]
        },
        {
            question: "How do you secure a web application?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["authentication", "authorization", "XSS", "CSRF", "encryption", "HTTPS"]
        },
        {
            question: "What database would you choose for different use cases and why?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["SQL", "NoSQL", "relational", "document", "scalability", "ACID"]
        },
        {
            question: "How do you approach debugging issues across the full stack?",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["logs", "network", "database", "frontend", "backend", "systematic"]
        },
        {
            question: "Describe a full-stack project you've built.",
            difficulty: "Easy",
            category: "Behavioral",
            expectedKeywords: ["frontend", "backend", "database", "deployment", "features"]
        }
    ],
    cybersecurity_analyst: [
        {
            question: "What is the difference between symmetric and asymmetric encryption?",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["symmetric", "asymmetric", "public key", "private key", "performance", "use cases"]
        },
        {
            question: "Explain the OWASP Top 10 vulnerabilities.",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["injection", "authentication", "XSS", "broken access", "misconfiguration", "sensitive data"]
        },
        {
            question: "How would you respond to a security incident?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["incident response", "containment", "investigation", "recovery", "documentation", "post-mortem"]
        },
        {
            question: "Describe your experience with penetration testing.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["methodology", "tools", "vulnerabilities", "report", "remediation"]
        },
        {
            question: "How do you stay updated with the latest security threats?",
            difficulty: "Easy",
            category: "Behavioral",
            expectedKeywords: ["research", "certifications", "conferences", "communities", "CVE", "threat intelligence"]
        }
    ],
    cloud_engineer: [
        {
            question: "Explain the difference between IaaS, PaaS, and SaaS.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["infrastructure", "platform", "software", "service", "responsibility", "examples"]
        },
        {
            question: "How do you ensure high availability in cloud architecture?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["redundancy", "load balancing", "auto-scaling", "multi-region", "disaster recovery"]
        },
        {
            question: "What is Infrastructure as Code and why is it important?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["IaC", "Terraform", "CloudFormation", "version control", "reproducibility", "automation"]
        },
        {
            question: "How do you optimize cloud costs?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["right-sizing", "reserved instances", "spot instances", "monitoring", "tagging", "storage"]
        },
        {
            question: "Describe a cloud migration project you've worked on.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["assessment", "planning", "strategy", "migration", "testing", "challenges"]
        }
    ],
    data_engineer: [
        {
            question: "What is the difference between batch and stream processing?",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["batch", "stream", "real-time", "latency", "use cases", "tools"]
        },
        {
            question: "Explain ETL vs ELT pipelines.",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["extract", "transform", "load", "data warehouse", "processing", "performance"]
        },
        {
            question: "How do you handle data quality issues?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["validation", "cleaning", "monitoring", "quality checks", "data profiling"]
        },
        {
            question: "What experience do you have with big data technologies?",
            difficulty: "Hard",
            category: "Behavioral",
            expectedKeywords: ["Hadoop", "Spark", "Kafka", "distributed", "scalability", "projects"]
        },
        {
            question: "How do you design scalable data pipelines?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["architecture", "orchestration", "fault tolerance", "monitoring", "optimization"]
        }
    ],
    mobile_developer: [
        {
            question: "What's the difference between native and cross-platform development?",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["native", "cross-platform", "performance", "code reuse", "frameworks"]
        },
        {
            question: "How do you handle different screen sizes in mobile apps?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["responsive", "adaptive", "layouts", "constraints", "testing"]
        },
        {
            question: "Explain the mobile app lifecycle.",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["lifecycle", "states", "background", "foreground", "memory", "save state"]
        },
        {
            question: "How do you optimize mobile app performance?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["performance", "memory", "battery", "network", "caching", "profiling"]
        },
        {
            question: "Describe a challenging mobile app feature you've implemented.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["feature", "challenge", "approach", "solution", "testing", "user experience"]
        }
    ],
    network_engineer: [
        {
            question: "Explain the OSI model and its layers.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["OSI", "layers", "physical", "data link", "network", "transport", "application"]
        },
        {
            question: "What is the difference between TCP and UDP?",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["TCP", "UDP", "connection", "reliability", "speed", "use cases"]
        },
        {
            question: "How do you troubleshoot network connectivity issues?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["ping", "traceroute", "DNS", "routing", "firewall", "methodology"]
        },
        {
            question: "Explain BGP and its role in internet routing.",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["BGP", "routing", "autonomous system", "path selection", "internet backbone"]
        },
        {
            question: "Describe your experience with network security.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["firewall", "VPN", "segmentation", "monitoring", "policies", "incidents"]
        }
    ],
    qa_engineer: [
        {
            question: "What is the difference between unit, integration, and E2E testing?",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["unit", "integration", "end-to-end", "scope", "isolation", "automation"]
        },
        {
            question: "How do you write effective test cases?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["test cases", "requirements", "coverage", "edge cases", "documentation"]
        },
        {
            question: "Explain your approach to test automation.",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["automation", "framework", "tools", "maintenance", "ROI", "strategy"]
        },
        {
            question: "How do you handle flaky tests?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["flaky", "intermittent", "root cause", "stability", "reliability"]
        },
        {
            question: "Tell me about a critical bug you found and how you reported it.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["bug", "testing", "reproduction", "reporting", "severity", "communication"]
        }
    ],
    blockchain_developer: [
        {
            question: "Explain how blockchain ensures data immutability.",
            difficulty: "Easy",
            category: "Technical",
            expectedKeywords: ["blockchain", "immutability", "hash", "chain", "consensus", "cryptography"]
        },
        {
            question: "What are smart contracts and how do they work?",
            difficulty: "Medium",
            category: "Technical",
            expectedKeywords: ["smart contracts", "Ethereum", "Solidity", "execution", "conditions", "blockchain"]
        },
        {
            question: "Explain different consensus mechanisms.",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["consensus", "proof of work", "proof of stake", "Byzantine", "mining"]
        },
        {
            question: "How do you ensure security in smart contracts?",
            difficulty: "Hard",
            category: "Technical",
            expectedKeywords: ["security", "vulnerabilities", "auditing", "testing", "best practices", "reentrancy"]
        },
        {
            question: "Describe a blockchain project you've worked on.",
            difficulty: "Medium",
            category: "Behavioral",
            expectedKeywords: ["project", "blockchain", "implementation", "challenges", "outcomes"]
        }
    ]
};

function startInterview() {
    const role = document.getElementById('jobRole').value;
    const count = parseInt(document.getElementById('questionCount').value);
    
    // Get random questions
    const availableQuestions = questionBank[role];
    interviewState.role = role;
    interviewState.questions = shuffleArray(availableQuestions).slice(0, count);
    interviewState.currentIndex = 0;
    interviewState.answers = [];
    interviewState.startTime = Date.now();
    
    // Update UI
    document.getElementById('setupSection').classList.add('hidden');
    document.getElementById('interviewSection').classList.remove('hidden');
    
    // Show first question
    displayQuestion();
    startTimer();
}

function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

function displayQuestion() {
    const question = interviewState.questions[interviewState.currentIndex];
    
    document.getElementById('currentQuestion').textContent = interviewState.currentIndex + 1;
    document.getElementById('totalQuestions').textContent = interviewState.questions.length;
    document.getElementById('questionText').textContent = question.question;
    document.getElementById('difficulty').textContent = question.difficulty;
    document.getElementById('difficulty').style.background = 
        question.difficulty === 'Easy' ? 'var(--secondary-color)' :
        question.difficulty === 'Medium' ? 'var(--warning-color)' :
        'var(--danger-color)';
    
    document.getElementById('answerInput').value = '';
    
    // Reset recording state
    if (isRecording) {
        stopRecording();
    }
    document.getElementById('recordingStatus').textContent = '';
    
    // Update progress
    const progress = ((interviewState.currentIndex + 1) / interviewState.questions.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    
    interviewState.questionStartTime = Date.now();
    
    // Auto-speak question (optional - can be removed if too intrusive)
    // setTimeout(() => speakQuestion(), 500);
}

// Text-to-Speech: Speak the question
function speakQuestion() {
    // Stop any ongoing speech
    speechSynthesis.cancel();
    
    const question = interviewState.questions[interviewState.currentIndex];
    const utterance = new SpeechSynthesisUtterance(question.question);
    
    // Configure voice settings
    utterance.rate = 0.9; // Slightly slower for clarity
    utterance.pitch = 1;
    utterance.volume = 1;
    
    // Use a clear voice if available
    const voices = speechSynthesis.getVoices();
    const englishVoice = voices.find(voice => voice.lang.startsWith('en-')) || voices[0];
    if (englishVoice) {
        utterance.voice = englishVoice;
    }
    
    utterance.onstart = function() {
        document.getElementById('recordingStatus').textContent = '🔊 Speaking question...';
    };
    
    utterance.onend = function() {
        document.getElementById('recordingStatus').textContent = '✓ Question spoken. Ready to record your answer!';
        setTimeout(() => {
            document.getElementById('recordingStatus').textContent = '';
        }, 2000);
    };
    
    speechSynthesis.speak(utterance);
}

// Start Voice Recording
function startRecording() {
    if (!recognition) {
        alert('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
        return;
    }
    
    try {
        isRecording = true;
        recognition.start();
        
        // Update UI
        document.getElementById('startRecordBtn').classList.add('hidden');
        document.getElementById('stopRecordBtn').classList.remove('hidden');
        document.getElementById('recordingIndicator').classList.remove('hidden');
        document.getElementById('recordingStatus').textContent = 'Listening... Speak your answer';
        
        // Focus on textarea so user can see transcription
        document.getElementById('answerInput').focus();
    } catch (error) {
        console.error('Error starting recording:', error);
        alert('Could not start recording. Please check microphone permissions.');
        stopRecording();
    }
}

// Stop Voice Recording
function stopRecording() {
    if (recognition && isRecording) {
        isRecording = false;
        recognition.stop();
        
        // Update UI
        document.getElementById('startRecordBtn').classList.remove('hidden');
        document.getElementById('stopRecordBtn').classList.add('hidden');
        document.getElementById('recordingIndicator').classList.add('hidden');
        document.getElementById('recordingStatus').textContent = '✓ Recording stopped. Review your answer below.';
        
        setTimeout(() => {
            document.getElementById('recordingStatus').textContent = '';
        }, 3000);
    }
}

function startTimer() {
    setInterval(() => {
        const elapsed = Date.now() - interviewState.startTime;
        const minutes = Math.floor(elapsed / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        document.getElementById('timer').textContent = 
            `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function submitAnswer() {
    // Stop recording if active
    if (isRecording) {
        stopRecording();
    }
    
    const answer = document.getElementById('answerInput').value.trim();
    
    if (!answer) {
        alert('Please provide an answer before submitting.');
        return;
    }
    
    const question = interviewState.questions[interviewState.currentIndex];
    const timeSpent = Math.floor((Date.now() - interviewState.questionStartTime) / 1000);
    
    // Evaluate answer
    const evaluation = evaluateAnswer(answer, question);
    
    interviewState.answers.push({
        question: question.question,
        answer,
        timeSpent,
        evaluation,
        category: question.category,
        difficulty: question.difficulty
    });
    
    // Move to next question or finish
    if (interviewState.currentIndex < interviewState.questions.length - 1) {
        interviewState.currentIndex++;
        displayQuestion();
    } else {
        finishInterview();
    }
}

function skipQuestion() {
    // Stop recording if active
    if (isRecording) {
        stopRecording();
    }
    
    const question = interviewState.questions[interviewState.currentIndex];
    
    interviewState.answers.push({
        question: question.question,
        answer: '',
        timeSpent: 0,
        evaluation: { score: 0, feedback: 'Question skipped' },
        category: question.category,
        difficulty: question.difficulty
    });
    
    if (interviewState.currentIndex < interviewState.questions.length - 1) {
        interviewState.currentIndex++;
        displayQuestion();
    } else {
        finishInterview();
    }
}

function evaluateAnswer(answer, question) {
    let score = 0;
    const feedback = [];
    
    // Keyword coverage (40%)
    const keywords = question.expectedKeywords;
    const matchedKeywords = keywords.filter(kw => 
        answer.toLowerCase().includes(kw.toLowerCase())
    );
    const keywordScore = (matchedKeywords.length / keywords.length) * 40;
    score += keywordScore;
    
    if (matchedKeywords.length > 0) {
        feedback.push(`✓ Mentioned key concepts: ${matchedKeywords.join(', ')}`);
    }
    
    // Length and detail (20%)
    const wordCount = answer.split(/\s+/).length;
    let lengthScore = 0;
    if (wordCount > 100) lengthScore = 20;
    else if (wordCount > 50) lengthScore = 15;
    else if (wordCount > 20) lengthScore = 10;
    score += lengthScore;
    
    if (wordCount < 20) {
        feedback.push('⚠ Answer is too brief. Provide more detail.');
    }
    
    // Structure (20%)
    const sentences = answer.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const structureScore = Math.min((sentences.length / 3) * 20, 20);
    score += structureScore;
    
    // Technical depth (20%)
    const technicalWords = ['architecture', 'performance', 'optimization', 'scalability', 'implementation'];
    const hasTechnical = technicalWords.some(word => answer.toLowerCase().includes(word));
    const technicalScore = hasTechnical ? 20 : 10;
    score += technicalScore;
    
    // Grade
    let grade;
    if (score >= 90) grade = 'A+';
    else if (score >= 80) grade = 'A';
    else if (score >= 70) grade = 'B';
    else if (score >= 60) grade = 'C';
    else grade = 'D';
    
    return {
        score: Math.round(score),
        grade,
        feedback: feedback.join('\n'),
        matchedKeywords,
        missingKeywords: keywords.filter(kw => !matchedKeywords.includes(kw))
    };
}

function finishInterview() {
    // Calculate overall performance
    const totalDuration = Math.floor((Date.now() - interviewState.startTime) / 1000);
    const overallScore = Math.round(
        interviewState.answers.reduce((sum, a) => sum + a.evaluation.score, 0) / 
        interviewState.answers.length
    );
    
    const technicalAnswers = interviewState.answers.filter(a => a.category === 'Technical');
    const technicalScore = technicalAnswers.length > 0 ? Math.round(
        technicalAnswers.reduce((sum, a) => sum + a.evaluation.score, 0) / technicalAnswers.length
    ) : 0;
    
    const behavioralAnswers = interviewState.answers.filter(a => a.category === 'Behavioral');
    const communicationScore = behavioralAnswers.length > 0 ? Math.round(
        behavioralAnswers.reduce((sum, a) => sum + a.evaluation.score, 0) / behavioralAnswers.length
    ) : 0;
    
    // Save to history
    saveInterviewToHistory({
        role: interviewState.role,
        overallScore,
        technicalScore,
        communicationScore,
        questionsCount: interviewState.questions.length,
        duration: totalDuration,
        timestamp: Date.now()
    });
    
    // Display results
    document.getElementById('interviewSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');
    
    document.getElementById('overallScore').textContent = overallScore;
    document.getElementById('technicalScore').textContent = technicalScore;
    document.getElementById('communicationScore').textContent = communicationScore;
    
    // Detailed feedback
    const feedbackHTML = interviewState.answers.map((a, i) => `
        <div style="background: var(--light-gray); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                <h4>Question ${i + 1}</h4>
                <span class="skill-tag" style="background: ${a.evaluation.score >= 70 ? 'var(--secondary-color)' : 'var(--warning-color)'}">
                    ${a.evaluation.score}% (${a.evaluation.grade})
                </span>
            </div>
            <p style="margin-bottom: 1rem;"><strong>${a.question}</strong></p>
            ${a.answer ? `
                <p style="color: var(--gray); margin-bottom: 1rem;">${a.answer.substring(0, 200)}${a.answer.length > 200 ? '...' : ''}</p>
                <div style="background: white; padding: 1rem; border-radius: 4px;">
                    <p style="margin-bottom: 0.5rem;"><strong>Feedback:</strong></p>
                    <p style="white-space: pre-line;">${a.evaluation.feedback}</p>
                    ${a.evaluation.missingKeywords.length > 0 ? `
                        <p style="margin-top: 0.5rem; color: var(--warning-color);">
                            <i class="fas fa-exclamation-circle"></i> Consider mentioning: ${a.evaluation.missingKeywords.join(', ')}
                        </p>
                    ` : ''}
                </div>
            ` : '<p style="color: var(--danger-color);"><i class="fas fa-times"></i> Question skipped</p>'}
        </div>
    `).join('');
    document.getElementById('detailedFeedback').innerHTML = feedbackHTML;
    
    // Recommendations
    const recommendations = generateInterviewRecommendations(interviewState.answers, overallScore);
    document.getElementById('interviewRecommendations').innerHTML = recommendations;
}

function generateInterviewRecommendations(answers, overallScore) {
    const recommendations = [];
    
    if (overallScore < 70) {
        recommendations.push('Practice answering common interview questions for your role');
    }
    
    const skippedCount = answers.filter(a => !a.answer).length;
    if (skippedCount > 0) {
        recommendations.push(`You skipped ${skippedCount} question(s). Try to answer all questions even if uncertain`);
    }
    
    const lowScoreAnswers = answers.filter(a => a.evaluation.score < 60);
    if (lowScoreAnswers.length > 0) {
        recommendations.push('Provide more detailed and structured answers with specific examples');
    }
    
    const avgLength = answers.filter(a => a.answer).reduce((sum, a) => 
        sum + a.answer.split(/\s+/).length, 0) / answers.length;
    if (avgLength < 30) {
        recommendations.push('Expand your answers with more details and examples');
    }
    
    recommendations.push('Review technical concepts related to ' + interviewState.role.replace('_', ' '));
    recommendations.push('Practice the STAR method (Situation, Task, Action, Result) for behavioral questions');
    
    return recommendations.map(rec => `
        <div style="background: #dbeafe; padding: 1rem; border-left: 4px solid var(--primary-color); margin-bottom: 1rem; border-radius: 4px;">
            <i class="fas fa-lightbulb" style="color: var(--primary-color);"></i> ${rec}
        </div>
    `).join('');
}

function saveInterviewToHistory(data) {
    const history = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
    history.unshift(data);
    
    // Keep only last 10
    if (history.length > 10) history.pop();
    
    localStorage.setItem('interviewHistory', JSON.stringify(history));
}
