// file: static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const nameInput = form.querySelector('input[name="nom"]');
    const postalCodeInput = form.querySelector('input[name="cp"]');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-messages';
    form.insertBefore(errorDiv, form.firstChild);

    form.addEventListener('submit', function(event) {
        let errors = [];
        errorDiv.innerHTML = '';

        if (nameInput.value.length < 3 || nameInput.value.length > 20) {
            errors.push('The name must be between 3 and 20 characters.');
        }
        if (!postalCodeInput.value.match(/^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$/)) {
            errors.push('Postal code must be in Canadian format (e.g., A1A 1A1).');
        }

        if (errors.length > 0) {
            event.preventDefault();
            errors.forEach(function(error) {
                const errorParagraph = document.createElement('p');
                errorParagraph.textContent = error;
                errorParagraph.style.color = 'red';
                errorDiv.appendChild(errorParagraph);
            });
        }
    });
});
