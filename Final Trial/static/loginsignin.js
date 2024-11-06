function validateAndProceed(nextModalId, event) {
    // Prevent default form submission
    event.preventDefault();

    // Get the form that triggered the event
    var form = event.target;

    // Check if the form is valid
    if (form.checkValidity()) {
        // Form is valid, show the next modal
        showModal(nextModalId);
        return true; // Optionally allow form submission if needed
    } else {
        // Form is invalid, show validation errors
        form.reportValidity();
        return false; // Prevent form submission
    }
}

function showModal(modalId) {
    // Hide all modals
    document.getElementById('login').style.display = 'none';
    document.getElementById('signin').style.display = 'none';
    document.getElementById('enterEmail').style.display = 'none';
    document.getElementById('enterNumber').style.display = 'none';
    document.getElementById('enterNewPass').style.display = 'none';

    // Show the requested modal
    document.getElementById(modalId).style.display = 'block';
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    var modals = ['login', 'signin', 'enterEmail', 'enterNumber', 'enterNewPass'];
    modals.forEach(function(modalId) {
        var modal = document.getElementById(modalId);
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
};
