Tarjeta de artista: avatar arriba, nombre en serif negrita y cantidad de canciones en `muted`. Va en una grilla de 2 columnas en teléfono, 3 desde 560px y 4 desde 800px, con 12px de separación.

- `surface`, borde `line`, `radius-lg`, `shadow-card`, 16px de relleno y 14px entre avatar y texto.
- Hover: borde `accent` y sube 2px; al apretar, se achica a 0.98. Sin animación si la persona pidió reducir movimiento.
- Los nombres largos se parten (`overflow-wrap: anywhere`). Debajo de la grilla, las letras de sección usan `t-letter` en `accent`.