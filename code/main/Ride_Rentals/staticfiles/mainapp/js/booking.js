// vars
const carPriceElement = document.getElementById("car_price");
const totalRentElement = document.getElementById("total_rent");
const pickupDateInput = document.getElementById("pickup-date");
const returnDateInput = document.getElementById("return-date");

// calcualte total price

function calculateRentalPrice() {
    // Parse the car price (monthly)
    const carPricePerMonth = parseFloat(
        carPriceElement.textContent.replace(/[₹,]/g, "")
    );
    const pickupDate = new Date(pickupDateInput.value);
    const returnDate = new Date(returnDateInput.value);

    // Update the min attribute for return-date
    if (!isNaN(pickupDate)) {
        const newMinReturnDate = new Date(pickupDate);
        newMinReturnDate.setDate(newMinReturnDate.getDate() + 1); // Add 1 day
        returnDateInput.min = newMinReturnDate.toISOString().split("T")[0];

        // Only reset return date if it's before the min allowed return date
        if (returnDate < newMinReturnDate || isNaN(returnDate)) {
            returnDateInput.value = newMinReturnDate.toISOString().split("T")[0];
        }
    }

    // Check if dates are invalid
    if (isNaN(pickupDate) || isNaN(returnDate) || returnDate <= pickupDate) {
        totalRentElement.textContent = "Total Rent: ₹0.00";
        return;
    }

    // Calculate the total number of days
    const daysDifference = Math.ceil(
        (returnDate - pickupDate) / (1000 * 60 * 60 * 24)
    );

    // Calculate the monthly price prorated for the number of days
    const daysInMonth = 30; // Assumption
    const totalPrice = (carPricePerMonth / daysInMonth) * daysDifference;

    // Round the total rent to the nearest integer
    const roundedTotalPrice = Math.round(totalPrice);

    // Update the total rent display
    totalRentElement.textContent = `Total Rent: ₹${roundedTotalPrice}`;
}

// Event listener for pickup-date changes
function handlePickupDateChange() {
    const pickupDate = new Date(pickupDateInput.value);
    const newMinReturnDate = new Date(pickupDate);
    newMinReturnDate.setDate(newMinReturnDate.getDate() + 1); // Add 1 day

    // Set the new minimum date for return-date
    returnDateInput.min = newMinReturnDate.toISOString().split("T")[0];
    returnDateInput.value = newMinReturnDate.toISOString().split("T")[0];

    // Clear the return-date value if it is invalid
    if (new Date(returnDateInput.value) <= pickupDate) {
        returnDateInput.value = "";
    }

    calculateRentalPrice();
}

// Attach event listeners
document
    .getElementById("pickup-date")
    .addEventListener("change", handlePickupDateChange);
document
    .getElementById("return-date")
    .addEventListener("change", calculateRentalPrice);

// Trigger the pickup-date change event on page load
window.addEventListener("load", () => {
    // Manually trigger the change event for pickup-date
    const event = new Event("change");
    pickupDateInput.dispatchEvent(event);
});

//  form validation
document.querySelector("form").addEventListener("submit", function (e) {
    // Prevent the default form submission
    e.preventDefault();

    // Utility function to show error message
    function showError(input, message) {
        input.style.boxShadow = "0 0 8px rgb(255, 36, 36)";
        // Remove existing error message
        const parentDiv = input.parentElement;
        let errorSpan = parentDiv.querySelector(".field-error");
        if (!errorSpan) {
            errorSpan = document.createElement("span");
            errorSpan.className = "field-error";
            parentDiv.appendChild(errorSpan);
        }
        errorSpan.textContent = message;
    }

    // Utility function to clear error
    function clearError(input) {
        input.style.boxShadow = "0 0 8px rgb(56, 255, 0)";
        const parentDiv = input.parentElement;
        const errorSpan = parentDiv.querySelector(".field-error");
        if (errorSpan) {
            parentDiv.removeChild(errorSpan);
        }
    }

    // Get form inputs
    const fullName = document.getElementById("full-name");
    const email = document.getElementById("email");
    const phone = document.getElementById("phone");
    const pickupDate = new Date(document.getElementById("pickup-date").value);
    const pDate = document.getElementById("pickup-date");
    const returnDate = new Date(document.getElementById("return-date").value);
    const rDate = document.getElementById("return-date");
    const today = new Date();

    // Validate Full Name
    if (!/^[A-Za-z\s]{3,}$/.test(fullName.value.trim())) {
        showError(
            fullName,
            "Full Name must contain at least 3 letters and only letters and spaces."
        );
        return;
    } else {
        clearError(fullName);
    }

    // Validate Email
    if (!/^.{4,}@.+\..+$/.test(email.value.trim())) {
        showError(email, "Enter a vaild email address");
        return;
    } else {
        clearError(email);
    }

    // Validate Phone Number
    if (!/^\d{10,}$/.test(phone.value.trim())) {
        showError(phone, "Enter a vaild phone number");
        return;
    } else {
        clearError(phone);
    }

    // Validate Pickup Date
    if (pickupDate < today.setHours(0, 0, 0, 0)) {
        showError(pDate, "Pick-Up Date cannot be earlier than today.");
        return;
    } else {
        clearError(pDate);
    }

    // Validate Return Date
    if (returnDate <= pickupDate) {
        showError(
            rDate,
            "Return Date cannot be earlier than or same as Pick-Up Date."
        );
        return;
    } else {
        clearError(rDate);
    }

    // If all validations pass, submit the form
    e.target.submit();
});