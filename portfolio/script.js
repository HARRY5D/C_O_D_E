// script.js
AOS.init({
    duration: 1000,
    once: true
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add animation to skills on scroll
const skillCategories = document.querySelectorAll('.skill-category');
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = 1;
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.5 });

skillCategories.forEach(category => {
    category.style.opacity = 0;
    category.style.transform = 'translateY(20px)';
    observer.observe(category);
});

// Contact form handler with Web3Forms
document.getElementById('contactForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formStatus = document.getElementById('formStatus');
    const submitBtn = this.querySelector('.submit-btn');
    const form = this;
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';
    formStatus.style.display = 'block';
    
    try {
        // Send to Web3Forms
        const formData = new FormData(form);
        const response = await fetch('https://api.web3forms.com/submit', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            formStatus.textContent = "Message sent successfully! I'll get back to you soon.";
            formStatus.className = 'success';
            form.reset();
        } else {
            throw new Error(data.message || 'Failed to send message');
        }
    } catch (error) {
        formStatus.textContent = 'Failed to send message. Please email me directly at harnishdpatel@gmail.com';
        formStatus.className = 'error';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
        
        // Hide status after 5 seconds
        setTimeout(() => {
            formStatus.style.display = 'none';
        }, 5000);
    }
});
