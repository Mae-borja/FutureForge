document.addEventListener("DOMContentLoaded", function() {
    // Load the navbar
    fetch('../Navbar/navbar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('navbar').innerHTML = data;
        });

    // Automatically click the first diamond to set it as active
    const firstDiamond = document.querySelector('.diamond');
    if (firstDiamond) {
        expandDiamond(firstDiamond);
    }
});

let activeDiamond = null; // Track the currently active diamond
let activeContent = null; // Track the currently active content container

function expandDiamond(element) {
    // Check if the clicked diamond is already active, and if so, do nothing
    if (element === activeDiamond) return;

    // If there is an active diamond and it is not the clicked one, reset it
    if (activeDiamond) {
        activeDiamond.style.width = '100px'; // Original width
        activeDiamond.style.height = '100px'; // Original height
        const activeText = activeDiamond.querySelector('.diamond-text');
        activeText.style.fontSize = '40px'; // Original text size

        // Reset the bottom line color
        const activeBottomLine = activeDiamond.nextElementSibling;
        activeBottomLine.style.borderBottom = `7px solid ${activeDiamond.style.backgroundColor}`;

        // Reset the diamond container gradient
        const activeContainer = activeBottomLine.parentElement;
        activeContainer.style.background = '';

        // Reset box shadow
        activeDiamond.style.boxShadow = '';

        // Hide the previously active content container
        if (activeContent) {
            activeContent.style.display = 'none';
        }
    }

    // Enlarge the clicked diamond
    element.style.width = '130px';
    element.style.height = '130px';
    
    // Change the text size
    const diamondText = element.querySelector('.diamond-text');
    diamondText.style.fontSize = '50px';

    // Change the color of the bottom line to match the diamond
    const bottomLine = element.nextElementSibling;
    bottomLine.style.borderBottom = `0 solid ${element.style.backgroundColor}`;

    // Set the current diamond as the active one
    activeDiamond = element;

    // Apply linear gradient to the diamond container
    const container = bottomLine.parentElement;
    container.style.background = `linear-gradient(to top, ${element.style.backgroundColor}, transparent)`;

    // Add white shadow to the diamond
    element.style.boxShadow = `0 4px 10px rgba(255, 255, 255, 0.5)`;

    // Show the corresponding content container based on the diamond clicked
    const diamondIndex = Array.from(document.querySelectorAll('.diamond')).indexOf(element);
    const contentContainers = document.querySelectorAll('.content-container');
    
    if (contentContainers[diamondIndex]) {
        activeContent = contentContainers[diamondIndex];
        activeContent.style.display = 'block'; // Show the content container
    }
}
