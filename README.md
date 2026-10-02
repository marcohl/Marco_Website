# Marco's Website

Small data-analysis and science-outreach projects, each built around one
interactive d3.js chart. Built with Astro, d3 and Python.

## Run it

```
npm install
npm run dev          # http://localhost:4321
npm run build        # static site in dist/
```

Data for each project is rebuilt with `python3 analysis/<slug>/build_data.py`.

## Working with Claude Code

Open this folder with Claude Code. `CLAUDE.md` holds the method every project
follows (brief, data, form, build, words, QA, publish). Start a project with:

```
/new-project <topic>
```

and check it before publishing with `/qa <slug>`.

## Projects

| Slug | Title | Status |
|---|---|---|
| `uranium-enrichment` | Seven in a Thousand | published |
