# Project rules

- After every change: commit, `git push origin main`, then confirm the Vercel
  production deployment is READY and share the live URL:
  https://noor-hossain-portfolio-ten.vercel.app
- Vercel auto-deploys `main` (project `noor-hossain-portfolio`, static site, no build step).
- "Latest projects" cards are generated from `scripts/projects.py` (each project picks a cover style:
  frame/macbook/imac/tablet/browser/angle, full-page screenshots that scroll on hover). Run `python3 scripts/projects.py index.html`; full-page screenshots live in `assets/work/shots/<slug>-full.webp`. Do not move the section.
