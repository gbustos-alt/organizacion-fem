// Interactividad para Navegación Móvil (Drawer & Acordeones)
document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.getElementById("nav-toggle");
    const mainNav = document.getElementById("main-nav");
    const drawerClose = document.getElementById("drawer-close");
    const drawerOverlay = document.getElementById("drawer-overlay");

    // Función para abrir/cerrar el Drawer
    const toggleMenu = () => {
        const isOpen = mainNav.classList.toggle("open");
        navToggle.classList.toggle("active");
        navToggle.setAttribute("aria-expanded", isOpen);
        document.body.style.overflow = isOpen ? "hidden" : ""; // Evita scroll de fondo
    };

    if (navToggle && mainNav) {
        navToggle.addEventListener("click", toggleMenu);
    }

    if (drawerClose) {
        drawerClose.addEventListener("click", toggleMenu);
    }

    if (drawerOverlay) {
        drawerOverlay.addEventListener("click", toggleMenu);
    }

    // Manejo de Submenús en Acordeón para versión Mobile (Táctil)
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle");
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener("click", (e) => {
            // Solo actuar en pantallas móviles
            if (window.innerWidth <= 767) {
                e.preventDefault(); // Evitar navegación si es un link dummy
                
                const dropdownMenu = toggle.nextElementSibling;
                const arrow = toggle.querySelector(".arrow-down");
                
                if (dropdownMenu) {
                    const isOpen = dropdownMenu.classList.toggle("open");
                    
                    // Rotar flechita suavemente
                    if (arrow) {
                        arrow.style.transform = isOpen ? "rotate(180deg)" : "";
                    }
                }
            }
        });
    });

    // --- Slider del Hero ("Estilo Netflix") ---
    const slider = document.getElementById("hero-slider");
    if (slider) {
        const slides = slider.querySelectorAll(".hero-slide");
        const indicators = slider.querySelectorAll(".indicator");
        const prevBtn = document.getElementById("slider-prev");
        const nextBtn = document.getElementById("slider-next");
        let currentIndex = 0;
        let timer = null;

        const showSlide = (index) => {
            slides[currentIndex].classList.remove("active");
            indicators[currentIndex].classList.remove("active");
            
            currentIndex = (index + slides.length) % slides.length;
            
            slides[currentIndex].classList.add("active");
            indicators[currentIndex].classList.add("active");
        };

        const nextSlide = () => {
            showSlide(currentIndex + 1);
        };

        const prevSlide = () => {
            showSlide(currentIndex - 1);
        };

        const startTimer = () => {
            stopTimer();
            timer = setInterval(nextSlide, 5000);
        };

        const stopTimer = () => {
            if (timer) clearInterval(timer);
        };

        if (nextBtn) {
            nextBtn.addEventListener("click", () => {
                nextSlide();
                startTimer();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener("click", () => {
                prevSlide();
                startTimer();
            });
        }

        indicators.forEach((indicator) => {
            indicator.addEventListener("click", () => {
                const index = parseInt(indicator.getAttribute("data-index"), 10);
                showSlide(index);
                startTimer();
            });
        });

        // Pausa al pasar el mouse por encima
        slider.addEventListener("mouseenter", stopTimer);
        slider.addEventListener("mouseleave", startTimer);

        // Inicio inicial
        startTimer();
    }

    // --- Lógica de Drag & Drop para la Bolsa de Trabajo ---
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("cv");
    const promptEl = document.getElementById("drop-zone-prompt");
    const filenameEl = document.getElementById("drop-zone-filename");
    const filenameText = document.getElementById("file-name-text");

    if (dropZone && fileInput) {
        // Detectar cambios en la selección de archivos
        fileInput.addEventListener("change", () => {
            if (fileInput.files.length > 0) {
                const file = fileInput.files[0];
                filenameText.textContent = `${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
                promptEl.style.display = "none";
                filenameEl.style.display = "block";
                dropZone.style.borderColor = "var(--color-primary)";
                dropZone.style.backgroundColor = "rgba(12, 30, 54, 0.02)";
            } else {
                promptEl.style.display = "block";
                filenameEl.style.display = "none";
                dropZone.style.borderColor = "var(--color-border)";
                dropZone.style.backgroundColor = "var(--color-bg-alt)";
            }
        });

        // Estilos interactivos al arrastrar archivos encima
        ["dragenter", "dragover"].forEach(eventName => {
            fileInput.addEventListener(eventName, () => {
                dropZone.style.borderColor = "var(--color-coral)";
                dropZone.style.backgroundColor = "rgba(241, 101, 54, 0.05)";
            });
        });

        ["dragleave", "drop"].forEach(eventName => {
            fileInput.addEventListener(eventName, () => {
                if (fileInput.files.length > 0) {
                    dropZone.style.borderColor = "var(--color-primary)";
                    dropZone.style.backgroundColor = "rgba(12, 30, 54, 0.02)";
                } else {
                    dropZone.style.borderColor = "var(--color-border)";
                    dropZone.style.backgroundColor = "var(--color-bg-alt)";
                }
            });
        });
    }

    // --- Animación Smooth por Scroll para la Sección Misión / Identidad ---
    const identitySection = document.querySelector(".home-identity-section");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (identitySection && !prefersReducedMotion && "IntersectionObserver" in window) {
        // Habilita el estado preparado para la animación inicial
        identitySection.classList.add("js-motion-ready");

        const identityObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    identitySection.classList.add("is-visible");
                }
            });
        }, {
            threshold: 0.15,
            rootMargin: "0px 0px -50px 0px"
        });

        identityObserver.observe(identitySection);
    }
});

