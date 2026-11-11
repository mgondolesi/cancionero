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
