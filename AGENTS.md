# Project rules

- After every change: commit, `git push origin main`, then confirm the Vercel
  production deployment is READY and share the live URL:
  https://noor-hossain-portfolio-ten.vercel.app
- Vercel auto-deploys `main` (project `noor-hossain-portfolio`, static site, no build step).
- "Recent work" cards are generated from `scripts/projects.py`
  (`python3 scripts/projects.py index.html`); cover images live in `assets/work/`.
