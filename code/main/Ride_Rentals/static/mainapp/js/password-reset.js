// Password Visibility Toggle Script
function togglePassword(inputId, iconId) {
    const passwordField = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    const isPassword = passwordField.type === "password";

    passwordField.type = isPassword ? "text" : "password";
    icon.setAttribute("name", isPassword ? "eye-off-outline" : "eye-outline");
}

function checkPasswordStrength(password, confirmPassword) {
    return {
        upperCase: /[A-Z]/.test(password),
        lowerCase: /[a-z]/.test(password),
        minLength: password.length >= 8,
        number: /\d/.test(password),
        special: /[!@#$%^&*()_+\-=\[\]{};':",\\|,.<>\/?]/.test(password),
        matchPassword: password === confirmPassword && password.length > 0
    };
}

function updateRuleIndicators() {
    const password = document.getElementById('id_new_password1').value;
    const confirmPassword = document.getElementById('id_new_password2').value;
    const rules = checkPasswordStrength(password, confirmPassword);

    Object.entries(rules).forEach(([rule, isValid]) => {
        const ruleElement = document.getElementById(rule);
        const icon = ruleElement.querySelector("ion-icon");

        icon.setAttribute("name", isValid ? "checkmark-circle-outline" : "close-circle-outline");
        icon.style.color = isValid ? "#39ff14" : "#ff3b30";
    });
}

function validatePassword(event) {
    event.preventDefault();

    const password = document.getElementById('id_new_password1').value;
    const confirmPassword = document.getElementById('id_new_password2').value;
    const rules = checkPasswordStrength(password, confirmPassword);

    if (!rules.minLength) {
        alert('Password must be at least 8 and max 12 characters long.');
        return;
    }

    if (!rules.matchPassword) {
        alert('Passwords do not match. Please try again.');
        return;
    }

    if (Object.values(rules).every(Boolean)) {
        document.getElementById('new_password_form').submit();
    } else {
        alert('Password validation failed. Please check the rules.');
    }
}

document.getElementById('id_new_password1').addEventListener('input', updateRuleIndicators);
document.getElementById('id_new_password2').addEventListener('input', updateRuleIndicators);