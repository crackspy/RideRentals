// Tab Switching Logic
function openTab(tabName) {
    const tabs = document.querySelectorAll(".tab-content");
    const buttons = document.querySelectorAll(".tab-button");

    tabs.forEach((tab) => tab.classList.remove("active"));
    buttons.forEach((button) => button.classList.remove("active"));

    document.getElementById(tabName).classList.add("active");
    document
        .querySelector(`[onclick="openTab('${tabName}')"]`)
        .classList.add("active");
}

// Password Validation
document.getElementById("registerForm").addEventListener("submit", function (event) {
    const password = document.getElementById("reg_password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    // Reset previous error messages
    resetError("reg_password");
    resetError("confirm_password");

    // Password length validation
    if (password.length < 6) {
        showError("reg_password", "Password must be at least 6 characters long");
        event.preventDefault();
        return false;
    }

    // Password match validation
    if (password !== confirmPassword) {
        showError("confirm_password", "Passwords do not match");
        event.preventDefault();
        return false;
    }
});

function showError(inputId, message) {
    const inputField = document.getElementById(inputId);
    const parentElement = inputField.parentElement; // This is the .form-group div

    // Set the input field border color to red to indicate an error
    inputField.style.borderColor = "red";

    // Create a new div for the error message container if it doesn't exist
    let errorDiv = document.querySelector(`#${inputId}-error-container`);

    // If errorDiv doesn't exist, create a new div
    if (!errorDiv) {
        // Create a new div for the error message container
        errorDiv = document.createElement("div");
        errorDiv.id = `${inputId}-error-container`; // Set a unique id for the error container
        errorDiv.className = "error-message-container"; // Add class for styling

        // Insert the errorDiv next to the .form-group div
        parentElement.parentElement.insertBefore(errorDiv, parentElement.nextSibling);
    }

    // Create or update the error message inside the error container
    let errorMessage = errorDiv.querySelector(".error-message");

    // If error message doesn't exist, create it
    if (!errorMessage) {
        errorMessage = document.createElement("span");
        errorMessage.className = "error-message"; // Apply class for styling
        errorDiv.appendChild(errorMessage);
    }

    // Set the error message text
    errorMessage.textContent = message;
}

function resetError(inputId) {
    const inputField = document.getElementById(inputId);
    const parentElement = inputField.parentElement;

    // Reset the input field border color
    inputField.style.borderColor = "";

    // Find the error message container and remove its content
    const errorDiv = parentElement.querySelector(".error-message-container");
    if (errorDiv) {
        errorDiv.remove(); // Remove the error message container
    }
}

// Password Visibility Toggle Script
function togglePassword(inputId, iconId) {
    const passwordField = document.getElementById(inputId);
    const icon = document.getElementById(iconId);

    if (passwordField.type === "password") {
        passwordField.type = "text";
        icon.setAttribute("name", "eye-off-outline"); // Change icon to eye-off
    } else {
        passwordField.type = "password";
        icon.setAttribute("name", "eye-outline"); // Change icon back to eye
    }
}