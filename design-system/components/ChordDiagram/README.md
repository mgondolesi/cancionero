Ventana de diagramas que se abre al tocar un acorde de la hoja. En teléfono sube desde abajo con el fondo oscurecido (`rgba(0,0,0,.5)`) y las esquinas superiores en `radius-xl`; desde 700px se centra con las cuatro esquinas redondeadas. Fondo `bg`, borde `line`, `shadow-sheet`, máximo 640px y 88vh.

- Encabezado: nombre del acorde en `t-chord-name` con `accent` y un botón `cd-x` circular de 40px para cerrar.
- Grilla `cd-grid` de tarjetas de 128px mínimo (`radius-md`). Cada tarjeta es un SVG de 6 cuerdas y 5 trastes: cejilla gruesa en `ink`, cuerdas y trastes en `muted` de 1px, puntos `g-dot` en `accent`, cuerdas al aire `g-open` y silenciadas `g-x` en `ink`.
- Debajo del SVG, nombre de la posición y nota en `muted` de 12px; si no empieza en el primer traste, el número va en `t-fret` con `accent`.
- Se cierra con la ×, tocando fuera o con Escape; la animación (aparecer y subir) se omite si se pidió reducir movimiento.