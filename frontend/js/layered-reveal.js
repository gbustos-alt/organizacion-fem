/**
 * Motor Layered Reveal v12 - Fundación FEM
 * Manejo de escenas full-height con transiciones de contenido serenas, desvanecidos suaves (fade in/out),
 * puntero lateral sutil con línea y puntos amarillos, y scroll nativo fluido de alta respuesta.
 */
document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".lr-container") || document.body;
    const layerItems = Array.from(document.querySelectorAll("[data-layer-item]"));
    const navDots = Array.from(document.querySelectorAll("[data-nav-dot]"));
    const progressFill = document.getElementById("lr-progress-fill");

    if (!layerItems.length) return;

    let currentActiveIndex = 0;

    // Detección de dirección de Scroll para animaciones contextuales
    let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;

    window.addEventListener("scroll", () => {
        const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        if (currentScrollTop > lastScrollTop + 4) {
            container.setAttribute("data-scroll-dir", "down");
        } else if (currentScrollTop < lastScrollTop - 4) {
            container.setAttribute("data-scroll-dir", "up");
        }
        lastScrollTop = currentScrollTop <= 0 ? 0 : currentScrollTop;
    }, { passive: true });

    // Respeto estricto a las preferencias de reducción de movimiento
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
        layerItems.forEach(item => {
            item.classList.add("is-active");
            item.classList.remove("is-before", "is-after", "is-near");
        });
        return;
    }

    // Actualización serena de estados de sección y widget de navegación
    const updateActiveLayer = (activeIndex) => {
        if (currentActiveIndex === activeIndex && layerItems[activeIndex].classList.contains("is-active")) return;
        const scrollDir = container.getAttribute("data-scroll-dir") || "down";
        currentActiveIndex = activeIndex;

        layerItems.forEach((item, index) => {
            item.classList.remove("is-active", "is-entering", "is-exiting", "is-before", "is-after");

            if (index === activeIndex) {
                item.classList.add("is-active");
            } else if (index < activeIndex) {
                item.classList.add("is-before");
                if (index === activeIndex - 1 && scrollDir === "down") {
                    item.classList.add("is-exiting");
                }
            } else {
                item.classList.add("is-after");
                if (index === activeIndex + 1 && scrollDir === "up") {
                    item.classList.add("is-entering");
                }
            }
        });

        // Actualizar atributo data-active-scene en el contenedor
        const activeSceneNum = layerItems[activeIndex].getAttribute("data-scene-num") || `00${activeIndex + 1}`;
        container.setAttribute("data-active-scene", activeSceneNum);

        // Actualizar puntos de navegación de progreso lateral
        navDots.forEach((dot, index) => {
            if (index === activeIndex) {
                dot.classList.add("is-active");
                dot.setAttribute("aria-selected", "true");
            } else {
                dot.classList.remove("is-active");
                dot.setAttribute("aria-selected", "false");
            }
        });

        // Actualizar línea de progreso de scroll
        if (progressFill && layerItems.length > 1) {
            const fillPercentage = (activeIndex / (layerItems.length - 1)) * 100;
            progressFill.style.height = `${fillPercentage}%`;
        }
    };

    // Observador de Intersección de alta precisión para Snap-Layered Narrative
    const isMobileScreen = window.innerWidth < 767;
    const observerOptions = {
        root: null,
        rootMargin: isMobileScreen ? "-5% 0px -5% 0px" : "-10% 0px -10% 0px",
        threshold: isMobileScreen ? [0.15, 0.45, 0.75] : [0.2, 0.5, 0.8]
    };

    let visibleRatios = new Map();

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                visibleRatios.set(entry.target, entry.intersectionRatio);
            } else {
                visibleRatios.delete(entry.target);
            }
        });

        let maxRatio = 0;
        let activeElement = null;

        visibleRatios.forEach((ratio, target) => {
            if (ratio > maxRatio) {
                maxRatio = ratio;
                activeElement = target;
            }
        });

        if (activeElement) {
            const activeIndex = layerItems.indexOf(activeElement);
            if (activeIndex !== -1) {
                updateActiveLayer(activeIndex);
            }
        }
    }, observerOptions);

    layerItems.forEach(item => observer.observe(item));

    // Navegación interactiva por click en los puntos de progreso lateral
    navDots.forEach(dot => {
        dot.addEventListener("click", () => {
            const targetId = dot.getAttribute("data-target-id");
            if (!targetId) return;

            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Navegación accesible por teclado (Flechas Arriba / Abajo)
    window.addEventListener("keydown", (e) => {
        if (e.key === "ArrowDown" || e.key === "PageDown") {
            if (currentActiveIndex < layerItems.length - 1) {
                e.preventDefault();
                layerItems[currentActiveIndex + 1].scrollIntoView({ behavior: "smooth" });
            }
        } else if (e.key === "ArrowUp" || e.key === "PageUp") {
            if (currentActiveIndex > 0) {
                e.preventDefault();
                layerItems[currentActiveIndex - 1].scrollIntoView({ behavior: "smooth" });
            }
        }
    });

    // ==========================================================================
    // CARRO ESCÉNICO INMERSIVO MÓVIL
    // ==========================================================================
    if (isMobileScreen) {
        const carousels = document.querySelectorAll("[data-scenic-carousel]");

        carousels.forEach(carousel => {
            const carouselId = carousel.getAttribute("data-scenic-carousel");
            const cards = Array.from(carousel.children);
            const indicatorContainer = document.querySelector(`[data-carousel-indicators="${carouselId}"]`);
            const dots = indicatorContainer ? Array.from(indicatorContainer.children) : [];
            const bgImg = document.getElementById(`bg-${carouselId}`);

            if (!cards.length) return;

            carousel.addEventListener("scroll", () => {
                const scrollLeft = carousel.scrollLeft;
                const cardWidth = cards[0].offsetWidth;
                const activeCardIndex = Math.round(scrollLeft / (cardWidth + 12));

                dots.forEach((dot, i) => {
                    if (i === activeCardIndex) {
                        dot.classList.add("is-active");
                    } else {
                        dot.classList.remove("is-active");
                    }
                });

                if (bgImg && cards[activeCardIndex]) {
                    const newBg = cards[activeCardIndex].getAttribute("data-bg-mobile");
                    if (newBg && bgImg.getAttribute("src") !== newBg) {
                        bgImg.style.opacity = "0.3";
                        setTimeout(() => {
                            bgImg.setAttribute("src", newBg);
                            bgImg.style.opacity = "1";
                        }, 200);
                    }
                }
            }, { passive: true });
        });
    }
});
