"""Regenerate the "Latest projects" section of index.html.

Usage:  python3 scripts/projects.py index.html

Each project picks a cover `style` so the grid never repeats itself:
  laptop  - pre-rendered laptop + phone mockup (assets/work/<img>.webp)
  float   - desktop screen tilted in 3D with floating UI chips
  bleed   - full-bleed screenshot, outlined brand word, phone peeking in
  phone   - large phone on a glowing backdrop with stat chips
  browser - light browser window that pans on hover, brand watermark
  split   - screenshot + mini style guide (swatches and type)
Screenshots live in assets/work/shots/<slug>-d.webp (desktop) and -m.webp (mobile).
"""
import html, re, sys

PROJECTS = [
    dict(slug="content-writing-ai-website", style="frame", span=7, title="Quantum", sub="AI Content Writing Website",
         tags=["AI SaaS", "Web Design", "Next.js"], url="https://content-writing-ai-website.vercel.app/",
         bg="#e9e8e5", accent="#8b5cf6", year="2026"),
    dict(slug="project-management-saas-website", style="macbook", span=5, title="WorkUp", sub="Project Management SaaS",
         tags=["SaaS", "UI/UX", "Dashboard"], url="https://project-management-saa-s-website.vercel.app/",
         bg="#e9e8e5", accent="#c4b5fd", year="2026", chips=["+ Add task", "Sprint 12 · 75%"]),
    dict(slug="fitness-training-website", style="imac", span=5, title="Gymnastic", sub="Fitness Training Website",
         tags=["Fitness", "Web Design"], url="https://fitness-training-website-bay.vercel.app/",
         bg="#e9e8e5", accent="#22d3ee", year="2026", logo="GYMNASTIC", cta="Be a Member"),
    dict(slug="cryptocurrency-website", style="tablet", span=7, title="Lumino", sub="Bitcoin Mining Platform",
         tags=["Crypto", "Fintech", "Web Design"], url="https://cryptocurrency-website-development.vercel.app/",
         bg="#e9e8e5", accent="#7c5cff", year="2026", chips=["Total deposits $8M+", "Active users 125k+"]),
    dict(slug="rent-a-car-website", style="browser", span=7, title="Rent", sub="Car Rental Website · Dubai",
         tags=["Car Rental", "Booking UX", "Next.js"], url="https://rent-a-car-website-eight.vercel.app/",
         bg="#e9e8e5", accent="#1d72e8", year="2026", logo="Rent", cta="Book in 60 sec"),
    dict(slug="nattoral", style="angle", span=5, title="Nattoral", sub="Skincare E-commerce Store",
         tags=["E-commerce", "Beauty", "UI/UX"], url="https://nattoral-zeta.vercel.app/",
         bg="#e9e8e5", accent="#2f4f4a", year="2026", logo="NATTORAL", swatches=["#2f4f4a", "#9bc7c0", "#e9e3d6", "#111111"]),
    # Behance case studies (cover images to be added: set img="..." in assets/work/behance/)
    dict(img="team-collabs.webp", device="full", kind="behance", style="be", span=7, title="Team Collabs", sub="Website UI", tags=["Website", "UI Design"],
         url="https://www.behance.net/gallery/159708065/Team-Collabs-Website-UI", bg="#e9e8e5", accent="#4f46e5", year="Behance", word="Collabs"),
    dict(img="saas-clicker.webp", device="full", kind="behance", style="be", span=5, title="SaaS Landing Page", sub="UI/UX Design", tags=["SaaS", "Landing Page"],
         url="https://www.behance.net/gallery/238128689/SaaS-Landing-Page-ui-ui-design-uiux-design", bg="#e9e8e5", accent="#ff5a1f", year="Behance", word="SaaS"),
    dict(img="saas2.webp", device="frame", kind="behance", style="be", span=5, title="SaaS Landing Page", sub="UI/UX Design · v2", tags=["SaaS", "Landing Page"],
         url="https://www.behance.net/gallery/172665281/Saas-Landing-Page-ui-ui-design-uiux-Design", bg="#e9e8e5", accent="#0ea5e9", year="Behance", word="SaaS"),
    dict(img="interior.webp", device="frame", kind="behance", style="be", span=7, title="Interior Design", sub="Landing Page", tags=["Interior", "Landing Page"],
         url="https://www.behance.net/gallery/183139315/Interior-Design-Landing-Page-ui-ui-design-uiux-design", bg="#e9e8e5", accent="#a16207", year="Behance", word="Interior"),
    dict(img="agency.webp", device="frame", kind="behance", style="be", span=12, title="Marketing Agency", sub="Landing Page", tags=["Agency", "UI/UX Design"],
         url="https://www.behance.net/gallery/165900155/Marketing-Agency-Landing-Page-UIUX-Design", bg="#e9e8e5", accent="#db2777", year="Behance", word="Agency"),
]

ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'


def shot(p, kind, cls, alt=""):
    return f'<img class="{cls}" src="/assets/work/shots/{p["slug"]}-{kind}.webp" alt="{alt}" loading="lazy" decoding="async">'


def cover(p):
    e = lambda k: html.escape(p.get(k, ""))
    st = p["style"]
    if st == "be":
        if p.get("img"):
            src = f'/assets/work/behance/{p["img"]}'
            im = f'<img class="be-fill" src="{src}" alt="{e("title")} — {e("sub")} cover" loading="lazy" decoding="async">'
            dev = p.get("device", "browser")
            if dev == "full":
                return f'<img class="be-img" src="{src}" alt="{e("title")} — {e("sub")} design" loading="lazy" decoding="async">'
            if dev == "browser":
                return f'<div class="dv-win"><div class="dv-bar"><i></i><i></i><i></i><span>behance.net</span></div><div class="dv-scr">{im}</div></div>'
            if dev == "frame":
                return f'<div class="dv-frame"><div class="dv-scr">{im}</div></div>'
            if dev == "tablet":
                return f'<div class="dv-tab"><span class="dv-cam"></span><div class="dv-scr">{im}</div></div>'
            if dev == "imac":
                return f'<div class="dv-imac"><div class="dv-mon"><div class="dv-scr">{im}</div><div class="dv-chin"></div></div><div class="dv-neck"></div><div class="dv-foot"></div></div>'
            return f'<div class="dv-laptop"><div class="dv-lid"><span class="dv-cam"></span><div class="dv-scr">{im}</div></div><div class="dv-base"></div></div>'
        return (f'<div class="be-cv"><span class="be-word" aria-hidden="true">{e("word")}</span>'
                f'<div class="be-in"><span class="be-logo">Bē Behance case study</span><b>{e("title")}</b><small>{e("sub")}</small>'
                f'<span class="be-cta">View on Behance ↗</span></div></div>')
    if st == "frame":
        return (f'<div class="dv-frame"><div class="dv-scr"><img src="/assets/work/shots/{p["slug"]}-full.webp" alt="{e("title")} full website" loading="lazy" decoding="async"></div></div>')
    if st == "tablet":
        return (f'<div class="dv-tab"><span class="dv-cam"></span><div class="dv-scr"><img src="/assets/work/shots/{p["slug"]}-full.webp" alt="{e("title")} full website" loading="lazy" decoding="async"></div></div>')
    if st == "browser":
        return (f'<div class="dv-win"><div class="dv-bar"><i></i><i></i><i></i><span>{e("title").lower()}.com</span></div>'
                f'<div class="dv-scr"><img src="/assets/work/shots/{p["slug"]}-full.webp" alt="{e("title")} full website" loading="lazy" decoding="async"></div></div>')
    if st in ("macbook", "angle"):
        return (f'<div class="dv-laptop{" tilt" if st == "angle" else ""}"><div class="dv-lid"><span class="dv-cam"></span>'
                f'<div class="dv-scr"><img src="/assets/work/shots/{p["slug"]}-full.webp" alt="{e("title")} full website" loading="lazy" decoding="async"></div></div>'
                f'<div class="dv-base"></div></div>')
    if st == "imac":
        return (f'<div class="dv-imac"><div class="dv-mon"><div class="dv-scr">'
                f'<img src="/assets/work/shots/{p["slug"]}-full.webp" alt="{e("title")} full website" loading="lazy" decoding="async"></div>'
                f'<div class="dv-chin"></div></div><div class="dv-neck"></div><div class="dv-foot"></div></div>')
    raise ValueError(st)


def card(i, p):
    tags = ''.join(f'<span>{html.escape(t)}</span>' for t in p["tags"])
    style = f'--bg:{p["bg"]};--ac:{p["accent"]}'
    be = p.get("kind") == "behance"
    badge = '<span class="pc-live be"><b>Bē</b>Behance</span>' if be else '<span class="pc-live"><i></i>Live</span>'
    where = "on Behance" if be else "(live site)"
    return f'''        <article class="pc s{p["span"]} rv" data-style="{p["style"]}">
          <a class="pc-cover is-{p["style"]}" href="{p["url"]}" target="_blank" rel="noopener" style="{style}" aria-label="Open {html.escape(p["title"])} — {html.escape(p["sub"])} {where}" data-cursor="{"View on Behance" if be else "View live"}">
            {cover(p)}
            {badge}
          </a>
          <div class="pc-meta">
            <span class="pc-n">{i:02d}</span>
            <div class="pc-txt"><h3>{html.escape(p["title"])} <em>— {html.escape(p["sub"])}</em></h3><div class="pc-tags">{tags}<span>{p["year"]}</span></div></div>
            <a class="pc-go" href="{p["url"]}" target="_blank" rel="noopener" aria-label="Visit {html.escape(p["title"])} {where}">{ARR}</a>
          </div>
        </article>'''


def section():
    cards = '\n'.join(card(i + 1, p) for i, p in enumerate(PROJECTS))
    return f'''  <!-- WORK -->
  <section id="work" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <div class="rv"><span class="eyebrow">Recent work</span><h2 class="h2">Latest <span class="serif">projects</span> <sup class="pc-count">({len(PROJECTS):02d})</sup></h2></div>
        <a href="https://www.behance.net/noorxtk" target="_blank" rel="noopener" class="btn btn-ghost rv">View all on Behance <span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><path d="M7 17L17 7M8 7h9v9"/></svg></span></a>
      </div>
      <div class="pc-grid">
{cards}
      </div>
    </div>
    <div class="pc-cursor" aria-hidden="true"><span>View live</span>{ARR}</div>
  </section>

'''


CSS = r'''/* Work */
.pc-count{font-family:var(--sans);font-style:normal;font-size:.32em;font-weight:500;color:var(--ink-3);vertical-align:super;letter-spacing:0}
.pc-grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:clamp(18px,2.2vw,28px) 20px}
.pc.s7{grid-column:span 7}.pc.s5{grid-column:span 5}.pc.s12{grid-column:span 12}
.pc-cover{--bg:#111;--ac:#ff5a1f;position:relative;display:block;height:clamp(320px,36vw,500px);border-radius:var(--r-lg);overflow:hidden;isolation:isolate;background:var(--bg);
  clip-path:inset(12% 6% 12% 6% round 32px);transition:clip-path 1.1s cubic-bezier(.7,0,.2,1)}
.pc.in .pc-cover,.pc:not(.rv) .pc-cover{clip-path:inset(0 0 0 0 round 32px)}
.pc.rv{opacity:1;transform:none}
.pc-cover>*{transition:transform 1.1s cubic-bezier(.2,.8,.2,1)}
.pc:not(.in) .pc-cover>*{transform:scale(1.12)}
.pc-live{position:absolute;z-index:5;top:18px;right:18px;display:inline-flex;align-items:center;gap:7px;padding:7px 12px;border-radius:999px;font:600 12px/1 var(--sans);color:#fff;background:rgba(17,17,16,.35);border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}
.pc-live i{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 0 3px rgba(34,197,94,.25)}
.pc-meta{display:flex;align-items:flex-start;gap:16px;margin-top:18px}
.pc-n{font:600 13px/1 var(--sans);color:var(--accent);padding-top:6px}
.pc-txt{flex:1;min-width:0}
.pc-txt h3{font-size:clamp(20px,1.9vw,25px);letter-spacing:-.03em;font-weight:600;line-height:1.2}
.pc-txt h3 em{font-style:normal;font-weight:500;color:var(--ink-3)}
.pc-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.pc-tags span{font-size:12px;font-weight:500;padding:5px 11px;border-radius:999px;border:1px solid var(--line);color:var(--ink-2);background:var(--surface)}
.pc-go{flex:none;width:50px;height:50px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--line);background:var(--surface);transition:background .35s,color .35s,transform .45s cubic-bezier(.2,.8,.2,1),border-color .35s}
.pc-go svg{width:18px;height:18px}
.pc:hover .pc-go{background:var(--accent);border-color:var(--accent);color:#fff;transform:rotate(45deg)}

/* cover: Behance case study */
.be-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.dv-scr img.be-fill{height:100%;object-fit:cover;object-position:center top}
.pc-cover:hover .be-img{transform:scale(1.05)}
.be-cv{position:absolute;inset:0;display:grid;place-items:center;overflow:hidden}
.be-cv::before{content:"";position:absolute;width:70%;aspect-ratio:1;border-radius:50%;background:var(--ac);filter:blur(90px);opacity:.22;transition:transform 1s cubic-bezier(.2,.8,.2,1)}
.pc-cover:hover .be-cv::before{transform:scale(1.25)}
.be-word{position:absolute;left:-2%;bottom:-6%;font:800 clamp(90px,13vw,190px)/1 var(--sans);letter-spacing:-.06em;color:transparent;-webkit-text-stroke:1.5px color-mix(in srgb,var(--ac) 45%,transparent);white-space:nowrap;transition:transform 1.2s cubic-bezier(.2,.8,.2,1)}
.pc-cover:hover .be-word{transform:translateX(4%)}
.be-in{position:relative;text-align:center;padding:24px}
.be-logo{display:inline-flex;align-items:center;gap:8px;font:600 12px/1 var(--sans);color:var(--ink-2);padding:7px 12px;border-radius:999px;background:#fff;box-shadow:0 6px 16px -10px rgba(0,0,0,.3)}
.be-in b{display:block;margin-top:18px;font-size:clamp(30px,3.6vw,52px);letter-spacing:-.04em;line-height:1;color:var(--ink)}
.be-in small{display:block;margin-top:8px;font:400 italic clamp(20px,2vw,28px)/1.1 var(--serif);color:var(--ac)}
.be-cta{display:inline-block;margin-top:22px;font:600 13px/1 var(--sans);color:#fff;background:var(--ink);padding:11px 16px;border-radius:999px;transition:background .3s}
.pc-cover:hover .be-cta{background:var(--ac)}
.pc-live.be b{font:800 12px/1 var(--sans);color:#1769ff}

/* cover: device mockups (full website, scrolls on hover) */
.pc-cover{background:#e9e8e5!important}
.pc-cover::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(70% 60% at 50% 40%,#f6f5f2,transparent 75%)}
.dv-frame{position:absolute;left:8%;right:8%;top:9%;bottom:-2%;padding:6px 6px 0;border-radius:14px 14px 0 0;background:#fdfdfc;box-shadow:0 0 0 1px rgba(17,17,16,.08),0 30px 60px -30px rgba(17,17,16,.35);transition:transform .9s cubic-bezier(.2,.8,.2,1)}
.dv-frame .dv-scr{height:100%;border-radius:9px 9px 0 0}
.pc-cover:hover .dv-frame{transform:translateY(-8px)}
.dv-tab{position:absolute;left:9%;right:9%;top:9%;bottom:9%;padding:2.2%;border-radius:30px;background:#141416;box-shadow:inset 0 0 0 2px #2c2c30,0 40px 70px -30px rgba(17,17,16,.55);transition:transform .9s cubic-bezier(.2,.8,.2,1)}
.dv-tab .dv-cam{top:50%;left:1%;margin:-3px 0 0}
.dv-tab .dv-scr{height:100%;border-radius:14px}
.pc-cover:hover .dv-tab{transform:translateY(-6px) scale(1.01)}
.dv-win{position:absolute;left:8%;right:8%;top:10%;bottom:-3%;border-radius:14px 14px 0 0;overflow:hidden;background:#fff;box-shadow:0 0 0 1px rgba(17,17,16,.08),0 30px 60px -30px rgba(17,17,16,.35);display:flex;flex-direction:column;transition:transform .9s cubic-bezier(.2,.8,.2,1)}
.dv-bar{flex:none;height:32px;display:flex;align-items:center;gap:6px;padding:0 14px;background:#f4f3f0;border-bottom:1px solid #e8e6e1}
.dv-bar i{width:9px;height:9px;border-radius:50%;background:#ff5f57}.dv-bar i:nth-child(2){background:#febc2e}.dv-bar i:nth-child(3){background:#28c840}
.dv-bar span{margin:0 auto;font:500 11.5px/1 var(--sans);color:#8c8a84;padding:6px 44px;border-radius:7px;background:#fff}
.dv-win .dv-scr{flex:1}
.pc-cover:hover .dv-win{transform:translateY(-8px)}
.is-angle .dv-lid,.dv-lid{box-shadow:inset 0 0 0 1.5px #3c3d42,0 40px 70px -30px rgba(17,17,16,.45)}
.pc-live{color:#111;background:rgba(255,255,255,.75);border-color:rgba(17,17,16,.08)}
.dv-scr{position:relative;overflow:hidden;background:#fff}
.dv-scr img{position:absolute;left:0;top:0;width:100%;height:auto;transform:translateY(0);transition:transform var(--dur,5s) cubic-bezier(.45,0,.25,1)}
.pc-cover:hover .dv-scr img{transform:translateY(calc(var(--dist,0) * -1px))}
.dv-laptop{position:absolute;left:50%;top:50%;width:82%;transform:translate(-50%,-50%);transition:transform .9s cubic-bezier(.2,.8,.2,1)}
.dv-lid{position:relative;padding:3.2% 3.2% 3.6%;border-radius:18px 18px 6px 6px;background:linear-gradient(180deg,#2c2d31,#121316);box-shadow:inset 0 0 0 1.5px #3c3d42,0 40px 80px -30px rgba(0,0,0,.7)}
.dv-cam{position:absolute;top:1.2%;left:50%;width:6px;height:6px;margin-left:-3px;border-radius:50%;background:#050506;box-shadow:0 0 0 2px #222}
.dv-laptop .dv-scr{aspect-ratio:16/10;border-radius:4px}
.dv-base{position:relative;height:14px;margin:0 -7%;border-radius:0 0 18px 18px;background:linear-gradient(180deg,#e3e4e8,#a9acb3 55%,#7d8088);box-shadow:0 24px 40px -12px rgba(0,0,0,.6)}
.dv-base::before{content:"";position:absolute;left:50%;top:0;width:18%;height:6px;margin-left:-9%;border-radius:0 0 8px 8px;background:#a3a6ad}
.pc-cover:hover .dv-laptop{transform:translate(-50%,-53%)}
.dv-laptop.tilt{transform:translate(-50%,-50%) perspective(1600px) rotateY(-18deg) rotateX(8deg) rotateZ(1deg)}
.pc-cover:hover .dv-laptop.tilt{transform:translate(-50%,-52%) perspective(1600px) rotateY(-6deg) rotateX(3deg)}
.is-angle .dv-lid{box-shadow:inset 0 0 0 1.5px #3c3d42,30px 40px 70px -24px rgba(20,40,36,.55)}
.dv-imac{position:absolute;left:50%;top:50%;width:min(92%,620px);transform:translate(-50%,-50%);transition:transform .9s cubic-bezier(.2,.8,.2,1)}
.dv-mon{border-radius:16px;padding:2.4% 2.4% 0;background:linear-gradient(180deg,#e9eaee,#c9ccd2);box-shadow:inset 0 0 0 1px rgba(255,255,255,.6),0 40px 80px -24px rgba(0,0,0,.75);overflow:hidden}
.dv-imac .dv-scr{aspect-ratio:16/10;border-radius:6px;background:#111;box-shadow:0 0 0 6px #0c0c0e}
.dv-chin{height:clamp(24px,3vw,36px);margin:0 -3%;margin-top:10px;background:linear-gradient(180deg,#d7d9de,#b9bcc3)}
.dv-neck{width:18%;height:clamp(36px,4.6vw,64px);margin:0 auto;background:linear-gradient(90deg,#9ea1a8,#d5d7dc 50%,#9ea1a8);clip-path:polygon(12% 0,88% 0,100% 100%,0 100%)}
.dv-foot{width:38%;height:10px;margin:0 auto;border-radius:6px 6px 10px 10px;background:linear-gradient(180deg,#d5d7dc,#9ea1a8);box-shadow:0 16px 30px -8px rgba(0,0,0,.6)}
.pc-cover:hover .dv-imac{transform:translate(-50%,calc(-50% - 6px))}

/* cursor bubble */
.pc-cursor{position:fixed;left:0;top:0;z-index:60;width:104px;height:104px;margin:-52px 0 0 -52px;border-radius:50%;display:grid;place-items:center;align-content:center;gap:2px;pointer-events:none;
  background:var(--accent);color:#fff;font:600 13px/1.1 var(--sans);text-align:center;transform:translate(var(--x,-200px),var(--y,-200px)) scale(0);transition:transform .35s cubic-bezier(.2,.8,.2,1);box-shadow:0 16px 40px -12px rgba(255,90,31,.8)}
.pc-cursor svg{width:16px;height:16px;justify-self:center}
.pc-cursor.on{transform:translate(var(--x),var(--y)) scale(1)}
@media (hover:none),(pointer:coarse){.pc-cursor{display:none}}

@media (max-width:880px){.pc.s7,.pc.s5,.pc.s12{grid-column:span 12}.pc-cover{height:clamp(280px,64vw,420px)}}
@media (max-width:560px){.cv-bento{grid-template-columns:1fr 1fr}.bt.c{display:none}.cv-rphone{width:30%}.cv-sphone{width:24%}.cv-pill{font-size:11px;padding:9px 13px}.cv-chip{font-size:11px}.cv-stat{font-size:11px;padding:9px 12px}}
@media (prefers-reduced-motion:reduce){.pc-cover{clip-path:none!important;transition:none}.pc-cover>*,.pc-cover *{transition:none!important;animation:none!important;transform:none!important}}

'''

JS = r'''  (() => {
    const cur = document.querySelector('.pc-cursor'); if (!cur || matchMedia('(hover: none)').matches) return;
    const fit = (img) => { const scr = img.parentElement, d = Math.max(0, img.offsetHeight - scr.clientHeight); img.style.setProperty('--dist', d); img.style.setProperty('--dur', Math.min(9, Math.max(3, d / 450)) + 's'); };
    document.querySelectorAll('.dv-scr img').forEach((img) => { img.complete ? fit(img) : img.addEventListener('load', () => fit(img)); });
    addEventListener('resize', () => document.querySelectorAll('.dv-scr img').forEach(fit));
    document.querySelectorAll('.pc-cover [data-d]').forEach((el) => el.style.setProperty('--dd', el.dataset.d));
    document.querySelectorAll('.pc-cover').forEach((c) => {
      c.addEventListener('pointermove', (e) => { const r = c.getBoundingClientRect(); c.style.setProperty('--px', ((e.clientX - r.left) / r.width - .5) * 2); c.style.setProperty('--py', ((e.clientY - r.top) / r.height - .5) * 2); });
      c.addEventListener('pointerleave', () => { c.style.setProperty('--px', 0); c.style.setProperty('--py', 0); });
    });
    document.querySelectorAll('.pc-cover').forEach((c) => {
      c.addEventListener('pointerenter', () => { cur.querySelector('span').textContent = c.dataset.cursor || 'View live'; cur.classList.add('on'); });
      c.addEventListener('pointerleave', () => cur.classList.remove('on'));
    });
    addEventListener('pointermove', (e) => { cur.style.setProperty('--x', e.clientX + 'px'); cur.style.setProperty('--y', e.clientY + 'px'); }, { passive: true });
  })();
'''

if __name__ == '__main__':
    path = sys.argv[1]
    s = open(path, encoding='utf-8').read()
    # replace the WORK section in place
    s = re.sub(r'  <!-- WORK -->.*?(?=  <!-- [A-Z]+ -->)', lambda _: section(), s, count=1, flags=re.S)
    s = re.sub(r'/\* Work \*/.*?(?=/\* Process \*/)', lambda _: CSS, s, count=1, flags=re.S)
    s = re.sub(r"  \(\(\) => \{\n    const cur = document\.querySelector\('\.pc-cursor'\).*?\n  \}\)\(\);\n", "", s, count=1, flags=re.S)
    if True:
        s = s.replace("  document.getElementById('yr').textContent", JS + "  document.getElementById('yr').textContent", 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('cards', s.count('<article class="pc '))
