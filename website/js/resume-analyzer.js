// Resume Analyzer JavaScript
let resumeData = null;

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file) handleFile(file);
    });
    
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) handleFile(file);
    });
});

function handleFile(file) {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    
    if (!validTypes.includes(file.type)) {
        alert('Please upload a PDF, DOCX, or TXT file');
        return;
    }
    
    document.getElementById('fileName').textContent = `Selected: ${file.name}`;
    
    // Show loading
    document.getElementById('uploadSection').classList.add('hidden');
    document.getElementById('loadingSection').classList.remove('hidden');
    
    // Read file
    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        analyzeResume(text, file.name);
    };
    reader.readAsText(file);
}

function analyzeResume(text, filename) {
    // Simulate processing time
    setTimeout(() => {
        resumeData = processResume(text);
        displayResults(resumeData);
        saveToHistory(resumeData, filename);
        
        // Hide loading, show results
        document.getElementById('loadingSection').classList.add('hidden');
        document.getElementById('resultsSection').classList.remove('hidden');
    }, 2000);
}

function processResume(text) {
    // Extract information from resume text
    const skills = extractSkills(text);
    const contact = extractContact(text);
    const experience = extractExperience(text);
    const education = extractEducation(text);
    
    // Calculate ATS score
    const atsScore = calculateATSScore(text, skills, experience, education);
    
    return {
        text,
        skills,
        contact,
        experience,
        education,
        atsScore,
        timestamp: new Date().toISOString()
    };
}

function extractSkills(text) {
    const skillsBank = [
        // Programming Languages
        'JavaScript', 'Python', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust', 'Swift',
        'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell', 'Bash', 'PowerShell',
        
        // Cybersecurity
        'Penetration Testing', 'Ethical Hacking', 'Security Analysis', 'Vulnerability Assessment',
        'SIEM', 'Splunk', 'Wireshark', 'Metasploit', 'Burp Suite', 'Nmap', 'Kali Linux',
        'Security Operations', 'Incident Response', 'Threat Intelligence', 'Malware Analysis',
        'Firewall', 'IDS', 'IPS', 'WAF', 'Cryptography', 'PKI', 'SSL/TLS', 'VPN',
        'ISO 27001', 'NIST', 'GDPR', 'HIPAA', 'PCI DSS', 'SOC 2', 'Risk Assessment',
        'Security Auditing', 'CISSP', 'CEH', 'CompTIA Security+', 'OSCP', 'Network Security',
        'Application Security', 'Cloud Security', 'Endpoint Security', 'Zero Trust',
        
        // Web Development
        'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot',
        'ASP.NET', 'Laravel', 'Ruby on Rails', 'Next.js', 'Nuxt.js', 'HTML', 'CSS',
        'SASS', 'LESS', 'Tailwind CSS', 'Bootstrap', 'Material UI', 'jQuery', 'Webpack',
        'Vite', 'REST API', 'GraphQL', 'WebSockets', 'OAuth', 'JWT', 'Redux', 'MobX',
        
        // Mobile Development
        'React Native', 'Flutter', 'iOS', 'Android', 'Xamarin', 'Ionic', 'SwiftUI',
        
        // Cloud & DevOps
        'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
        'Ansible', 'Chef', 'Puppet', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'CircleCI',
        'CI/CD', 'CloudFormation', 'ECS', 'EKS', 'Lambda', 'EC2', 'S3', 'CloudWatch',
        'Prometheus', 'Grafana', 'Nagios', 'ELK Stack', 'Datadog', 'New Relic',
        
        // Databases
        'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Cassandra', 'DynamoDB',
        'Oracle', 'SQL Server', 'MariaDB', 'Elasticsearch', 'Neo4j', 'CouchDB',
        
        // Data Science & AI
        'Machine Learning', 'Deep Learning', 'Neural Networks', 'TensorFlow', 'PyTorch',
        'Keras', 'scikit-learn', 'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn',
        'Natural Language Processing', 'NLP', 'Computer Vision', 'OpenCV', 'YOLO',
        'Big Data', 'Hadoop', 'Spark', 'Kafka', 'Airflow', 'Data Mining', 'ETL',
        'Data Visualization', 'Tableau', 'Power BI', 'Looker', 'Statistics', 'A/B Testing',
        
        // Networking
        'TCP/IP', 'DNS', 'DHCP', 'Routing', 'Switching', 'VLAN', 'BGP', 'OSPF',
        'Load Balancing', 'CDN', 'Network Architecture', 'Cisco', 'Juniper',
        
        // Testing & Quality
        'Unit Testing', 'Integration Testing', 'End-to-End Testing', 'Test Automation',
        'Selenium', 'Cypress', 'Jest', 'JUnit', 'Pytest', 'Mocha', 'Postman',
        'Load Testing', 'Performance Testing', 'Quality Assurance', 'QA',
        
        // Blockchain
        'Blockchain', 'Ethereum', 'Solidity', 'Smart Contracts', 'Web3', 'Cryptocurrency',
        'DeFi', 'NFT', 'Hyperledger',
        
        // Version Control & Tools
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN', 'JIRA', 'Confluence', 'Trello',
        'Slack', 'VS Code', 'IntelliJ', 'Eclipse', 'Visual Studio',
        
        // Methodologies
        'Agile', 'Scrum', 'Kanban', 'Waterfall', 'SAFe', 'Lean', 'DevOps', 'Microservices',
        'Serverless', 'Event-Driven Architecture', 'Design Patterns', 'SOLID', 'TDD', 'BDD',
        
        // Soft Skills
        'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Project Management',
        'Time Management', 'Critical Thinking', 'Adaptability', 'Collaboration',
        'Mentoring', 'Presentation', 'Negotiation', 'Strategic Planning'
    ];
    
    const foundSkills = [];
    const textLower = text.toLowerCase();
    
    skillsBank.forEach(skill => {
        if (textLower.includes(skill.toLowerCase())) {
            foundSkills.push(skill);
        }
    });
    
    return foundSkills;
}

function extractContact(text) {
    const contact = {};
    
    // Email
    const emailMatch = text.match(/[\w.-]+@[\w.-]+\.\w+/);
    if (emailMatch) contact.email = emailMatch[0];
    
    // Phone
    const phoneMatch = text.match(/(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/);
    if (phoneMatch) contact.phone = phoneMatch[0];
    
    // LinkedIn
    const linkedinMatch = text.match(/linkedin\.com\/in\/[\w-]+/i);
    if (linkedinMatch) contact.linkedin = linkedinMatch[0];
    
    // GitHub
    const githubMatch = text.match(/github\.com\/[\w-]+/i);
    if (githubMatch) contact.github = githubMatch[0];
    
    return contact;
}

function extractExperience(text) {
    // Look for experience-related keywords
    const hasExperience = /experience|worked|developed|managed|led|created|implemented/i.test(text);
    const yearsMatch = text.match(/(\d+)\+?\s*years?/i);
    
    return {
        hasExperience,
        years: yearsMatch ? parseInt(yearsMatch[1]) : 0
    };
}

function extractEducation(text) {
    const degrees = ['Bachelor', 'Master', 'PhD', 'B.Tech', 'M.Tech', 'B.S', 'M.S', 'MBA'];
    const foundDegrees = [];
    
    degrees.forEach(degree => {
        if (text.includes(degree)) {
            foundDegrees.push(degree);
        }
    });
    
    return {
        degrees: foundDegrees,
        hasEducation: foundDegrees.length > 0
    };
}

function calculateATSScore(text, skills, experience, education) {
    let score = 0;
    const components = {};
    
    // Keyword density (25 points)
    const keywords = ['experience', 'skills', 'education', 'projects', 'achievements'];
    let keywordCount = 0;
    keywords.forEach(kw => {
        if (text.toLowerCase().includes(kw)) keywordCount++;
    });
    components.keywords = Math.round((keywordCount / keywords.length) * 25);
    score += components.keywords;
    
    // Skills match (25 points)
    components.skills = Math.min(Math.round(skills.length * 2.5), 25);
    score += components.skills;
    
    // Format quality (20 points)
    const sections = ['experience', 'education', 'skills'].filter(s => 
        text.toLowerCase().includes(s)
    ).length;
    components.format = Math.round((sections / 3) * 20);
    score += components.format;
    
    // Experience (15 points)
    components.experience = experience.hasExperience ? 
        Math.min(15, experience.years * 3) : 0;
    score += components.experience;
    
    // Education (15 points)
    components.education = education.hasEducation ? 15 : 0;
    score += components.education;
    
    return {
        total: Math.min(score, 100),
        components
    };
}

function displayResults(data) {
    // Display ATS Score
    const scoreValue = data.atsScore.total;
    document.getElementById('scoreValue').textContent = scoreValue;
    
    const scoreCircle = document.getElementById('atsScore');
    if (scoreValue >= 75) {
        scoreCircle.classList.add('score-high');
        document.getElementById('scoreDescription').textContent = 'Excellent! Your resume is well-optimized for ATS systems.';
    } else if (scoreValue >= 50) {
        scoreCircle.classList.add('score-medium');
        document.getElementById('scoreDescription').textContent = 'Good, but there\'s room for improvement.';
    } else {
        scoreCircle.classList.add('score-low');
        document.getElementById('scoreDescription').textContent = 'Needs significant improvement to pass ATS screening.';
    }
    
    // Score Breakdown
    const breakdownHTML = Object.entries(data.atsScore.components).map(([key, value]) => `
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="font-weight: 600; text-transform: capitalize;">${key}</span>
                <span>${value} points</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${(value / 25) * 100}%"></div>
            </div>
        </div>
    `).join('');
    document.getElementById('scoreBreakdown').innerHTML = breakdownHTML;
    
    // Skills
    const skillsHTML = data.skills.map(skill => 
        `<span class="skill-tag">${skill}</span>`
    ).join('');
    document.getElementById('skillsContainer').innerHTML = skillsHTML || '<p style="color: var(--gray);">No skills detected. Consider adding a skills section to your resume.</p>';
    
    // Contact Info
    const contactHTML = Object.keys(data.contact).length > 0 ?
        Object.entries(data.contact).map(([key, value]) => `
            <p><strong>${key.charAt(0).toUpperCase() + key.slice(1)}:</strong> ${value}</p>
        `).join('') :
        '<p style="color: var(--gray);">No contact information detected.</p>';
    document.getElementById('contactInfo').innerHTML = contactHTML;
    
    // Recommendations
    const recommendations = generateRecommendations(data);
    document.getElementById('recommendations').innerHTML = recommendations;
    
    // Job Matches
    const jobMatches = calculateJobMatches(data.skills);
    const jobMatchesHTML = jobMatches.map(job => `
        <div style="background: var(--light-gray); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4>${job.title}</h4>
                <span class="skill-tag">${job.match}% Match</span>
            </div>
            <p style="color: var(--gray); margin-top: 0.5rem;">${job.description}</p>
        </div>
    `).join('');
    document.getElementById('jobMatches').innerHTML = jobMatchesHTML;
}

function generateRecommendations(data) {
    const recommendations = [];
    
    if (data.atsScore.total < 75) {
        recommendations.push('Add more relevant keywords related to your target job role');
    }
    if (data.skills.length < 10) {
        recommendations.push('Include more technical and soft skills in your resume');
    }
    if (!data.contact.email) {
        recommendations.push('Add your email address for easy contact');
    }
    if (!data.contact.linkedin && !data.contact.github) {
        recommendations.push('Include links to your professional profiles (LinkedIn, GitHub)');
    }
    if (!data.experience.hasExperience) {
        recommendations.push('Add a detailed work experience section with achievements');
    }
    if (!data.education.hasEducation) {
        recommendations.push('Include your educational qualifications');
    }
    
    return recommendations.map(rec => `
        <div style="background: #fef3c7; padding: 1rem; border-left: 4px solid var(--warning-color); margin-bottom: 1rem; border-radius: 4px;">
            <i class="fas fa-exclamation-triangle" style="color: var(--warning-color);"></i> ${rec}
        </div>
    `).join('');
}

function calculateJobMatches(skills) {
    const jobRoles = {
        'Cybersecurity Analyst': ['Security Analysis', 'Penetration Testing', 'SIEM', 'Firewall', 'Incident Response', 'Network Security'],
        'Security Engineer': ['Security Operations', 'Vulnerability Assessment', 'Cryptography', 'ISO 27001', 'Cloud Security', 'Ethical Hacking'],
        'SOC Analyst': ['SIEM', 'Splunk', 'Incident Response', 'Threat Intelligence', 'Security Monitoring', 'Log Analysis'],
        'Penetration Tester': ['Penetration Testing', 'Ethical Hacking', 'Metasploit', 'Burp Suite', 'Kali Linux', 'OSCP'],
        'Software Engineer': ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'SQL'],
        'Backend Developer': ['Python', 'Java', 'Node.js', 'SQL', 'REST API', 'Microservices'],
        'Frontend Developer': ['JavaScript', 'React', 'Angular', 'Vue', 'HTML', 'CSS'],
        'Full Stack Developer': ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'MongoDB'],
        'Mobile Developer': ['React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin'],
        'DevOps Engineer': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'CI/CD', 'Jenkins'],
        'Cloud Engineer': ['AWS', 'Azure', 'GCP', 'Terraform', 'CloudFormation', 'Lambda'],
        'Data Scientist': ['Python', 'Machine Learning', 'TensorFlow', 'Pandas', 'NumPy', 'Statistics'],
        'Data Engineer': ['Python', 'SQL', 'Spark', 'Kafka', 'ETL', 'Big Data'],
        'ML Engineer': ['Machine Learning', 'TensorFlow', 'PyTorch', 'Python', 'Deep Learning', 'Model Deployment'],
        'Network Engineer': ['TCP/IP', 'Routing', 'Switching', 'Firewall', 'Cisco', 'Network Architecture'],
        'Database Administrator': ['SQL', 'MySQL', 'PostgreSQL', 'Oracle', 'Database Performance', 'Backup & Recovery'],
        'QA Engineer': ['Test Automation', 'Selenium', 'Cypress', 'Quality Assurance', 'Unit Testing', 'Integration Testing'],
        'Product Manager': ['Project Management', 'Agile', 'Scrum', 'Leadership', 'Strategic Planning', 'Stakeholder Management'],
        'Blockchain Developer': ['Blockchain', 'Ethereum', 'Solidity', 'Smart Contracts', 'Web3', 'Cryptocurrency'],
        'AI/ML Researcher': ['Deep Learning', 'Neural Networks', 'Research', 'TensorFlow', 'PyTorch', 'NLP']
    };
    
    const matches = Object.entries(jobRoles).map(([title, requiredSkills]) => {
        const matchCount = requiredSkills.filter(skill => 
            skills.some(s => s.toLowerCase().includes(skill.toLowerCase()))
        ).length;
        const matchPercent = Math.round((matchCount / requiredSkills.length) * 100);
        
        return {
            title,
            match: matchPercent,
            description: `Matched ${matchCount} of ${requiredSkills.length} key skills`
        };
    });
    
    return matches.sort((a, b) => b.match - a.match).slice(0, 3);
}

function saveToHistory(data, filename) {
    const history = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
    history.unshift({
        filename,
        score: data.atsScore.total,
        skills: data.skills.length,
        timestamp: Date.now()
    });
    
    // Keep only last 10
    if (history.length > 10) history.pop();
    
    localStorage.setItem('resumeHistory', JSON.stringify(history));
}
