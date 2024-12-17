// Create floating particles
        function createParticles() {
            const container = document.getElementById('particles');
            const particleCount = 50;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 8 + 's';
                particle.style.opacity = Math.random() * 0.5 + 0.2;
                
                container.appendChild(particle);
            }
        }

        // Handle form submission
        function handleLogin(event) {
            event.preventDefault();
            
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            let isValid = true;

            // Reset error messages
            document.querySelectorAll('.error-message').forEach(elem => {
                elem.style.display = 'none';
            });

            // Validate email
            if (!isValidEmail(email.value)) {
                showError('emailError', 'Please enter a valid email address');
                isValid = false;
            }

            // Validate password
            if (password.value.length < 6) {
                showError('passwordError', 'Password must be at least 6 characters');
                isValid = false;
            }

            if (isValid) {
                // Simulated login success
                alert('Login successful! (Demo only)');
                document.getElementById('loginForm').reset();
            }

            return false;
        }

        // Email validation
        function isValidEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }

        // Show error message
        function showError(elementId, message) {
            const errorElement = document.getElementById(elementId);
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }

        // Handle social login buttons
        function handleSocialLogin(provider) {
            alert(`${provider} login would be implemented here`);
        }

        // Handle forgot password
        function handleForgotPassword() {
            alert('Password reset would be implemented here');
        }

        // Handle sign up
        function handleSignUp() {
            alert('Sign up would be implemented here');
        }

        // Add mouse move effect for gradient spheres
        document.addEventListener('mousemove', (e) => {
            const spheres = document.querySelectorAll('.gradient-sphere');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            spheres.forEach((sphere, index) => {
                const speed = (index + 1) * 20;
                const xOffset = (0.5 - x) * speed;
                const yOffset = (0.5 - y) * speed;
                
                sphere.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(${1 + (index * 0.1)})`;
            });
        });

        // Add smooth reveal animation for form elements
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize particles
            createParticles();

            // Animate form elements
            const elements = document.querySelectorAll('.form-group, .submit-button, .divider, .social-login, .additional-options');
            elements.forEach((element, index) => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    element.style.transition = 'all 0.6s ease-out';
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, 100 * index);
            });

            // Add input focus effects
            const inputs = document.querySelectorAll('.form-input');
            inputs.forEach(input => {
                input.addEventListener('focus', () => {
                    input.parentElement.classList.add('focused');
                });
                
                input.addEventListener('blur', () => {
                    if (!input.value) {
                        input.parentElement.classList.remove('focused');
                    }
                });
            });
        });

        // Add ripple effect to buttons
        document.querySelectorAll('.submit-button, .social-button').forEach(button => {
            button.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const ripple = document.createElement('div');
                ripple.style.position = 'absolute';
                ripple.style.width = '0';
                ripple.style.height = '0';
                ripple.style.background = 'rgba(255, 255, 255, 0.4)';
                ripple.style.borderRadius = '50%';
                ripple.style.transform = 'translate(-50%, -50%)';
                ripple.style.left = `${x}px`;
                ripple.style.top = `${y}px`;
                ripple.style.animation = 'ripple 0.6s ease-out';

                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);

                setTimeout(() => ripple.remove(), 600);
            });
        });