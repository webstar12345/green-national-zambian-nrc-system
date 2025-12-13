// Zambian NRC System - Animation and Interaction Scripts

document.addEventListener('DOMContentLoaded', function() {
    
    // Scroll animations disabled - all content visible immediately
    // Make sure all elements with animation classes are visible
    const animatedElements = document.querySelectorAll(
        '.fade-in-scroll, .slide-in-left, .slide-in-right, .scale-up'
    );
    
    animatedElements.forEach(element => {
        element.classList.add('visible');
        element.classList.remove('animate-on-scroll');
        // Ensure full visibility
        element.style.opacity = '1';
        element.style.transform = 'none';
    });

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Add hover effect to cards
    const cards = document.querySelectorAll('.bg-white.rounded-lg, .card');
    cards.forEach(card => {
        card.classList.add('card-hover');
    });

    // Add hover effect to buttons
    const hoverButtons = document.querySelectorAll('button, .btn, a.bg-zambian-green, a.bg-zambian-orange');
    hoverButtons.forEach(btn => {
        btn.classList.add('btn-hover');
    });

    // Add hover effect to links
    const links = document.querySelectorAll('a:not(.btn):not(button)');
    links.forEach(link => {
        if (!link.classList.contains('no-hover')) {
            link.classList.add('link-hover');
        }
    });

    // Add focus effect to inputs
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.classList.add('input-focus');
    });

    // Add hover effect to table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.classList.add('table-row-hover');
    });

    // Statistics animation disabled
    // Numbers display immediately without counting animation

    // Stagger animation disabled
    // All list items are visible immediately

    // Add icon bounce effect
    const icons = document.querySelectorAll('i.fas, i.far');
    icons.forEach(icon => {
        icon.classList.add('icon-bounce');
    });

    // Page transition effect
    document.body.classList.add('page-transition');

    // Form validation with shake effect
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasError = false;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    hasError = true;
                    field.classList.add('shake');
                    field.style.borderColor = '#DE2910';
                    
                    setTimeout(() => {
                        field.classList.remove('shake');
                    }, 500);
                }
            });
            
            if (hasError) {
                e.preventDefault();
            }
        });
    });

    // Add glow effect to important buttons
    const importantButtons = document.querySelectorAll('.bg-zambian-green, .bg-zambian-orange');
    importantButtons.forEach(btn => {
        btn.classList.add('glow-effect');
    });

    // Subtle parallax effect for hero sections (disabled by default for better performance)
    // Uncomment if you want parallax effect
    /*
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                const scrolled = window.pageYOffset;
                const parallaxElements = document.querySelectorAll('.parallax-enabled');
                
                parallaxElements.forEach(element => {
                    const speed = 0.2; // Reduced speed for subtlety
                    element.style.transform = `translateY(${scrolled * speed}px)`;
                });
                ticking = false;
            });
            ticking = true;
        }
    });
    */

    // Add loading animation to images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
        
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        // If image is already loaded
        if (img.complete) {
            img.style.opacity = '1';
        }
    });

    // Notification animations
    const notifications = document.querySelectorAll('.alert, [class*="bg-green-100"], [class*="bg-red-100"], [class*="bg-blue-100"]');
    notifications.forEach(notification => {
        notification.classList.add('notification-slide');
    });

    // Floating animation disabled
    // Icons remain static

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Add progress bar animation to status indicators
    const progressBars = document.querySelectorAll('[role="progressbar"]');
    progressBars.forEach(bar => {
        bar.classList.add('progress-animate');
    });

    // Tooltip animations
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Gradient animation disabled
    // Gradients remain static

    console.log('🇿🇲 Zambian NRC System animations loaded successfully!');
});

// Ripple effect styles
const style = document.createElement('style');
style.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);


// NRC Carousel Functionality with Sliding Effect
let currentSlide = 0;
let carouselInterval;
let isAnimating = false;

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.carousel-indicator');
    
    if (!slides.length || isAnimating) return;
    
    // Wrap around
    if (index >= slides.length) currentSlide = 0;
    else if (index < 0) currentSlide = slides.length - 1;
    else currentSlide = index;
    
    isAnimating = true;
    
    // Slide all slides
    slides.forEach((slide, i) => {
        slide.style.transition = 'transform 0.6s ease-in-out';
        const offset = (i - currentSlide) * 100;
        slide.style.transform = `translateX(${offset}%)`;
        
        // Update active class
        if (i === currentSlide) {
            slide.classList.add('active');
        } else {
            slide.classList.remove('active');
        }
    });
    
    // Update indicators
    indicators.forEach((indicator, i) => {
        if (i === currentSlide) {
            indicator.style.opacity = '1';
            indicator.style.transform = 'scale(1.2)';
        } else {
            indicator.style.opacity = '0.5';
            indicator.style.transform = 'scale(1)';
        }
    });
    
    // Reset animation lock after transition
    setTimeout(() => {
        isAnimating = false;
    }, 600);
}

function nextSlide() {
    showSlide(currentSlide + 1);
    resetCarouselInterval();
}

function previousSlide() {
    showSlide(currentSlide - 1);
    resetCarouselInterval();
}

function goToSlide(index) {
    showSlide(index);
    resetCarouselInterval();
}

function resetCarouselInterval() {
    clearInterval(carouselInterval);
    startCarouselAutoplay();
}

function startCarouselAutoplay() {
    carouselInterval = setInterval(() => {
        nextSlide();
    }, 5000); // Change slide every 5 seconds
}

// Initialize carousel when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.getElementById('nrcCarousel');
    if (carousel) {
        showSlide(0);
        startCarouselAutoplay();
        
        // Pause autoplay on hover
        carousel.addEventListener('mouseenter', () => {
            clearInterval(carouselInterval);
        });
        
        carousel.addEventListener('mouseleave', () => {
            startCarouselAutoplay();
        });
    }
});

// Keyboard navigation for carousel
document.addEventListener('keydown', function(e) {
    const carousel = document.getElementById('nrcCarousel');
    if (!carousel) return;
    
    if (e.key === 'ArrowLeft') {
        previousSlide();
    } else if (e.key === 'ArrowRight') {
        nextSlide();
    }
});
