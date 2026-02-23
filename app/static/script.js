const form = document.getElementById('studentForm');
const submitBtn = document.getElementById('submitBtn');
const fillSampleBtn = document.getElementById('fillSampleBtn');
const resultSection = document.getElementById('resultSection');
const riskBadge = document.getElementById('riskBadge');
const riskLevel = document.getElementById('riskLevel');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const resultMessage = document.getElementById('resultMessage');
const resultIcon = document.getElementById('resultIcon');

// Sample data for quick testing
const sampleData = {
    school: "GP",
    sex: "F",
    age: 17,
    address: "U",
    famsize: "GT3",
    Pstatus: "T",
    Medu: 4,
    Fedu: 4,
    Mjob: "teacher",
    Fjob: "services",
    reason: "course",
    guardian: "mother",
    traveltime: 2,
    studytime: 3,
    failures: 0,
    schoolsup: "yes",
    famsup: "no",
    paid: "no",
    activities: "yes",
    nursery: "yes",
    higher: "yes",
    internet: "yes",
    romantic: "no",
    famrel: 4,
    freetime: 3,
    goout: 3,
    Dalc: 1,
    Walc: 1,
    health: 4,
    absences: 4,
    G1: 15,
    G2: 14
};

// Fill sample data
fillSampleBtn.addEventListener('click', () => {
    Object.keys(sampleData).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            element.value = sampleData[key];
        }
    });
    
    // Smooth scroll to submit button
    submitBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Highlight submit button
    submitBtn.style.animation = 'pulse 1s ease 3';
    setTimeout(() => {
        submitBtn.style.animation = '';
    }, 3000);
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(form);
    const data = {};
    
    formData.forEach((value, key) => {
        // Convert numeric fields
        if (['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 
             'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 
             'absences', 'G1', 'G2'].includes(key)) {
            data[key] = parseInt(value);
        } else {
            data[key] = value;
        }
    });
    
    // Show loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResult(result);
        } else {
            showError('Prediction failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection.');
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
});

function displayResult(result) {
    const { risk_level, confidence, message } = result;
    
    // Update risk badge
    riskLevel.textContent = risk_level;
    riskBadge.className = 'risk-badge';
    
    if (risk_level === 'At-risk') {
        riskBadge.classList.add('at-risk');
        updateIcon('danger');
    } else if (risk_level === 'Average') {
        riskBadge.classList.add('average');
        updateIcon('warning');
    } else {
        riskBadge.classList.add('high-performing');
        updateIcon('success');
    }
    
    // Update confidence
    confidenceValue.textContent = `${confidence}%`;
    confidenceFill.style.width = `${confidence}%`;
    
    // Update message
    resultMessage.textContent = message;
    
    // Scroll to result on mobile
    if (window.innerWidth <= 1024) {
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function updateIcon(type) {
    const icons = {
        success: `
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <circle cx="30" cy="30" r="28" stroke="currentColor" stroke-width="3"/>
                <path d="M20 30L27 37L40 23" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
            </svg>
        `,
        warning: `
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <circle cx="30" cy="30" r="28" stroke="currentColor" stroke-width="3"/>
                <path d="M30 20V32M30 40V42" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
            </svg>
        `,
        danger: `
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <circle cx="30" cy="30" r="28" stroke="currentColor" stroke-width="3"/>
                <path d="M22 22L38 38M38 22L22 38" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
            </svg>
        `
    };
    
    resultIcon.innerHTML = icons[type];
}

function showError(message) {
    resultMessage.textContent = message;
    riskLevel.textContent = 'Error';
    riskBadge.className = 'risk-badge at-risk';
    confidenceFill.style.width = '0%';
    updateIcon('danger');
}

// Add smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Form validation feedback
const inputs = form.querySelectorAll('input, select');
inputs.forEach(input => {
    input.addEventListener('invalid', (e) => {
        e.preventDefault();
        input.style.borderColor = 'var(--danger)';
    });
    
    input.addEventListener('input', () => {
        input.style.borderColor = 'var(--border)';
    });
});
