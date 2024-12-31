// Function to update error state
        function updateErrorState(type, title, message) {
            const header = document.querySelector('.error-header');
            const errorMessage = document.querySelector('.error-message');
            const icon = document.querySelector('.error-icon i');

            // Reset classes
            header.className = 'error-header';
            errorMessage.className = 'error-message';

            // Update classes and content based on type
            switch(type) {
                case 'warning':
                    header.classList.add('warning');
                    errorMessage.classList.add('warning');
                    icon.className = 'fas fa-exclamation-triangle';
                    break;
                case 'info':
                    header.classList.add('info');
                    errorMessage.classList.add('info');
                    icon.className = 'fas fa-info-circle';
                    break;
                case 'success':
                    header.classList.add('success');
                    errorMessage.classList.add('success');
                    icon.className = 'fas fa-check-circle';
                    break;
                default:
                    icon.className = 'fas fa-exclamation-circle';
            }

            // Update text content
            document.querySelector('.error-title').textContent = title;
            errorMessage.textContent = message;
        }

        // Event handler for buttons
        document.querySelectorAll('.error-button').forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });

            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });

        // Example usage:
       // updateErrorState('warning', 'Warning', 'Session expired. Please log in again.');
       // updateErrorState('info', 'Information', 'System maintenance scheduled.');
       // updateErrorState('success', 'Success', 'Action completed successfully.');