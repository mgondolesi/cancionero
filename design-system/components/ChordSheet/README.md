La hoja de la canción: cada acorde va arriba de la sílaba donde cambia (`seg` = acorde en `cc` + trozo de letra en `ll`) y la letra se parte en renglones según el ancho de la pantalla, sin scroll horizontal. Las palabras no se cortan: cada una va en un `w` que no se parte.

- Contenedor `sheet`: `surface`, borde `line`, `radius-lg`, `shadow-card`, relleno 18px 16px. La letra va en la sans del sistema a 17px (`--fs`, con A− / A+), alto de línea 1.4.
- Acordes (`cc`): Inconsolata en negrita (mono, 0.9em) con `chord`. Si el acorde es más ancho que su sílaba, empuja la letra de al lado: es esperado.
- Una línea con solo acordes (intro) es `cl`: mono en negrita y respeta sus espacios. Los rótulos de sección (`s`, VERSO, ESTRIBILLO) van en mayúsculas chicas con `muted`. La tablatura (`raw`) queda monoespaciada, en `muted`, con scroll horizontal propio.
- Cada acorde (`ch`) se puede tocar: hover con `accent` al 22% y `radius-xs`; abre ChordDiagram.
- Quien lo usa pasa el texto original (acordes en una línea, letra debajo, alineados por columnas): la página arma los `seg`. No reformatear el `.txt`.