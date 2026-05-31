// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    loadDashboard();
});

function loadDashboard() {
    const resumeHistory = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
    const interviewHistory = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
    
    // Update statistics
    document.getElementById('totalResumes').textContent = resumeHistory.length;
    document.getElementById('totalInterviews').textContent = interviewHistory.length;
    
    // Average resume score
    if (resumeHistory.length > 0) {
        const avgResume = Math.round(
            resumeHistory.reduce((sum, r) => sum + r.score, 0) / resumeHistory.length
        );
        document.getElementById('avgResumeScore').textContent = avgResume;
    }
    
    // Average interview score
    if (interviewHistory.length > 0) {
        const avgInterview = Math.round(
            interviewHistory.reduce((sum, i) => sum + i.overallScore, 0) / interviewHistory.length
        );
        document.getElementById('avgInterviewScore').textContent = avgInterview + '%';
    }
    
    // Display recent resumes
    displayRecentResumes(resumeHistory);
    
    // Display recent interviews
    displayRecentInterviews(interviewHistory);
}

function displayRecentResumes(resumes) {
    const container = document.getElementById('recentResumes');
    
    if (resumes.length === 0) {
        container.innerHTML = '<p style="color: var(--gray); text-align: center; padding: 2rem;">No resumes analyzed yet. <a href="resume-analyzer.html" style="color: var(--primary-color);">Analyze your first resume</a></p>';
        return;
    }
    
    const html = resumes.map(resume => {
        const date = new Date(resume.timestamp);
        const scoreClass = resume.score >= 75 ? 'score-high' : 
                          resume.score >= 50 ? 'score-medium' : 'score-low';
        
        return `
            <div style="background: var(--light-gray); padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: grid; grid-template-columns: 1fr auto auto; gap: 1rem; align-items: center;">
                    <div>
                        <h4 style="margin-bottom: 0.5rem;">
                            <i class="fas fa-file-alt"></i> ${resume.filename}
                        </h4>
                        <p style="color: var(--gray); font-size: 0.9rem;">
                            <i class="fas fa-clock"></i> ${formatDate(date)}
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <div class="${scoreClass}" style="width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">
                            ${resume.score}
                        </div>
                        <p style="font-size: 0.9rem; margin-top: 0.5rem;">ATS Score</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: var(--primary-color);">
                            ${resume.skills}
                        </div>
                        <p style="font-size: 0.9rem;">Skills</p>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

function displayRecentInterviews(interviews) {
    const container = document.getElementById('recentInterviews');
    
    if (interviews.length === 0) {
        container.innerHTML = '<p style="color: var(--gray); text-align: center; padding: 2rem;">No interviews completed yet. <a href="mock-interview.html" style="color: var(--primary-color);">Start your first mock interview</a></p>';
        return;
    }
    
    const html = interviews.map(interview => {
        const date = new Date(interview.timestamp);
        const duration = formatDuration(interview.duration);
        const scoreClass = interview.overallScore >= 75 ? 'score-high' : 
                          interview.overallScore >= 50 ? 'score-medium' : 'score-low';
        
        return `
            <div style="background: var(--light-gray); padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center;">
                    <div>
                        <h4 style="margin-bottom: 0.5rem;">
                            <i class="fas fa-microphone"></i> ${formatRole(interview.role)}
                        </h4>
                        <p style="color: var(--gray); font-size: 0.9rem; margin-bottom: 0.5rem;">
                            <i class="fas fa-clock"></i> ${formatDate(date)} • ${duration} • ${interview.questionsCount} questions
                        </p>
                        <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                            <span style="background: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.9rem;">
                                <strong>Technical:</strong> ${interview.technicalScore}%
                            </span>
                            <span style="background: white; padding: 0.25rem 0.75rem; border-radius: 4px; font-size: 0.9rem;">
                                <strong>Communication:</strong> ${interview.communicationScore}%
                            </span>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div class="${scoreClass}" style="width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white; font-size: 1.5rem;">
                            ${interview.overallScore}%
                        </div>
                        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Overall</p>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

function formatDate(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatRole(role) {
    return role.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function clearAllData() {
    if (confirm('Are you sure you want to clear all your data? This cannot be undone.')) {
        localStorage.removeItem('resumeHistory');
        localStorage.removeItem('interviewHistory');
        location.reload();
    }
}
