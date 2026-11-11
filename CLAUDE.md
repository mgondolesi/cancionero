# Cancionero — instrucciones para Claude

Cancionero de guitarra (acordes sobre la letra). El usuario habla en español rioplatense.
`songs/*.txt` son las canciones; `template.html` + `build.py` generan `index.html`
(un único archivo autocontenido que se publica en GitHub Pages).

## Cuando el usuario pega una canción en el chat: hacerlo todo, sin preguntar

Si el usuario pega o adjunta el texto de una canción (con o sin menús, links, puntajes
u otra basura de la web), **no preguntes nada y no pidas confirmación**: importala,
armá la página y subila a `main`. Pasos:

1. **Título y artista.** Salen del mensaje del usuario, del nombre del archivo adjunto
   (`artista - titulo.txt`, `titulo_-_artista.txt`) o de los dos primeros links del texto
   (`[Título](...)`, `[Artista](...)`). Solo si no hay forma de saberlos, preguntá.
2. **Guardar el texto crudo en `inbox/`** como `artista - titulo.txt` (sin modificarlo).
3. **Correr `python3 importar.py`.** Limpia el texto, arma el encabezado (título, artista,
   tono estimado), completa los acordes de estrofas repetidas con `fill_chords.py`,
   escribe en `songs/` y borra el archivo de `inbox/`.
4. **Revisar el resultado** (`songs/<artista>-<titulo>.txt`) y corregir a mano lo que el script
   no resuelve bien: tildes del título, tono mal estimado, estrofas con distinta cantidad de
   líneas que quedaron sin acordes (`python3 fill_chords.py` las lista), líneas de acordes
   mezcladas con la letra, etc.
5. **Correr `python3 build.py`** para regenerar `index.html`. Si avisa de una repetida,
   avisale al usuario en la respuesta (si es repetida de verdad, no la agregues).
6. **Commit y push a `main`** (el usuario lo autorizó para las canciones; si la sesión
   tiene una rama propia, empujá también a esa). Mensaje de commit corto en español,
   por ejemplo `Agregar Vine hasta aquí (Los Piojos)`.
7. **Responder breve**: qué canción se agregó, tono, qué estrofas se completaron
   automáticamente y qué conviene revisar. Sin pedir permiso para lo ya hecho.

Si el usuario pega varias canciones juntas, repetí el proceso con cada una (un commit
por canción o uno solo, como sea más simple).

## Logos de las bandas

Si el usuario manda la imagen del logo de una banda, guardala en `logos/` con el nombre del
artista en minúsculas, sin tildes y con guiones (`los-piojos.png`), achicala a unos 200x200 px
si pesa mucho, corré `python3 build.py`, probá en el navegador que se vea bien y subila a `main`.
No descargues logos de la web: solo los que el usuario manda.

## Reglas

- **No copies letras ni acordes de ninguna web.** Solo se agrega lo que el usuario pega o
  adjunta. No armar scrapers de La Cuerda ni de otros sitios.
- No toques las canciones existentes salvo que el usuario lo pida.
- Los acordes quedan alineados con la letra por los espacios: respetá los espacios y usá
  fuente monoespaciada. No reformatees líneas de acordes.
- `index.html` se genera: no editarlo a mano. El código de la página está en `template.html`.
- Después de cambiar `template.html` o `build.py`, probar en el navegador (Playwright está
  instalado) antes de subir.
- El repo no tiene permiso para cambiar ajustes de GitHub (rama default, Pages): si hace
  falta, decirle al usuario qué tocar.

## Archivos

- `importar.py` — limpia e importa lo que hay en `inbox/` (también lo corre la Action).
- `fill_chords.py` — copia acordes a estrofas repetidas sin acordes (`--write` para aplicar).
- `build.py` — arma `index.html`; avisa de canciones repetidas.
- `.github/workflows/pages.yml` — importa `inbox/`, arma el HTML y publica en Pages.
