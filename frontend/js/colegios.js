// ==============================================================================
// Script de Interactividad: Colegios Acompañados (Grid Responsivo)
// ==============================================================================

document.addEventListener("DOMContentLoaded", () => {
    // 1. Elementos del DOM
    const searchInput = document.getElementById("school-search");
    const provinciaPills = document.querySelectorAll("#filter-provincia .pill-btn");
    const carismaPills = document.querySelectorAll("#filter-carisma .pill-btn");
    const resultsCountEl = document.getElementById("results-count");
    const schoolCards = document.querySelectorAll(".school-card");
    const emptyState = document.getElementById("empty-state");
    const btnResetFilters = document.getElementById("btn-reset-filters");

    // Variables de estado activas
    let activeProvincia = "all";
    let activeCarisma = "all";
    let activeSearch = "";

    // 2. Lógica de Filtrado y Búsqueda combinada
    function filterSchools() {
        let visibleCount = 0;
        const searchNormalized = activeSearch.toLowerCase().trim();

        schoolCards.forEach(card => {
            const itemProvincia = card.getAttribute("data-provincia");
            const itemCarisma = card.getAttribute("data-carisma");
            const itemNombre = card.getAttribute("data-nombre");
            const itemCongregacion = card.getAttribute("data-congregacion");

            // Validar filtros
            const matchesProvincia = (activeProvincia === "all" || itemProvincia === activeProvincia);
            const matchesCarisma = (activeCarisma === "all" || itemCarisma.includes(activeCarisma));
            
            // Validar buscador
            const matchesSearch = (searchNormalized === "" || 
                                   itemNombre.includes(searchNormalized) || 
                                   itemCongregacion.includes(searchNormalized) ||
                                   itemProvincia.toLowerCase().includes(searchNormalized));

            const isVisible = matchesProvincia && matchesCarisma && matchesSearch;

            // Mostrar/Ocultar tarjeta con transiciones
            if (isVisible) {
                card.classList.remove("d-none");
                // Forzar re-trigger de animación fade-in
                card.style.animation = 'none';
                card.offsetHeight; /* trigger reflow */
                card.style.animation = null; 
                visibleCount++;
            } else {
                card.classList.add("d-none");
            }
        });

        // Actualizar contador
        resultsCountEl.textContent = visibleCount;

        // Gestionar estado vacío
        if (visibleCount === 0) {
            emptyState.classList.remove("d-none");
        } else {
            emptyState.classList.add("d-none");
        }
    }

    // 3. Escuchar eventos del Buscador
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            activeSearch = e.target.value;
            filterSchools();
        });
    }

    // 4. Clic en Pills de Provincia
    provinciaPills.forEach(pill => {
        pill.addEventListener("click", () => {
            provinciaPills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
            activeProvincia = pill.getAttribute("data-provincia");
            filterSchools();
        });
    });

    // 5. Clic en Pills de Carisma
    carismaPills.forEach(pill => {
        pill.addEventListener("click", () => {
            carismaPills.forEach(c => c.classList.remove("active"));
            pill.classList.add("active");
            activeCarisma = pill.getAttribute("data-carisma");
            filterSchools();
        });
    });

    // 6. Botón de restablecer filtros
    if (btnResetFilters) {
        btnResetFilters.addEventListener("click", () => {
            if (searchInput) searchInput.value = "";
            activeSearch = "";
            
            provinciaPills.forEach(p => p.classList.remove("active"));
            const defaultProv = document.querySelector("#filter-provincia .pill-btn[data-provincia='all']");
            if (defaultProv) defaultProv.classList.add("active");
            activeProvincia = "all";

            carismaPills.forEach(c => c.classList.remove("active"));
            const defaultCar = document.querySelector("#filter-carisma .pill-btn[data-carisma='all']");
            if (defaultCar) defaultCar.classList.add("active");
            activeCarisma = "all";

            filterSchools();
        });
    }
});
