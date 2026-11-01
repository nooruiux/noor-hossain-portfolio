# Noor Hossain — Portfolio

Personal portfolio of **Noor Hossain**, UI/UX Designer & Web Developer.

Static single-page site (HTML + CSS + vanilla JS), no build step.

## Run locally
```bash
npx serve .
```

## Deploy
Import this repo on Vercel → Framework Preset: **Other** → Deploy.

## Updating "Recent work"
Project cards are generated from the `PROJECTS` list in `scripts/projects.py`
(newest first). Edit a title, category or Behance `url`, then run:
```bash
python3 scripts/projects.py index.html
```

## Testimonial photos
Client avatars live in `assets/clients/`. To use a real photo, add e.g.
`assets/clients/sarah-k.jpg` and change that client's `"img"` path in the
`<script id="ts-data">` JSON inside `index.html`.
