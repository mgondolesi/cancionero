Cancionero es un cancionero de guitarra para leer en el teléfono: la letra con los acordes encima de cada sílaba. Se siente como papel tibio, una marca serif y un solo acento terracota. Todo el contenido está en español rioplatense.

## Fundamentos de contenido

- Hablá de vos y con verbos cortos: "Ver canciones", "Al azar", "Transponer", "Buscar canción, artista o letra". Sin signos de exclamación ni disculpas.
- Los títulos son los de la canción tal cual, con tildes ("Vine hasta aquí", "Por mil noches"); el artista va aparte, en `muted`.
- Los acordes se escriben en notación inglesa (C#m, G#m, A, E, B, Em, Am7) y el tono se muestra como una píldora.
- Una letra o un acorde se copian solo de lo que la persona pega: nunca se inventa ni se trae de otra web.
- Cero emoji: el único símbolo decorativo son flechas y glifos simples (‹ › × − +).

## Fundamentos visuales

- **Color.** Página `bg`, objetos sobre `surface`, bordes de 1px en `line`, texto en `ink`, texto secundario en `muted`. El acento `accent` (terracota) marca lo que se toca: botón primario, enlaces, foco y valores que cambian. Los acordes van siempre en `chord`. Hay dos temas (claro y oscuro) que cambian solos con el sistema; todo color sale de un token, nunca de un literal.
- **Tipografía.** Serif para marca, títulos y nombres (`t-display`, `t-title`, `t-row-title`); sans del sistema para interfaz (`t-body`, `t-meta`, `t-section-label`); la letra de las canciones va en la sans; Inconsolata (incrustada desde `fonts/`) solo para los acordes (`t-chord-sheet`). Serif y sans usan las fuentes del sistema.
- **Forma.** Píldoras (`radius-pill`) para botones y búsqueda, círculos para avatares y botones de 40px, `radius-lg` para tarjetas y hoja, `radius-md` para filas. Cada objeto tiene borde `line` de 1px; la sombra `shadow-card` es suave y se reserva para tarjetas, búsqueda y hoja.
- **Espaciado.** Margen lateral de 16px, contenido de 880px como máximo y centrado, 12px entre tarjetas, 8px entre filas, 24px entre secciones. En las canciones, los acordes quedan alineados con la letra por columnas en el `.txt`; la página los coloca sobre cada sílaba.
- **Movimiento.** Corto y funcional: entrada de 0.22s (sube 8px y aparece), hover que levanta 2px, apretar que achica a 0.98, pulso del micrófono. Todo se apaga con `prefers-reduced-motion`.
- **Estados.** Hover: borde en `accent`. Foco: contorno sólido de 2px en `accent` con 2px de separación. Escuchando: fondo `rec`.
- **Imágenes.** Sin ilustraciones. Un avatar con la inicial coloreada por el nombre; los logos son solo los que manda el usuario.
- **Barra superior.** Fija, `bg` al 86% con desenfoque, borde inferior `line`, 56px de alto.

## Iconografía

No hay librería de íconos. Los íconos son SVG de trazo de 2px (`currentColor`, 18px) para la lupa y el micrófono, y glifos de texto para flechas y pasos. Los diagramas de acordes son SVG propios con las clases `g-*` ligadas a los tokens.

## Uso

- Usá `t-display` para el título de inicio con una palabra en cursiva en `accent`; `t-title` para canción y artista.
- Armá listas con `SongRow` (un artista por canción) y grillas de `ArtistCard`; una `SearchField` arriba.
- La hoja se arma con `ChordSheet` y su barra con `Transposer`; el scroll automático con `AutoScroll`; los diagramas con `ChordDiagram`.
- El texto secundario (`muted`) a 13px o más y sobre `surface`: sobre `bg` claro da 4.2:1 y sobre `surface-2` 3.9:1, valores del original que se dejaron como están.
- `accent` sobre `bg` claro da 4.2:1: usalo en 13px o más en negrita, o sobre `surface` (4.6:1).
- La letra se parte en renglones; solo la tablatura se desplaza en horizontal.
