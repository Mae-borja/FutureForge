/*document.addEventListener("DOMContentLoaded", function() {
    fetch('../Navbar/navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
        });
});
*/

window.addEventListener('scroll', function() {
    const insightsContainer = document.querySelector('.insight-container');
    const manageButton = document.querySelector('.manage-button');
    const skillsSection = document.getElementById('skillcontainer');
    const skillsSectionRect = skillsSection.getBoundingClientRect();

    // Hide insights when in the skills section
    if (skillsSectionRect.top < window.innerHeight && skillsSectionRect.bottom >= 0) {
        insightsContainer.style.visibility = 'hidden'; // Hide insights
        manageButton.style.visibility = 'visible'; // Show Manage Skills button
    } else {
        insightsContainer.style.visibility = 'visible'; // Show insights
        manageButton.style.visibility = 'hidden'; // Hide Manage Skills button
    }
});



function showAndScrollToSkills() {
    const skillsSection = document.getElementById('skillcontainer');
    const manageButton = document.querySelector('.manage-button');

    // Make the skills section visible
    skillsSection.style.display = 'flex';

    // Show the manage button
    manageButton.style.visibility = 'visible';

    // Scroll to the skills section smoothly
    skillsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Adjust scroll position by a specific offset smoothly using window.scrollTo
    setTimeout(() => {
        let scrollPosition = window.scrollY;
        window.scrollTo({
            top: scrollPosition + 275,  // Add 175px to the current position
            behavior: 'smooth'          // Smooth scroll
        });
    }, 300);  // Delay to allow the initial scroll to finish before adjusting
}


function toggleModal() {
    const modal = document.getElementById("skillsModal");
    const modalContent = modal.querySelector(".modal-content");
    const manageButton = document.getElementById("manageButton");
    const mainContent = document.getElementById("mainContent");

    // Select the analyze container elements
    const analyzeContainer = document.querySelector('.analyze-container');
    const analyzeImage = analyzeContainer.querySelector('img');
    const analyzeText = analyzeContainer.querySelector('h2');

    const modalStyle = window.getComputedStyle(modal);
    
    if (modalStyle.display === "block") {
        // Close the modal
        
        modal.style.display = "none";
        modalContent.classList.remove("show");
        manageButton.textContent = "Manage Skills"; // Change button text to 'Manage Skills'
        mainContent.style.display = "block"; // Show main content again
        
        // Scroll to the #Description section smoothly
        const descriptionSection = document.getElementById("skillcontainer");
        descriptionSection.scrollIntoView({ behavior: 'auto' });

        // Reset the analyze-container image and text
        analyzeImage.src = "/static/Images/Analyze.png"; // Reset to original image
        analyzeText.textContent = "Gap Report"; // Reset to original text
    } else {
        // Open the modal
        modal.style.display = "block";
        modalContent.classList.add("show");
        manageButton.textContent = "Close Modal"; // Change button text to 'Close Modal'
        mainContent.style.display = "none"; // Hide main content
        
        // Change the analyze-container image and text
        analyzeImage.src = "/static/Images/Bookmark manager.png"; // Change to the new image you want
        analyzeText.textContent = "Manage Skills"; // Change to the new text you want
    }
}