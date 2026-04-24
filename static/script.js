/**
 * TrackIT – Client-side JavaScript
 * ==================================
 * Handles sidebar toggle, mobile menu, form validation, and flash
 * message auto-dismiss.
 */

document.addEventListener("DOMContentLoaded", () => {
    // ── Sidebar Toggle (Mobile) ─────────────────────────────────────────
    const sidebar      = document.getElementById("sidebar");
    const overlay      = document.getElementById("sidebarOverlay");
    const mobileBtn    = document.getElementById("mobileMenuBtn");

    function openSidebar() {
        if (sidebar) sidebar.classList.add("open");
        if (overlay) overlay.classList.add("show");
        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
        if (sidebar) sidebar.classList.remove("open");
        if (overlay) overlay.classList.remove("show");
        document.body.style.overflow = "";
    }

    if (mobileBtn) mobileBtn.addEventListener("click", openSidebar);
    if (overlay)   overlay.addEventListener("click", closeSidebar);

    // Close sidebar on Escape key
    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeSidebar();
    });

    // ── Flash Auto-Dismiss ──────────────────────────────────────────────
    document.querySelectorAll(".flash").forEach((flash) => {
        setTimeout(() => {
            flash.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            flash.style.opacity = "0";
            flash.style.transform = "translateY(-10px)";
            setTimeout(() => flash.remove(), 400);
        }, 5000);
    });

    // ── Client-Side Form Validation ─────────────────────────────────────
    const forms = document.querySelectorAll("#createTicketForm, #editTicketForm, #loginForm");

    forms.forEach((form) => {
        form.addEventListener("submit", (e) => {
            let hasError = false;

            // Clear previous validation styles
            form.querySelectorAll(".form-input, .input-wrapper input").forEach((input) => {
                input.style.borderColor = "";
            });

            // Validate required fields
            form.querySelectorAll("[required]").forEach((field) => {
                const value = field.value.trim();
                if (!value) {
                    hasError = true;
                    field.style.borderColor = "var(--color-error)";
                    field.style.boxShadow = "0 0 0 3px rgba(239,68,68,0.15)";

                    // Shake animation
                    field.classList.add("shake");
                    setTimeout(() => field.classList.remove("shake"), 500);
                }
            });

            if (hasError) {
                e.preventDefault();

                // Focus the first invalid field
                const firstInvalid = form.querySelector("[required]");
                if (firstInvalid) firstInvalid.focus();
            }
        });

        // Clear error styles on input
        form.querySelectorAll("[required]").forEach((field) => {
            field.addEventListener("input", () => {
                if (field.value.trim()) {
                    field.style.borderColor = "";
                    field.style.boxShadow = "";
                }
            });
        });
    });

    // ── Add shake animation CSS dynamically ─────────────────────────────
    if (!document.getElementById("shakeStyle")) {
        const style = document.createElement("style");
        style.id = "shakeStyle";
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                20%      { transform: translateX(-6px); }
                40%      { transform: translateX(6px); }
                60%      { transform: translateX(-4px); }
                80%      { transform: translateX(4px); }
            }
            .shake { animation: shake 0.4s ease; }
        `;
        document.head.appendChild(style);
    }

    // ── Animate stat card numbers on Dashboard ──────────────────────────
    document.querySelectorAll(".stat-value").forEach((el) => {
        const target = parseInt(el.textContent, 10);
        if (isNaN(target) || target === 0) return;

        el.textContent = "0";
        const duration = 600; // ms
        const start    = performance.now();

        function step(now) {
            const progress = Math.min((now - start) / duration, 1);
            // Ease-out quadratic
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(eased * target);
            if (progress < 1) requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    });

    // ── 3D Tilt & Interactive Effects for Login Page ─────────────────────
    const loginBrand = document.querySelector('.login-brand');
    const loginBrandContent = document.querySelector('.login-brand-content');
    
    if (loginBrand && loginBrandContent) {
        // Parallax depth effect on mousemove
        loginBrand.addEventListener('mousemove', (e) => {
            const rect = loginBrand.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const percentX = (x - centerX) / centerX;
            const percentY = (y - centerY) / centerY;
            
            // Max rotation of 4 degrees
            const rotateX = percentY * -4;
            const rotateY = percentX * 4;
            
            loginBrandContent.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            loginBrandContent.style.transition = 'transform 0.1s ease-out';
        });
        
        // Reset on leave
        loginBrand.addEventListener('mouseleave', () => {
            loginBrandContent.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg)';
            loginBrandContent.style.transition = 'transform 0.5s ease-out';
        });

        // Feature hover micro-animations
        const features = document.querySelectorAll('.login-feature');
        features.forEach(feature => {
            feature.style.cursor = 'default';
            feature.addEventListener('mouseenter', () => {
                const icon = feature.querySelector('i, svg');
                if(icon) {
                    icon.style.transform = 'scale(1.25) translateY(-2px)';
                    icon.style.color = 'var(--accent-hover)';
                    icon.style.transition = 'all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                }
            });
            feature.addEventListener('mouseleave', () => {
                const icon = feature.querySelector('i, svg');
                if(icon) {
                    icon.style.transform = 'scale(1) translateY(0)';
                    icon.style.color = 'var(--accent)';
                }
            });
        });
    }

    // ── Re-initialize Lucide icons (for dynamically loaded content) ─────
    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }
});
