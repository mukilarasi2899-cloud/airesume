// Main JavaScript for Homepage
document.addEventListener('DOMContentLoaded', function() {
    // Animate statistics on homepage
    animateStats();
});

function animateStats() {
    const resumesEl = document.getElementById('resumesAnalyzed');
    const interviewsEl = document.getElementById('interviewsConducted');
    
    if (resumesEl && interviewsEl) {
        // Get data from localStorage
        const resumes = JSON.parse(localStorage.getItem('resumeHistory') || '[]');
        const interviews = JSON.parse(localStorage.getItem('interviewHistory') || '[]');
        
        animateValue(resumesEl, 0, resumes.length, 1500);
        animateValue(interviewsEl, 0, interviews.length, 1500);
    }
}

function animateValue(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}
