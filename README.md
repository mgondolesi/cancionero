# Cancionero

Cancionero de guitarra: una página estática con acordes sobre la letra, buscador, tema al azar y transposición.

## Agregar una canción

1. Creá `songs/artista-titulo.txt` con este formato (los acordes quedan alineados con los espacios, no los toques):

   ```
   ---
   title: Brujería
   artist: Los Tipitos
   key: D
   ---
   D
   Nadie puede hablar en serio de algo así
   ```

2. Subilo a `main`. GitHub Pages corre `build.py` y publica solo.

Para probarlo en tu compu:

```bash
python3 build.py
python3 -m http.server   # y abrí http://localhost:8000
```

(`songs.js` se genera con `build.py` y también va commiteado, así el `index.html` funciona abriéndolo directo.)

## Publicar en GitHub Pages (una sola vez)

Settings → Pages → Source: **GitHub Actions**.
