// Interactividad básica para la navegación
document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.getElementById("nav-toggle");
    const mainNav = document.getElementById("main-nav");

    if (navToggle && mainNav) {
        navToggle.addEventListener("click", () => {
            const isOpen = mainNav.classList.toggle("open");
            navToggle.setAttribute("aria-expanded", isOpen);
        });
    }
});
