# Propuesta de Redefinición Cromática y Visual - Organización FEM

Este documento detalla la reestructuración del sistema visual y cromático para el portal de la **Fundación Educación y Misión (FEM)**. El objetivo es transicionar de una estética fría, oscura ("dashboard corporativo") hacia una interfaz **clara, cálida, institucional y humana**, alineada con el clima de una comunidad educativa y católica.

---

## 1. Justificación Visual de la Nueva Dirección

*   **Luz y Cercanía:** Reemplazamos los fondos oscuros (tanto en la cabecera como en el footer) por superficies claras y cálidas. El blanco tiza/alabastro (`#fdfdfa`) y el arena suave (`#f5f3eb`) transmiten serenidad, orden y transparencia.
*   **Eliminación del Azul Navy (Estética Tech):** La base azul marino (navy) no forma parte de la identidad de FEM y le daba un look comercial o corporativo alejado de la vida escolar. En su lugar, el **negro corporativo se suaviza a un grafito cálido** (`#2e3238`) para botones y jerarquías principales, manteniendo la seriedad institucional pero con mayor amabilidad visual.
*   **Protagonismo del Amarillo Cálido (Pantone 142 C):** Este color actúa como el acento del sistema. Evoca luz, cuidado y cercanía, aplicándose en detalles decorativos, bordes de destaque e iconografía.
*   **Footer Claro e Institucional:** Se elimina el bloque negro/oscuro del footer. Ahora utiliza un tono gris cálido claro (`#eae8e1`) con textos legibles en grafito, cerrando la página de manera limpia, sin dramatismo ni peso visual excesivo.

---

## 2. Propuesta de Tokens CSS en `:root`

A continuación se detallan las variables CSS listas para declarar en `app/static/src/scss/_tokens.scss`. Se eliminan las referencias a colores azulados y se definen roles semánticos basados en tonos arena y grafito:

```css
:root {
  /* ==========================================================================
     PALETA DE MARCA OFICIAL (FIEL AL MANUAL)
     ========================================================================== */
  --color-white: #ffffff;
  --color-black: #1a1c1e;              /* Negro carbón suave */
  --color-pantone-grey-raw: #888B8D;   /* Pantone Cool Grey 8 C */
  --color-pantone-yellow-raw: #F1BE48; /* Pantone 142 C (Dorado/Ocre) */

  /* ==========================================================================
     ROLES DE INTERFAZ (CLARA, CÁLIDA E INSTITUCIONAL)
     ========================================================================== */
  /* Superficies y Fondos */
  --color-bg: #fdfdfa;                 /* Alabastro / Blanco hueso cálido */
  --color-bg-alt: #f5f3eb;             /* Arena suave para alternancia de bloques */
  --color-card: var(--color-white);
  --color-border: #e4e2da;             /* Gris arena sutil para hilos de contorno */

  /* Textos (Legibilidad y Jerarquía) */
  --color-text: #202224;               /* Grafito oscuro para lectura cómoda */
  --color-text-muted: #6e7278;         /* Gris medio para datos secundarios */

  /* Elementos de Acción (Sin Navy/Azules) */
  --color-primary: #2e3238;            /* Grafito institucional para botones primarios */
  --color-primary-hover: #1f2125;      /* Grafito más oscuro */
  --color-secondary: var(--color-pantone-grey-raw); /* Gris medio para botones secundarios */
  
  --color-accent: var(--color-pantone-yellow-raw);  /* Ocre/Amarillo cálido para acentos */
  --color-accent-hover: #dba853;

  /* Componentes Estructurales */
  --color-navbar-bg: var(--color-white);
  --color-footer-bg: #eae8e1;          /* Gris arena institucional para el Footer claro */
  --color-footer-text: #3c3f44;
}
```

---

## 3. Checklist de Colores a Eliminar o Reemplazar

Para lograr la transición visual completa, se deben retirar del código de estilos (`_tokens.scss`, `_layout.scss`, `_components.scss`) los siguientes valores y criterios:

- [ ] **Eliminar el azul marino (`#1b365d` y `#122540`):** Reemplazar en los botones primarios (`--color-primary`) por el grafito institucional (`#2e3238`).
- [ ] **Eliminar fondos negros sólidos en bloques:** Quitar el fondo negro en el footer (`.main-footer`) y cambiarlo por el gris arena claro (`--color-footer-bg` / `#eae8e1`).
- [ ] **Reemplazar bordes grises fríos (`#e2e8f0` o `#e8e8e8`):** Cambiar por el gris arena cálido (`#e4e2da`) para mantener la cohesión con la paleta tierra.
- [ ] **Reemplazar textos negros puros en párrafos (`#000000`):** Ajustar al grafito oscuro `#202224` para suavizar el contraste contra los fondos claros.
- [ ] **Eliminar sombreados complejos o elevados:** Cambiar la variable `--shadow-sm` y `--shadow-md` a bordes planos (`1px solid var(--color-border)`) o a sombras imperceptibles (`rgba(0, 0, 0, 0.02)`).

---

## 4. Estructura y Usabilidad de Componentes bajo este Sistema

*   **Cabecera (Navbar):** Fondo blanco, hilos finos de color arena en la parte inferior, y uso del logotipo oficial en colores (`logo-fem-color.png`), que ahora resalta perfectamente gracias a la base clara.
*   **Hero Section:** Fondo completamente blanco hueso (`--color-bg`), tipografía en grafito oscuro, y un pequeño indicador o viñeta en amarillo ocre (`--color-accent`).
*   **Cards (Misión/Visión/Dimensiones):** Tarjetas blancas puras (`--color-card`) sobre el fondo alterno arena (`--color-bg-alt`), con un filete perimetral muy sutil. Al hacer hover, el borde cambia a amarillo ocre, sin movimientos en el eje Y.
*   **Footer:** Fondo arena claro (`#eae8e1`), textos en grafito y uso del logotipo oficial en colores, generando un cierre sumamente amigable y luminoso.
