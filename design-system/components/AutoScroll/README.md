Control flotante del scroll automático. En reposo es solo un botón circular de 52px (`accent` con `accent-ink`) abajo a la derecha, para que no tape la letra. Al tocarlo la canción empieza a avanzar y el control se abre (`open`): aparecen − y +, los puntos de nivel y el botón de pausa.

- Abierto es una píldora `surface` al 92% con desenfoque, borde `line` y `shadow-float`, fija a 16px del borde (más el margen seguro del teléfono), z-index 12.
- Nivel con 5 puntos de 7px: encendidos `accent`, apagados `line`, y "Nivel N" en 12px `muted`. Cambiar el nivel solo se puede con el scroll en marcha.
- Se pausa solo al llegar al final o si la persona desliza con el dedo o la rueda; vuelve a ser un solo botón.