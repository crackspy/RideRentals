// Get DOM Elements
const uploadPopup = document.getElementById("uploadPopup");
const openUploadButton = document.getElementById("openUploadButton");
const imageUpload = document.getElementById("imageUpload");
const profileImage = document.getElementById("profileImage");
const fileNameSpan = document.getElementById("fileName");
const revertButton = document.getElementById("revertImage");
const setDefaultButton = document.getElementById("setDefaultButton");
const setDefaultField = document.getElementById("setDefaultPictureField");

// Store initial image sources
const initialImageSrc = profileImage?.src || "";  // The image from the database
const defaultImageSrc = profileImage?.getAttribute("data-default") || ""; 
let lastUploadedFile = null; // Store the last uploaded file

// Utility function: Extract filename from URL
const getFileName = (url) => url?.split('/').pop() || "";

// Toggle "Set Default" button visibility
const toggleButtons = () => {
    if (!profileImage || !setDefaultButton || !revertButton) return;

    const isDefault = getFileName(profileImage.src) === getFileName(defaultImageSrc);
    const isInitial = getFileName(profileImage.src) === getFileName(initialImageSrc);

    setDefaultButton.style.display = isDefault ? "none" : "block";
    revertButton.style.display = isInitial ? "none" : "block";
};

// Handle "Set Default" button click
setDefaultButton?.addEventListener("click", () => {
    if (profileImage && profileImage.src !== defaultImageSrc) {
        lastUploadedFile = null; // Reset last uploaded file
        profileImage.src = defaultImageSrc;
        setDefaultField.value = "true";
        imageUpload.value = ""; // Clear file input
        toggleButtons();
    }
});

// Handle "Revert" button click
revertButton?.addEventListener("click", () => {
    if (!profileImage) return;

    profileImage.src = initialImageSrc;  // Restore the original DB image
    setDefaultField.value = "false";

    if (lastUploadedFile) {
        // Manually reset file input to match the previous upload
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(lastUploadedFile);
        imageUpload.files = dataTransfer.files;
    } else {
        imageUpload.value = "";  // No previous upload, just reset
    }

    fileNameSpan.innerText = ""; // Clear file name display
    toggleButtons();
});

// Open & Close Upload Popup
const openUploadPopup = () => {
    if (!uploadPopup) return;
    uploadPopup.style.display = "block";
    document.body.style.overflow = "hidden";

    const overlay = document.createElement("div");
    overlay.id = "popup-overlay";
    overlay.className = "popup-overlay";
    document.body.appendChild(overlay);
    overlay.addEventListener("click", closeUploadPopup);
};

const closeUploadPopup = () => {
    if (!uploadPopup) return;
    uploadPopup.style.display = "none";
    document.body.style.overflow = "auto";
    document.getElementById("popup-overlay")?.remove();
};

openUploadButton?.addEventListener("click", openUploadPopup);

// Handle File Drag & Drop
const handleDragOver = (event) => event.preventDefault();
const handleDrop = (event) => {
    event.preventDefault();
    handleFile(event.dataTransfer.files[0]);
};

document.addEventListener("dragover", handleDragOver);
document.addEventListener("drop", handleDrop);

// Handle Image Upload & Preview
imageUpload?.addEventListener("change", () => handleFile(imageUpload.files[0]));

const handleFile = (file) => {
    if (!file) return;

    const validTypes = ["image/png", "image/jpg", "image/jpeg"];
    if (file.size > 5 * 1024 * 1024 || !validTypes.includes(file.type)) {
        fileNameSpan.innerText = "Select another image";
        fileNameSpan.style.color = "red";
        return;
    }

    fileNameSpan.innerText = file.name;
    fileNameSpan.style.color = "green";

    const okButton = document.createElement("button");
    okButton.innerText = "OK";
    okButton.classList.add("ok-btn");
    okButton.onclick = (event) => {
        event.stopPropagation();
        previewImage(file);
        closeUploadPopup();
    };

    fileNameSpan.innerHTML = `${file.name} `;
    fileNameSpan.appendChild(okButton);
};

const previewImage = (file) => {
    const reader = new FileReader();
    reader.onload = (event) => {
        if (profileImage) {
            profileImage.src = event.target.result;
            lastUploadedFile = file; // Store the uploaded file
            revertButton.style.display = "block";
            setDefaultField.value = "false";
            toggleButtons();
        }
    };
    reader.readAsDataURL(file);
};

// Initialize
profileImage?.addEventListener("load", toggleButtons);
toggleButtons();


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("profile_update_form");

    // Utility function to show error message
    function showError(input, message) {
        input.style.boxShadow = "0 0 8px rgb(255, 36, 36)";
        const parentDiv = input.parentElement;
        parentDiv.classList.add("form-input-error"); 
        let errorSpan = parentDiv.querySelector(".field-error");
        if (!errorSpan) {
            errorSpan = document.createElement("span");
            errorSpan.className = "field-error";
            parentDiv.appendChild(errorSpan);
            parentDiv
        }
        errorSpan.textContent = message;
    }

    // Utility function to clear error
    function clearError(input) {
        input.style.boxShadow = "0 0 8px rgb(56, 255, 0)";
        const parentDiv = input.parentElement;
        parentDiv.classList.remove("form-input-error");
        let errorSpan = input.nextElementSibling;
        if (errorSpan && errorSpan.classList.contains("field-error")) {
            errorSpan.remove();
        }
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent default submission

        // Get form inputs
        const firstName = document.getElementById("id_first_name");
        const lastName = document.getElementById("id_last_name");
        const email = document.getElementById("id_email");
        const phone = document.getElementById("id_phone_number");

        let isValid = true;

        // Validate First Name
        if (!/^[A-Za-z\s]{2,}$/.test(firstName.value.trim())) {
            showError(firstName, "Enter a valid first name");
            isValid = false;
        } else {
            clearError(firstName);
        }

        // Validate Last Name
        if (!/^[A-Za-z\s]{1,}$/.test(lastName.value.trim())) {
            showError(lastName, "Enter a valid last name");
            isValid = false;
        } else {
            clearError(lastName);
        }

        // Validate Email
        if (!/^.{2,}@.+\..+$/.test(email.value.trim())) {
            showError(email, "Enter a valid email address.");
            isValid = false;
        } else {
            clearError(email);
        }

        // Validate Phone Number
        if (!/^\d{10}$/.test(phone.value.trim())) {
            showError(phone, "Phone number must be exactly 10 digits.");
            isValid = false;
        } else {
            clearError(phone);
        }

        // Submit form if valid
        if (isValid) {
            form.submit();
        }
    });
});

