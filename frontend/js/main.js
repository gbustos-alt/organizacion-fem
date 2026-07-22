// Motor de Animación e Interactividad Global - Fundación FEM (Todas las Páginas)
document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.getElementById("nav-toggle");
    const mainNav = document.getElementById("main-nav");
    const drawerClose = document.getElementById("drawer-close");
    const drawerOverlay = document.getElementById("drawer-overlay");

    // Función para abrir/cerrar el Drawer en Mobile
    const toggleMenu = () => {
        const isOpen = mainNav.classList.toggle("open");
        navToggle.classList.toggle("active");
        navToggle.setAttribute("aria-expanded", isOpen);
        document.body.style.overflow = isOpen ? "hidden" : "";
    };

    if (navToggle && mainNav) navToggle.addEventListener("click", toggleMenu);
    if (drawerClose) drawerClose.addEventListener("click", toggleMenu);
    if (drawerOverlay) drawerOverlay.addEventListener("click", toggleMenu);

    // Manejo de Submenús en Acordeón para versión Mobile
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle");
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener("click", (e) => {
            if (window.innerWidth <= 767) {
                e.preventDefault();
                const dropdownMenu = toggle.nextElementSibling;
                const arrow = toggle.querySelector(".arrow-down");
                if (dropdownMenu) {
                    const isOpen = dropdownMenu.classList.toggle("open");
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

        const nextSlide = () => showSlide(currentIndex + 1);
        const prevSlide = () => showSlide(currentIndex - 1);

        const startTimer = () => {
            stopTimer();
            timer = setInterval(nextSlide, 5000);
        };

        const stopTimer = () => {
            if (timer) clearInterval(timer);
        };

        if (nextBtn) nextBtn.addEventListener("click", () => { nextSlide(); startTimer(); });
        if (prevBtn) prevBtn.addEventListener("click", () => { prevSlide(); startTimer(); });

        indicators.forEach((indicator) => {
            indicator.addEventListener("click", () => {
                const index = parseInt(indicator.getAttribute("data-index"), 10);
                showSlide(index);
                startTimer();
            });
        });

        // Soporte de Gestos Táctiles (Swipe Left / Swipe Right)
        let touchStartX = 0;
        let touchEndX = 0;

        slider.addEventListener("touchstart", (e) => {
            touchStartX = e.changedTouches[0].screenX;
            stopTimer();
        }, { passive: true });

        slider.addEventListener("touchend", (e) => {
            touchEndX = e.changedTouches[0].screenX;
            const diffX = touchStartX - touchEndX;
            if (Math.abs(diffX) > 40) {
                if (diffX > 0) {
                    nextSlide();
                } else {
                    prevSlide();
                }
            }
            startTimer();
        }, { passive: true });

        slider.addEventListener("mouseenter", stopTimer);
        slider.addEventListener("mouseleave", startTimer);
        startTimer();
    }


    // --- Lógica de Drag & Drop para la Bolsa de Trabajo ---
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("cv");
    const promptEl = document.getElementById("drop-zone-prompt");
    const filenameEl = document.getElementById("drop-zone-filename");
    const filenameText = document.getElementById("file-name-text");

    if (dropZone && fileInput) {
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

    // --- Animación Sección Números FEM: Conteo Regresivo ---
    const numerosSection = document.querySelector(".numeros-fem-section");
    const numCounters = document.querySelectorAll(".num-counter");

    if (numerosSection && "IntersectionObserver" in window) {
        numerosSection.classList.add("js-motion-ready");

        const runCountdown = (el, staggerDelay) => {
            const targetStr = el.getAttribute("data-count-to");
            if (!targetStr) return;

            const cleanTarget = parseInt(targetStr.replace(/\./g, ""), 10);
            const hasDots = targetStr.includes(".");
            const startVal = Math.round(cleanTarget * 2.5);
            const duration = 2400;
            
            setTimeout(() => {
                const startTime = performance.now();
                const tick = (currentTime) => {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const easeOutProgress = 1 - Math.pow(1 - progress, 3);
                    const currentVal = Math.round(startVal - (startVal - cleanTarget) * easeOutProgress);

                    if (hasDots) {
                        el.textContent = currentVal.toLocaleString("es-AR");
                    } else {
                        el.textContent = currentVal;
                    }

                    if (progress < 1) {
                        requestAnimationFrame(tick);
                    } else {
                        el.textContent = targetStr;
                        el.classList.add("is-settled");
                    }
                };

                requestAnimationFrame(tick);
            }, staggerDelay);
        };

        const numerosObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    numerosSection.classList.add("is-visible");
                    numCounters.forEach((el, index) => {
                        runCountdown(el, index * 100);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        numerosObserver.observe(numerosSection);
    }

    // --- Header Fijo e Inteligente (Auto-Hide al Scroll Down, Show al Scroll Up) ---
    const mainHeader = document.querySelector(".main-header");
    if (mainHeader) {
        let lastScrollY = window.scrollY;
        const onHeaderScroll = () => {
            const currentScrollY = window.scrollY;
            const isScrollingDown = currentScrollY > lastScrollY && currentScrollY > 90;
            
            mainHeader.classList.toggle("scrolled", currentScrollY > 40);
            mainHeader.classList.toggle("header-hidden", isScrollingDown);
            
            lastScrollY = currentScrollY;
        };
        window.addEventListener("scroll", onHeaderScroll, { passive: true });
        onHeaderScroll();
    }

    // ==========================================================================
    // MOTOR DE REVELADO EN SCROLL UNIVERSAL PARA TODAS LAS PÁGINAS DEL SITIO
    // ==========================================================================

    (() => {
        // 1. Asignar entradas direccionales alternadas
        const leftGroups = document.querySelectorAll(
            '.identity-visual-block, .colegio-detail-left, ' +
            '.dimension-card:nth-child(odd), .mision-card:nth-child(odd), ' +
            '.editorial-block, .grid-split-2 > div:first-child'
        );
        const rightGroups = document.querySelectorAll(
            '.identity-text-block, .colegio-detail-right, ' +
            '.dimension-card:nth-child(even), .mision-card:nth-child(even), ' +
            '.text-block-accent, .grid-split-2 > div:last-child'
        );

        leftGroups.forEach(el => el.classList.add('reveal-left'));
        rightGroups.forEach(el => el.classList.add('reveal-right'));

        // 2. Cobertura exhaustiva de elementos para todas las páginas
        const targets = document.querySelectorAll(
            '.sec-head, .cifras-header, .card, .dimension-card, .news-card, .recursero-card, ' +
            '.quick-access-card, .team-member-card, .colegio-card-item, .school-card, .num-counter-box, ' +
            '.quienes-somos-card, .contact-info-card, .contact-form-card, .contact-form, .memory-card, ' +
            '.material-card, .hito-item, .member-card, .org-section, .editorial-block, .text-block-accent, ' +
            '.mission-card, .province-title, blockquote, .reveal-left, .reveal-right, .reveal-scale, ' +
            '.rasgo-card, .strategy-card, .branch-card, .memoria-row, .recursero-card-mockup, ' +
            '.contact-item, .contact-info-list, .cifra-card, .section-header'
        );


        if (!('IntersectionObserver' in window)) {
            targets.forEach(t => t.classList.add('is-visible'));
            return;
        }

        // 3. Aplicar clase base .reveal y retardo en cascada alternado
        targets.forEach((t, i) => {
            if (!t.classList.contains('reveal-left') &&
                !t.classList.contains('reveal-right') &&
                !t.classList.contains('reveal-scale')) {
                t.classList.add('reveal');
            }
            t.style.transitionDelay = `${(i % 4) * 80}ms`;
        });

        // 4. Observador de Intersección de Alto Rendimiento
        const io = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('is-visible');
                    io.unobserve(e.target);
                }
            });
        }, {
            threshold: 0.05,
            rootMargin: '0px 0px -2% 0px'
        });

        targets.forEach(t => io.observe(t));
    })();

    // --- SPOTLIGHT CURSOR GLOW EN TARJETAS ---
    (() => {
        const spotlightCards = document.querySelectorAll(
            ".card, .dimension-card, .news-card, .recursero-card, .quick-access-card, " +
            ".colegio-card-item, .school-card, .team-member-card, .member-card, .num-counter-box, " +
            ".contact-info-card, .contact-form, .memory-card, .material-card, .mission-card"
        );
        spotlightCards.forEach(card => {
            card.classList.add("card-spotlight");
            card.addEventListener("pointermove", (e) => {
                const rect = card.getBoundingClientRect();
                card.style.setProperty("--mx", `${e.clientX - rect.left}px`);
                card.style.setProperty("--my", `${e.clientY - rect.top}px`);
            });
        });
    })();

    // --- BOTONES MAGNÉTICOS ---
    (() => {
        const magneticBtns = document.querySelectorAll(
            ".btn-magnetic, .btn-primary, .btn-accent, .btn-coral, .btn-hero, .btn"
        );
        magneticBtns.forEach(btn => {
            btn.addEventListener("pointermove", (e) => {
                const rect = btn.getBoundingClientRect();
                const x = (e.clientX - rect.left - rect.width / 2) * 0.20;
                const y = (e.clientY - rect.top - rect.height / 2) * 0.28;
                btn.style.transform = `translate(${x}px, ${y - 2}px)`;
            });
            btn.addEventListener("pointerleave", () => {
                btn.style.transform = "";
            });
        });
    })();
});
