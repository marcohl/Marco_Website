# Cómo editar el texto del sitio

Todo el texto visible del sitio está en esta carpeta, un archivo por página:

| Archivo | Página |
|---|---|
| `site.md` | Cabecera, menú, pie de página, contacto (en todas las páginas) |
| `home.md` | Portada, About, gráfico de átomos |
| `404.md` | Página de error |
| `projects/<slug>.md` | Cada proyecto (texto, cifras clave, insights, notas, textos de los gráficos) |

Editas el archivo, guardas, y con `npm run dev` abierto la página se actualiza sola en `localhost:4321`.

## Las secciones

Cada archivo está dividido en secciones que empiezan con una línea así:

```
[[intro]]
```

La sección llega hasta el siguiente `[[...]]`. **No cambies ni borres los nombres entre `[[ ]]`**: el código los usa para saber dónde va cada texto. Todo lo que está antes de la primera sección es una nota para ti y no se publica.

Hay cuatro tipos de sección. El tipo depende de la sección, no hace falta declararlo:

**1. Texto (Markdown).** Párrafos normales. Una línea en blanco separa párrafos.

```
# Titular de la página (h1)
## Subtítulo
### Título de columna (en "Notes and method" cada ### es una columna)
**negrita**   *cursiva o número resaltado en el titular*
[texto del enlace](https://...)
`nombre_de_archivo.py`
```

**2. Etiquetas (`clave: texto`).** Una por línea. Cambia solo lo que va después de `: `. Las líneas que empiezan con `#` son comentarios. Se usan en `[[page]]` (título, descripción) y en los textos de los gráficos.

```
title: Where Bolivia makes its electricity
```

**3. Cifras clave (`- etiqueta | valor`).** Las cajas de números junto al titular. Puedes cambiar el orden, añadir o quitar líneas.

```
- Capacity, end of 2025 | {capacity_mw} MW
```

**4. Lista numerada (`1. ...`).** Los insights bajo el gráfico. Cada número es un punto.

## Los números: `{marcadores}`

Los números que salen de los datos se escriben como `{nombre}`, por ejemplo `{capacity_mw}`. Al publicar se reemplazan por el valor real del JSON, así el texto nunca queda desactualizado frente a los datos.

- La lista de marcadores disponibles está al inicio de cada archivo de proyecto.
- Si escribes un marcador que no existe (por ejemplo un error de tipeo), `npm run dev` / `npm run build` muestran un error que dice el archivo, la sección y los marcadores válidos.
- Puedes escribir números a mano, pero entonces tienes que actualizarlos tú si cambian los datos (y deben poder rastrearse a una fuente).
- Si necesitas un número nuevo, pídelo: se añade en el `.mdx` del proyecto (ahí se calculan).

En las secciones de gráficos (`[[map-chart]]`, `[[history-chart]]`, `[[atom-chart]]`) los marcadores se llenan mientras usas el gráfico; el comentario de cada sección dice cuáles hay.

## Qué no está aquí

- Fecha, tags, estado (`published`), código `MHL-00N`: en el frontmatter del `.mdx` de cada proyecto (`src/pages/projects/`).
- Los textos dentro de los gráficos de uranio, reactores y natación todavía están en sus componentes (`src/components/viz/`). Bolivia es el piloto.
