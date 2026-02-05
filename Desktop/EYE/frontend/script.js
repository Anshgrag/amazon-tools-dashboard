const API_URL = 'http://localhost:8000/predict';

const classExplanations = {
    'Normal': 'The image appears to show a healthy eye with no visible signs of infection or abnormalities.',
    'Conjunctivitis': 'The image shows possible signs of conjunctivitis (pink eye) including redness, swelling, or discharge. Consult an eye doctor for proper diagnosis and treatment.',
    'Cataract': 'The image may indicate cataract formation, characterized by cloudiness in the lens. This condition typically requires professional medical evaluation and treatment.',
    'Glaucoma': 'The image suggests potential signs of glaucoma, a serious eye condition that can damage the optic nerve. Immediate consultation with an ophthalmologist is recommended.'
};

const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const analyzeBtn = document.getElementById('analyzeBtn');
const removeBtn = document.getElementById('removeBtn');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const resultClass = document.getElementById('resultClass');
const confidenceScore = document.getElementById('confidenceScore');
const resultExplanation = document.getElementById('resultExplanation');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');

let selectedFile = null;

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', handleFileSelect);

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
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

removeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    removeFile();
});

analyzeBtn.addEventListener('click', analyzeImage);

retryBtn.addEventListener('click', () => {
    errorSection.style.display = 'none';
});

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    if (!file.type.match('image.*')) {
        showError('Please select a valid image file (JPEG or PNG).');
        return;
    }

    selectedFile = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'block';
        analyzeBtn.disabled = false;
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function removeFile() {
    selectedFile = null;
    fileInput.value = '';
    previewImage.src = '';
    uploadArea.style.display = 'block';
    previewContainer.style.display = 'none';
    analyzeBtn.disabled = true;
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

async function analyzeImage() {
    if (!selectedFile) {
        showError('Please select an image first.');
        return;
    }

    document.body.classList.add('loading');
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed. Please try again.');
        }

        const data = await response.json();
        
        displayResult(data);

    } catch (error) {
        showError(error.message || 'An error occurred during analysis. Please ensure the backend server is running.');
    } finally {
        document.body.classList.remove('loading');
    }
}

function displayResult(data) {
    resultClass.textContent = data.predicted_class;
    confidenceScore.textContent = (data.confidence_score * 100).toFixed(1) + '%';
    resultExplanation.textContent = classExplanations[data.predicted_class] || 'Analysis complete.';
    
    const resultsCard = document.querySelector('.results-card');
    
    if (data.predicted_class === 'Normal') {
        resultsCard.style.borderLeftColor = '#10b981';
        resultClass.style.color = '#10b981';
    } else if (data.predicted_class === 'Conjunctivitis') {
        resultsCard.style.borderLeftColor = '#f59e0b';
        resultClass.style.color = '#f59e0b';
    } else if (data.predicted_class === 'Cataract') {
        resultsCard.style.borderLeftColor = '#8b5cf6';
        resultClass.style.color = '#8b5cf6';
    } else if (data.predicted_class === 'Glaucoma') {
        resultsCard.style.borderLeftColor = '#ef4444';
        resultClass.style.color = '#ef4444';
    }
    
    resultsSection.style.display = 'block';
    
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Eye Infection Detection App initialized');
});
