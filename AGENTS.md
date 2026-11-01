# Project rules

- After every change: commit, `git push origin main`, then confirm the Vercel
  production deployment is READY and share the live URL:
  https://noor-hossain-portfolio-ten.vercel.app
- Vercel auto-deploys `main` (project `noor-hossain-portfolio`, static site, no build step).
- "Latest projects" cards are generated from `scripts/projects.py` (each project picks a cover style:
  laptop/float/bleed/phone/browser/split). Run `python3 scripts/projects.py index.html`; screenshots live in `assets/work/shots/`. Do not move the section.
