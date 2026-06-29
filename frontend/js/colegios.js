// ==============================================================================
// Script de Interactividad: Colegios Acompañados (Mapas Duales y Tarjeta Flotante)
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

    // Elementos de la Tarjeta Flotante
    const floatingCard = document.getElementById("map-floating-card");
    const floatingCardBody = document.getElementById("floating-card-body");
    const closeCardBtn = document.getElementById("close-floating-card");

    // Variables de estado activas
    let activeProvincia = "all";
    let activeCarisma = "all";
    let activeSearch = "";

    // 2. Coordenadas Geográficas de los 15 Colegios
    const coordsMap = {
        1: { lat: -34.557457, lng: -58.450162 }, // Santa Ana y San Joaquín
        2: { lat: -34.553974, lng: -58.448554 }, // Superior Santa Ana
        3: { lat: -34.662589, lng: -58.498877 }, // Plácido Marín
        4: { lat: -34.654876, lng: -58.495254 }, // San Pío X
        5: { lat: -34.662134, lng: -58.369324 }, // Dolores Rodríguez Sopeña
        6: { lat: -34.475456, lng: -58.528345 }, // Cardenal Spínola
        7: { lat: -34.093414, lng: -59.025345 }, // Colegio Sagrada Familia (Zárate)
        8: { lat: -34.093314, lng: -59.025245 }, // I.S.F.D. Sagrada Familia (offset)
        9: { lat: -34.921345, lng: -57.954678 }, // Colegio Sagrada Familia lp
        10: { lat: -34.757876, lng: -58.398654 }, // Instituto Nuestra Señora del Carmen
        11: { lat: -34.743245, lng: -58.389654 }, // Colegio San Juan de la Cruz
        12: { lat: -24.256876, lng: -65.212543 }, // Colegio Sagrado Corazón (Jujuy)
        13: { lat: -31.724567, lng: -61.102345 }, // Instituto Corazón de Jesús (Santa Fe)
        14: { lat: -26.812345, lng: -65.234567 }, // Colegio Montserrat (Tucumán)
        15: { lat: -33.054321, lng: -68.456789 }  // Colegio Nuestra Señora de la Compasión (Mendoza)
    };

    // 3. Inicializar Mapas Leaflet
    const defaultCenterArg = [-30.5, -63.5]; // Foco óptimo: Jujuy a Buenos Aires
    const defaultZoomArg = 5;
    
    const defaultCenterAmba = [-34.52, -58.55]; // Foco metropolitano
    const defaultZoomAmba = 9;

    const mapArgEl = document.getElementById("map-argentina");
    const mapAmbaEl = document.getElementById("map-amba");
    
    if (!mapArgEl || !mapAmbaEl) return;

    // Mapa 1: Presencia Nacional
    const mapArg = L.map("map-argentina", {
        scrollWheelZoom: false,
        minZoom: 3,
        maxZoom: 14
    }).setView(defaultCenterArg, defaultZoomArg);

    // Mapa 2: Detalle AMBA y Buenos Aires
    const mapAmba = L.map("map-amba", {
        scrollWheelZoom: false,
        minZoom: 7,
        maxZoom: 16
    }).setView(defaultCenterAmba, defaultZoomAmba);

    // Cargar capas CartoDB Positron en ambos mapas
    const tileUrl = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
    const tileAttrib = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>';

    L.tileLayer(tileUrl, { attribution: tileAttrib, subdomains: 'abcd', maxZoom: 20 }).addTo(mapArg);
    L.tileLayer(tileUrl, { attribution: tileAttrib, subdomains: 'abcd', maxZoom: 20 }).addTo(mapAmba);

    // Diccionarios para almacenar marcadores
    const markersArg = {};
    const markersAmba = {};

    // Obtener datos inyectados de los colegios
    const colegiosDataEl = document.getElementById("colegios-data");
    let colegiosList = [];
    if (colegiosDataEl) {
        try {
            colegiosList = JSON.parse(colegiosDataEl.textContent);
        } catch (e) {
            console.error("Error al parsear colegios-data:", e);
        }
    }

    // Función para mostrar la tarjeta flotante con info detallada
    function showFloatingCard(col) {
        if (!floatingCard || !floatingCardBody) return;

        const webButtonHtml = col.web_url ? `
            <a href="${col.web_url}" target="_blank" rel="noopener" class="btn btn-card-link">
                ${col.web_url.startsWith('mailto:') ? '✉️ Contactar por Email' : col.web_url.includes('instagram.com') ? '📷 Visitar Instagram' : '🌐 Visitar Sitio Web'}
            </a>
        ` : '';

        const phoneHtml = col.telefono ? `
            <div class="detail-item">
                <span class="detail-icon">📞</span>
                <span class="detail-text">${col.telefono}</span>
            </div>
        ` : '';

        const diocesisHtml = col.diocesis ? `
            <div class="detail-item">
                <span class="detail-icon">⛪</span>
                <span class="detail-text">${col.diocesis}</span>
            </div>
        ` : '';

        floatingCardBody.innerHTML = `
            <div class="popup-carisma">${col.congregacion}</div>
            <h5>${col.nombre}</h5>
            <span class="province-badge">${col.provincia}</span>
            <div class="detail-item">
                <span class="detail-icon">📍</span>
                <span class="detail-text">${col.ubicacion}</span>
            </div>
            ${phoneHtml}
            ${diocesisHtml}
            ${webButtonHtml}
        `;

        floatingCard.classList.remove("d-none");
    }

    // Función para cerrar la tarjeta flotante
    function closeFloatingCard() {
        if (floatingCard) {
            floatingCard.classList.add("d-none");
            floatingCard.classList.remove("on-left");
        }
        // Quitar clases activas
        document.querySelectorAll(".custom-marker").forEach(m => m.classList.remove("active"));
        schoolCards.forEach(c => c.classList.remove("active-card"));
    }

    if (closeCardBtn) {
        closeCardBtn.addEventListener("click", closeFloatingCard);
    }

    // Renderizar Pines en los Mapas
    colegiosList.forEach(col => {
        const coords = coordsMap[col.id];
        if (!coords) return;

        // Marcador 1: Mapa Nacional (Todos los Colegios)
        const iconArg = L.divIcon({
            className: `custom-marker marker-id-${col.id}`,
            html: `<div class="marker-pin"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });

        const markerArg = L.marker([coords.lat, coords.lng], { icon: iconArg }).addTo(mapArg);
        markersArg[col.id] = markerArg;

        // Marcador 2: Mapa AMBA (Solo CABA y Provincia de Buenos Aires)
        const isAmbaOrPba = col.provincia === "CABA" || col.provincia === "Provincia de Buenos Aires";
        if (isAmbaOrPba) {
            const iconAmba = L.divIcon({
                className: `custom-marker marker-id-${col.id}`,
                html: `<div class="marker-pin"></div>`,
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            });

            const markerAmba = L.marker([coords.lat, coords.lng], { icon: iconAmba }).addTo(mapAmba);
            markersAmba[col.id] = markerAmba;

            // Vincular Clic en Mapa AMBA
            markerAmba.on("click", () => {
                mapAmba.panTo([coords.lat, coords.lng]); // Centrado suave sin alterar el zoom
                
                // Resaltar marcador activo en ambos mapas
                document.querySelectorAll(".custom-marker").forEach(m => m.classList.remove("active"));
                document.querySelectorAll(`.custom-marker.marker-id-${col.id}`).forEach(m => m.classList.add("active"));
                
                // Resaltar tarjeta correspondiente en el listado
                schoolCards.forEach(c => c.classList.remove("active-card"));
                const targetCard = document.querySelector(`.school-card[data-id="${col.id}"]`);
                if (targetCard) targetCard.classList.add("active-card");

                if (floatingCard) floatingCard.classList.remove("on-left"); // Mostrar a la derecha (mapa AMBA)
                showFloatingCard(col);
            });
        }

        // Vincular Clic en Mapa Nacional
        markerArg.on("click", () => {
            mapArg.panTo([coords.lat, coords.lng]); // Centrado suave sin alterar el zoom
            
            // Si el colegio es de Buenos Aires/CABA, centrar y resaltar también en el mapa de AMBA
            if (isAmbaOrPba && markersAmba[col.id]) {
                mapAmba.panTo([coords.lat, coords.lng]);
            }

            // Resaltar marcador activo en ambos mapas
            document.querySelectorAll(".custom-marker").forEach(m => m.classList.remove("active"));
            document.querySelectorAll(`.custom-marker.marker-id-${col.id}`).forEach(m => m.classList.add("active"));

            // Resaltar tarjeta correspondiente en el listado
            schoolCards.forEach(c => c.classList.remove("active-card"));
            const targetCard = document.querySelector(`.school-card[data-id="${col.id}"]`);
            if (targetCard) targetCard.classList.add("active-card");

            if (floatingCard) floatingCard.classList.add("on-left"); // Mostrar a la izquierda (mapa Argentina)
            showFloatingCard(col);
        });
    });

    // 4. Lógica de Filtrado y Búsqueda combinada
    function filterSchools() {
        let visibleCount = 0;
        const searchNormalized = activeSearch.toLowerCase().trim();
        const visibleMarkersArg = [];
        const visibleMarkersAmba = [];

        schoolCards.forEach(card => {
            const id = parseInt(card.getAttribute("data-id"));
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

            // Mostrar/Ocultar tarjeta y pines correspondientes
            if (isVisible) {
                card.classList.remove("d-none");
                // Forzar re-trigger de animación fade-in
                card.style.animation = 'none';
                card.offsetHeight; /* trigger reflow */
                card.style.animation = null; 
                visibleCount++;

                // Sincronizar Mapa Nacional
                if (markersArg[id]) {
                    markersArg[id].addTo(mapArg);
                    visibleMarkersArg.push(markersArg[id]);
                }
                // Sincronizar Mapa AMBA
                if (markersAmba[id]) {
                    markersAmba[id].addTo(mapAmba);
                    visibleMarkersAmba.push(markersAmba[id]);
                }
            } else {
                card.classList.add("d-none");
                card.classList.remove("active-card");
                
                // Ocultar de ambos mapas
                if (markersArg[id]) mapArg.removeLayer(markersArg[id]);
                if (markersAmba[id]) mapAmba.removeLayer(markersAmba[id]);
            }
        });

        // Actualizar contador
        resultsCountEl.textContent = visibleCount;

        // Gestionar estado vacío
        if (visibleCount === 0) {
            emptyState.classList.remove("d-none");
            mapArg.setView(defaultCenterArg, defaultZoomArg);
            mapAmba.setView(defaultCenterAmba, defaultZoomAmba);
            closeFloatingCard();
        } else {
            emptyState.classList.add("d-none");
            
            // Auto-encuadrar el Mapa Nacional
            if (visibleMarkersArg.length > 0) {
                const groupArg = L.featureGroup(visibleMarkersArg);
                if (visibleMarkersArg.length === 1) {
                    mapArg.setView(visibleMarkersArg[0].getLatLng(), 8, { animate: true });
                } else {
                    mapArg.fitBounds(groupArg.getBounds().pad(0.15), { animate: true });
                }
            } else {
                mapArg.setView(defaultCenterArg, defaultZoomArg, { animate: true });
            }

            // Auto-encuadrar el Mapa AMBA
            if (visibleMarkersAmba.length > 0) {
                const groupAmba = L.featureGroup(visibleMarkersAmba);
                if (visibleMarkersAmba.length === 1) {
                    mapAmba.setView(visibleMarkersAmba[0].getLatLng(), 11, { animate: true });
                } else {
                    mapAmba.fitBounds(groupAmba.getBounds().pad(0.15), { animate: true });
                }
            } else {
                mapAmba.setView(defaultCenterAmba, defaultZoomAmba, { animate: true });
            }
        }
    }

    // 5. Escuchar eventos del Buscador
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            activeSearch = e.target.value;
            filterSchools();
        });
    }

    // 6. Clic en Pills de Provincia
    provinciaPills.forEach(pill => {
        pill.addEventListener("click", () => {
            provinciaPills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
            activeProvincia = pill.getAttribute("data-provincia");
            filterSchools();
        });
    });

    // 7. Clic en Pills de Carisma
    carismaPills.forEach(pill => {
        pill.addEventListener("click", () => {
            carismaPills.forEach(c => c.classList.remove("active"));
            pill.classList.add("active");
            activeCarisma = pill.getAttribute("data-carisma");
            filterSchools();
        });
    });

    // 8. Clic en las Tarjetas para interactuar con el Mapa y desplegar la tarjeta flotante
    schoolCards.forEach(card => {
        card.addEventListener("click", () => {
            const id = parseInt(card.getAttribute("data-id"));
            const coords = coordsMap[id];
            const col = colegiosList.find(c => c.id === id);

            if (coords && col) {
                // Resaltar tarjeta seleccionada
                schoolCards.forEach(c => c.classList.remove("active-card"));
                card.classList.add("active-card");

                // Resaltar marcador activo en ambos mapas
                document.querySelectorAll(".custom-marker").forEach(m => m.classList.remove("active"));
                document.querySelectorAll(`.custom-marker.marker-id-${id}`).forEach(m => m.classList.add("active"));

                // Centrar de forma suave en los mapas correspondientes (sin alterar su nivel de zoom por defecto)
                mapArg.panTo([coords.lat, coords.lng], { animate: true });
                
                const isAmbaOrPba = col.provincia === "CABA" || col.provincia === "Provincia de Buenos Aires";
                if (isAmbaOrPba) {
                    mapAmba.panTo([coords.lat, coords.lng], { animate: true });
                    if (floatingCard) floatingCard.classList.remove("on-left"); // Derecha para AMBA
                } else {
                    if (floatingCard) floatingCard.classList.add("on-left"); // Izquierda para Federal
                }

                // Mostrar tarjeta de detalles flotante sobre el mapa
                showFloatingCard(col);
            }
        });
    });

    // 9. Botón de restablecer filtros
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

            closeFloatingCard();
            filterSchools();

            // Reestablecer vistas iniciales de mapas
            mapArg.setView(defaultCenterArg, defaultZoomArg, { animate: true });
            mapAmba.setView(defaultCenterAmba, defaultZoomAmba, { animate: true });
        });
    }
});
