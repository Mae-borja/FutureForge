// Function to toggle navbar and spin the logo
function toggleNavbar() {
    var navbar = document.getElementById("navbar");
    var logoContainer = document.querySelector('.logo-container');
    const mainContent = document.querySelector('.main-container');

    // Toggle the 'active' class for the navbar and main content
    navbar.classList.toggle("active");
    mainContent.classList.toggle("active");
    // Toggle the 'active' class for the logo-container
    logoContainer.classList.toggle("active");

    // Add spinning animation to the logo (if you want the logo itself to spin)
    var logo = document.getElementById("logo");
    logo.classList.add("spinning");

    // Remove spinning class after 0.3 seconds to stop the spin
    setTimeout(function() {
        logo.classList.remove("spinning");
    }, 300);
}




// Function to position the indicator
let marker = document.querySelector('#indicator');
let icons = document.querySelectorAll('.nav-item');

// This function calculates and sets the position of the marker
function setIndicatorPosition(icon) {
    let iconOffsetTop;

    // Calculate the position relative to the navbar
    if (icon.querySelector('img')) {
        // Get the icon or image element
        const userElement = icon.querySelector('img');
        // Calculate the position based on the icon/image
        iconOffsetTop = userElement.getBoundingClientRect().top - document.querySelector('.navbar').getBoundingClientRect().top;
    } else {
        // For other nav items, use the standard position
        iconOffsetTop = icon.getBoundingClientRect().top - document.querySelector('.navbar').getBoundingClientRect().top;
    }

    // Set the top position of the indicator to match the clicked nav-item
    marker.style.top = iconOffsetTop + 'px';
}

// Function to handle click event for nav items
function indicatorP(e) {
    let icon = e.target.closest('.nav-item'); // Get the closest nav-item
    setIndicatorPosition(icon); // Set the position of the indicator
    localStorage.setItem('activeNavItem', icon.getAttribute('href'));
}

// Add click event listeners to nav items
icons.forEach(icon => {
    icon.addEventListener('click', (e) => {
        indicatorP(e);
    });
});

// Load the active nav item from localStorage on page load
window.onload = function() {
    const activeNavItem = localStorage.getItem('activeNavItem');
    if (activeNavItem) {
        const navItem = document.querySelector(`a[href="${activeNavItem}"]`);
        if (navItem) {
            indicatorP({ target: navItem }); // Call the function with the nav-item
        }
    }
};

// Event listener for window resize to reposition the marker
window.addEventListener('resize', () => {
    const activeNavItem = localStorage.getItem('activeNavItem');
    if (activeNavItem) {
        const navItem = document.querySelector(`a[href="${activeNavItem}"]`);
        if (navItem) {
            setIndicatorPosition(navItem); // Recalculate position
        }
    }
});

function updateNavbarVisibility() {
    var navbar = document.getElementById("navbar");
    var logoContainer = document.querySelector('.logo-container');
    const mainContent = document.querySelector('.main-container');
    
    // Check if the window width is less than 768px
    if (window.innerWidth < 1200 ) {
        navbar.classList.remove("active"); // Remove active class to hide the navbar
        logoContainer.classList.remove("active");
        mainContent.classList.remove("active");
    } else {
         navbar.classList.add("active"); // Add active class to show the navbar
        logoContainer.classList.add("active");
        mainContent.classList.add("active");
    }
}

// Event listener for window resize
window.addEventListener('resize', updateNavbarVisibility);

// Initial check on page load
updateNavbarVisibility();
