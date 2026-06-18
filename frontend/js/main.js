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
});
