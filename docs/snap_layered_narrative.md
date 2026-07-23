# Arquitectura del Sistema: Snap-Layered Narrative

El patrón **Snap-Layered Narrative** es una evolución del motor *Layered Reveal* diseñado para sitios institucionales y editoriales que requieren un scroll narrativo inmersivo por escenas (001, 002, 003...). 

Combina la presencia y el ritmo de un cambio de pantalla completo con la calidez, la continuidad y la elegancia visual de **Fundación FEM**, evitando rigideces futuristas y bloqueos de desbordamiento en dispositivos móviles.

---

## 🆚 Comparativa: Layered Reveal Clásico vs. Snap-Layered Narrative

| Característica | Layered Reveal Clásico | Snap-Layered Narrative |
| :--- | :--- | :--- |
| **Gramática de Scroll** | Revelado continuo de bloques | Lectura por **Escenas Numeradas (001, 002...)** |
| **Profundidad Visual** | Fade In / Fade Out básico | **Transición Multinivel (Scale + Blur + Brightness)** |
| **Máquina de Estados** | Binary (`is-active` / fuera de foco) | 5 Estados (`is-entering`, `is-active`, `is-exiting`, `is-before`, `is-after`) |
| **Staggering de Texto** | Bloque único | Micro-ritmo secuencial (`.lr-scene-tag` -> `h2` -> `p` -> CTAs) |
| **Comportamiento Mobile** | Lista de tarjetas con scroll tradicional | Escenas con `100dvh`, centrado simétrico y puntero sutil |
| **Compatibilidad WebKit** | Riesgo de bloqueo con `overflow: hidden` | **Scroll fluido 100% continuo sin scroll-lock** |

---

## ⚙️ Máquina de Estados Visuales (State Machine)

Cada sección `.lr-section` recibe clases dinámicas asignadas en tiempo real por el observador de intersección:

| Estado | Descripción | Estilos Aplicados |
| :--- | :--- | :--- |
| `is-active` | Escena dominante en el viewport. | `opacity: 1; transform: scale(1) translateY(0); filter: brightness(1) blur(0); z-index: 10;` |
| `is-entering` | Capa entrante desde la dirección de movimiento. | `opacity: 0.65; transform: scale(0.98) translateY(12px); filter: brightness(0.6) blur(1px); z-index: 6;` |
| `is-exiting` | Capa saliente al avanzar. | `opacity: 0.65; transform: scale(0.98) translateY(-12px); filter: brightness(0.6) blur(1px); z-index: 6;` |
| `is-before` | Capa previa situada arriba en la pila narrativa. | `opacity: 0.35; transform: scale(0.96) translateY(-18px); filter: brightness(0.4) blur(2px); z-index: 2;` |
| `is-after` | Capa posterior situada abajo en la pila. | `opacity: 0.35; transform: scale(0.96) translateY(18px); filter: brightness(0.4) blur(2px); z-index: 2;` |

---

## 📂 Atributos y Estructura HTML Reutilizable

Para utilizar el sistema en una nueva página o proyecto, se requiere la siguiente estructura básica:

```html
<div class="lr-container" id="layered-reveal-container" data-active-scene="001">
    
    <!-- Escena N -->
    <section class="lr-section is-active" 
             data-layer-item 
             data-layer-id="hero" 
             data-layer-order="1" 
             data-scene-num="001" 
             id="hero">
        
        <div class="lr-media">
            <img src="imagen_de_fondo.jpg" alt="Descripción de escena" loading="eager" decoding="async">
        </div>
        
        <div class="lr-overlay"></div>
        
        <div class="lr-content">
            <span class="lr-kicker">
                <span class="lr-scene-tag">001</span> Título Secundario
            </span>
            <h2>Título Principal de la Escena</h2>
            <p>Texto descriptivo con lectura calmada y tipografía editorial.</p>
            <div class="lr-cta-actions">
                <a href="/link" class="lr-cta">Acción Principal</a>
            </div>
        </div>
    </section>

    <!-- Indicador de Progreso Lateral / Mobile -->
    <nav class="lr-nav-progress" id="lr-nav-progress" aria-label="Navegación narrativamente por capas">
        <div class="lr-progress-bar">
            <div class="lr-progress-fill" id="lr-progress-fill"></div>
        </div>
        <button class="lr-nav-dot is-active" data-nav-dot data-target-id="hero" aria-label="Ir a escena 1"></button>
    </nav>

</div>
```

---

## 📱 Guía de Adaptación Responsiva (Mobile First)

En pantallas `< 767px`:
1. Cada sección `.lr-section` ocupa `min-height: 100dvh` para encuadrar la escena sin solapamientos.
2. El contenedor `.lr-content` centra simétricamente el texto, títulos y CTAs.
3. El puntero `.lr-nav-progress` se simplifica a una línea vertical ultra-sutil con puntos dorados de 8px y un área táctil invisible de `44px x 44px` para cumplir con las directrices de accesibilidad **WCAG AAA**.

---

## ♿ Accesibilidad y Degradación Razonable

1. **`prefers-reduced-motion: reduce`**: Desactiva las transformaciones espaciales, desenfoques y zooms, mostrando las escenas en opacidad 1 de forma estática sin saltos bruscos.
2. **Teclado**: Permite navegar entre escenas utilizando las teclas `PageDown`, `PageUp`, `Flecha Abajo` y `Flecha Arriba`.
3. **Lectores de pantalla**: Atributos `aria-selected` en los botones de navegación y etiquetas descriptivas `aria-label` por escena.
