document.addEventListener("DOMContentLoaded", function () {
  
    const paymentMethods = document.querySelectorAll(".payment-option");
    const codMethod = document.querySelector(".cod");
    const confirmButton = document.querySelector(".btn-primary");
  
    // Ensure only Cash on Delivery is active
    paymentMethods.forEach((method) => {
        method.addEventListener("click", function () {
            if (method.classList.contains("unavailable")) {
                alert("This payment method is not available right now.");
            } else {
                // Remove 'selected' class from all and add it only to COD
                paymentMethods.forEach((m) => m.classList.remove("selected"));
                codMethod.classList.add("selected");
            }
        });
    });
  
    // Prevent submission if COD is not selected
    confirmButton.addEventListener("click", function (event) {
        if (!codMethod.classList.contains("selected")) {
            event.preventDefault();
            alert("Only Cash on Delivery is available at the moment.");
        }
    });
  });