# Project rules

- After every change: commit, `git push origin main`, then confirm the Vercel
  production deployment is READY and share the live URL:
  https://noor-hossain-portfolio-ten.vercel.app
- Vercel auto-deploys `main` (project `noor-hossain-portfolio`, static site, no build step).
- "Latest projects" is an Orbix-style 3-column grid (same light-grey cover bg, hover shows a cursor ellipse with the project name, click opens it). Cards are generated from `scripts/projects.py` (cover styles:
  frame/macbook/imac/tablet/browser/angle, full-page screenshots that scroll on hover). Run `python3 scripts/projects.py index.html`; full-page screenshots live in `assets/work/shots/<slug>-full.webp`. Do not move the section.
