Círculo con la inicial del artista (o de la canción). Sin logo, el color sale del nombre: se calcula un matiz `--h` (0 a 359) a partir del texto y se pinta con `hsl(var(--h) var(--av-bg-s) var(--av-bg-l))` de fondo y `--av-fg-*` de letra, así que cada banda tiene siempre el mismo color.

- Tamaño con `--s` (48px por defecto, 64px en la página de artista, 36px en listas densas). La letra es el 36% del tamaño, en serif negrita.
- En el tema oscuro las variables `--av-*` cambian solas (fondo oscuro y saturado, letra clara).
- `av logo` es la versión con imagen: fondo blanco, borde `line`, la imagen con `object-fit: contain`. Con `photo` la imagen llena el círculo (`cover`) y sin relleno.
- Los logos de `logos/` son solo los que manda el usuario; si no hay, queda la inicial.