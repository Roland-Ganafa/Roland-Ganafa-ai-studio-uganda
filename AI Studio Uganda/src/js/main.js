import '../styles/global.css';

// Global specific logic
document.addEventListener('DOMContentLoaded', () => {
    setupAnimations();
    highlightActiveLink();
    highlightActiveLink();
});

function setupAnimations() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

function highlightActiveLink() {
    const path = window.location.pathname;
    // Normalize path (handle trailing slash or index.html)
    const cleanPath = path.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';

    const links = document.querySelectorAll('.nav-link');
    links.forEach(link => {
        const href = link.getAttribute('href');
        const cleanHref = href.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';

        // Exact match or subpath match for some things?
        // Doing exact for now.
        if (cleanPath === cleanHref) {
            link.classList.add('active');
        }

        // Special case for root
        if (cleanPath === '/' && cleanHref === '/') {
            link.classList.add('active');
        }
    });
}
