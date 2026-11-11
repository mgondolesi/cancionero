# Cancionero

Cancionero de guitarra: una página estática con acordes sobre la letra, buscador, tema al azar y transposición.

## Agregar una canción

1. En GitHub: `songs` → Add file → Create new file → `artista-titulo.txt`, con este formato (los acordes quedan alineados con los espacios, no los toques):

   ```
   ---
   title: Brujería
   artist: Los Tipitos
   key: D
   ---
   D
   Nadie puede hablar en serio de algo así
   ```

2. Commit a `main`. Una Action regenera `index.html` (con todas las canciones adentro) y publica la página. No hay que correr nada.

`index.html` es un único archivo autocontenido: se puede descargar y abrir offline, con todos los temas.

Archivos: `template.html` es el código de la página, `index.html` se genera solo (no editar a mano). Para probar local: `python3 build.py`.

## Publicar en GitHub Pages (una sola vez)

Settings → Pages → Source: **GitHub Actions**.

## Completar acordes de estrofas repetidas

Si una canción trae los acordes solo en la primera estrofa y las siguientes vienen sin acordes, `fill_chords.py` los copia (mismas columnas, misma cantidad de líneas, misma sección):

```bash
python3 fill_chords.py            # simulación: muestra qué completaría
python3 fill_chords.py --write    # aplica los cambios
python3 fill_chords.py songs/archivo.txt --write   # una sola canción
```

Conviene revisar el resultado: los acordes quedan aproximadamente sobre las mismas sílabas, no exactamente.

## Control de repetidas

`build.py` avisa si hay canciones repetidas: mismo título y artista (ignorando tildes y mayúsculas), contenido casi igual, o mismo título con distinto artista. Es solo un aviso: no frena la publicación. En GitHub aparece como advertencia amarilla en la ejecución de "Publicar cancionero" (pestaña Actions).

## Sumar canciones sin correr nada: la carpeta `inbox/`

1. En GitHub: `inbox` → Add file → Create new file. Nombralo `artista - titulo.txt` (por ejemplo `los piojos - vine hasta aqui.txt`).
2. Pegá adentro el texto tal cual lo copiaste, con todo lo que traiga.
3. Commit a `main`.

La Action corre `importar.py`: limpia el texto (menús, puntajes, "Enviado por", links), arma el encabezado con título, artista y tono (el tono es una estimación: revisalo), completa los acordes de las estrofas repetidas, avisa si la canción ya existe, la guarda en `songs/`, borra el archivo de `inbox/` y publica la página.

Si el nombre no tiene " - ", intenta sacar título y artista de los dos primeros links del texto copiado. Si no puede, deja un aviso amarillo en Actions y el archivo queda en `inbox/`.

Para probarlo en la compu: `python3 importar.py --dry-run` (simulación) o `python3 importar.py`.

## Logos de las bandas

Si hay una imagen en `logos/` con el nombre del artista, la página la usa en lugar de la inicial. Si no hay, queda la inicial.

- Nombre del archivo: el artista en minúsculas, sin tildes y con guiones: `los-piojos.png`, `babasonicos.png`, `ella-es-tan-cargosa.png`. Sirve `.png`, `.jpg`, `.webp` o `.svg`.
- Tamaño: unos 200x200 px alcanza (el logo se guarda dentro del HTML; `build.py` avisa si pesa más de 200 KB).
- Si el nombre no coincide con ningún artista, `build.py` avisa y lo ignora.

### Foto automática al importar una banda nueva

Cuando `importar.py` importa una canción de un artista que todavía no está en el cancionero y no tiene imagen en `logos/`, intenta bajar la imagen principal de su página de Wikipedia (primero en español, después en inglés) a 200 px y la guarda en `logos/`.

- Es automático y puede equivocarse o no encontrar nada (en ese caso queda la inicial y el script lo avisa). Para cambiarla, poné tu propio archivo en `logos/` con el nombre del artista (reemplaza el que bajó solo).
- Las imágenes `.jpg` (fotos) se muestran llenando el círculo; las `.png`/`.svg` (logos) se muestran enteras con un margen.
- Para saltearlo: `python3 importar.py --sin-fotos`.
