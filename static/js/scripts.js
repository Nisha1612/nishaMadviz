document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const loadingIndicator = document.getElementById('loading');
    const summaryDiv = document.getElementById('summary');

    form.addEventListener('submit', function() {
        loadingIndicator.style.display = 'block';
        summaryDiv.style.display = 'none';
    });

    // Hide loading indicator when the page reloads with a response
    if (summaryDiv && summaryDiv.textContent.trim() !== '') {
        loadingIndicator.style.display = 'none';
        summaryDiv.style.display = 'block';
    }
});