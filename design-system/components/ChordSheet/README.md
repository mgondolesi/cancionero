La hoja de la canción: texto monoespaciado con los acordes en una línea y la letra debajo. Los acordes se alinean con la letra por los espacios, así que se respeta cada espacio y no se reformatea ninguna línea.

- Contenedor `pre`: `surface`, borde `line`, `radius-lg`, `shadow-card`, relleno 18px 16px, desplazamiento horizontal propio. Tamaño base 15px (`--fs`), alto de línea 1.4.
- Acordes: clase `c`, negrita en `chord`. Marcas de sección entre corchetes ([Estribillo]): clase `s`, negrita en `muted`.
- Cada acorde (`ch`) se puede tocar: hover con un fondo de `accent` al 22% y `radius-xs`; abre la ventana de diagramas (ChordDiagram).
- Deja 110px libres debajo para el deslizador flotante.