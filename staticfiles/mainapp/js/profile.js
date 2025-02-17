// vars
const Wishlist = document.getElementById("wishlistPopup");
const Booking = document.getElementById("bookingPopup");
const Settings = document.getElementById("settingsPopup");

const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");

// ---------------Wishlist popup ------------------
// Function to open the wishlist popup
function openWishlistPopup() {
    // Show popup and overlay
    Wishlist.style.display = "flex";
    document.body.style.overflow = "hidden";  // Prevent body from scrolling when popup is open

    // Add overlay
    var overlay = document.createElement("div");
    overlay.id = "popup-overlay";
    overlay.className = "popup-overlay";
    document.body.appendChild(overlay);

    sidebarToggle.style.display = 'none';

    // Close popup when clicking outside
    overlay.onclick = function () {
        closeWishlistPopup();
    };
}

// Function to close the wishlist popup
function closeWishlistPopup() {
    // Hide popup and overlay
    Wishlist.style.display = "none";
    document.body.style.overflow = "auto";  // Allow body to scroll again

    // Remove overlay
    var overlay = document.getElementById("popup-overlay");
    if (overlay) {
        overlay.remove();
    }
    sidebarToggle.style.display = 'block';
}

// ---------------Booking popup ------------------
// Function to open the booking popup
function openBookingPopup() {
    // Show popup and overlay
    Booking.style.display = "flex";
    document.body.style.overflow = "hidden";  // Prevent body from scrolling when popup is open

    sidebarToggle.style.display = 'none';

    // Add overlay
    var overlay = document.createElement("div");
    overlay.id = "popup-overlay";
    overlay.className = "popup-overlay";
    document.body.appendChild(overlay);

    // Close popup when clicking outside
    overlay.onclick = function () {
        closeBookingPopup();
    };
}

// Function to close the booking popup
function closeBookingPopup() {
    // Hide popup and overlay
    Booking.style.display = "none";
    document.body.style.overflow = "auto";  // Allow body to scroll again

    // Remove overlay
    var overlay = document.getElementById("popup-overlay");
    if (overlay) {
        overlay.remove();
    }

    sidebarToggle.style.display = 'block';
}

// ---------------Settings popup ------------------
// Function to open the settings popup
function openSettingsPopup() {
    // Show popup and overlay
    Settings.style.display = "flex";
    document.body.style.overflow = "hidden";  // Prevent body from scrolling when popup is open

    sidebarToggle.style.display = 'none';
    sidebar.classList.remove("open");
    Sidebar();

    // Add overlay
    var overlay = document.createElement("div");
    overlay.id = "popup-overlay";
    overlay.className = "popup-overlay";
    document.body.appendChild(overlay);

    // Close popup when clicking outside
    overlay.onclick = function () {
        closeSettingsPopup();
    };
}

// Function to close the settings popup
function closeSettingsPopup() {
    // Hide popup and overlay
    Settings.style.display = "none";
    document.body.style.overflow = "auto";  // Allow body to scroll again

    // Remove overlay
    var overlay = document.getElementById("popup-overlay");
    if (overlay) {
        overlay.remove();
    }

    sidebarToggle.style.display = 'block';
}

// ---------------Side bar ------------------
// Function to slidbar
document.addEventListener("DOMContentLoaded", function () {

    // Toggle sidebar on click
    sidebarToggle.addEventListener("click", () => {
        if (sidebar.classList.contains('open')) {
            sidebar.classList.remove("open");
            Sidebar();
        } else {
            sidebar.classList.add("open");
            // Add overlay
            var overlay = document.createElement("div");
            overlay.id = "popup-overlay";
            overlay.className = "popup-overlay";
            document.body.appendChild(overlay);

            // Close popup when clicking outside
            overlay.onclick = function () {
                sidebar.classList.remove("open");
                Sidebar();
            };
            Sidebar();
        }

    });
});

function Sidebar() {
    // Change the toggle button text
    if (sidebar.classList.contains("open")) {
        sidebarToggle.classList.add('arrow-back');
        sidebarToggle.innerHTML = '<ion-icon name="arrow-back"></ion-icon>';
        sidebarToggle.style.animation = 'none';
    } else {

        // Remove overlay
        var overlay = document.getElementById("popup-overlay");
        if (overlay) {
            overlay.remove();
        }
        sidebarToggle.classList.remove('arrow-back');
        sidebarToggle.innerHTML = '<ion-icon name="arrow-forward"></ion-icon>';
        sidebarToggle.style.animation = 'none';
    }
}