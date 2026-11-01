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
    dict(slug="content-writing-ai-website", style="laptop", span=7, title="Quantum", sub="AI Content Writing Website",
         tags=["AI SaaS", "Web Design", "Next.js"], url="https://content-writing-ai-website.vercel.app/",
         bg="#0b0716", accent="#8b5cf6", year="2026"),
    dict(slug="project-management-saas-website", style="float", span=5, title="WorkUp", sub="Project Management SaaS",
         tags=["SaaS", "UI/UX", "Dashboard"], url="https://project-management-saa-s-website.vercel.app/",
         bg="#5b3df5", accent="#c4b5fd", year="2026", chips=["+ Add task", "Sprint 12 · 75%"]),
    dict(slug="fitness-training-website", style="rise", span=5, title="Gymnastic", sub="Fitness Training Website",
         tags=["Fitness", "Web Design"], url="https://fitness-training-website-bay.vercel.app/",
         bg="#061a1d", accent="#22d3ee", year="2026", logo="GYMNASTIC", cta="Be a Member"),
    dict(slug="cryptocurrency-website", style="phone", span=7, title="Lumino", sub="Bitcoin Mining Platform",
         tags=["Crypto", "Fintech", "Web Design"], url="https://cryptocurrency-website-development.vercel.app/",
         bg="#0a0b2e", accent="#7c5cff", year="2026", chips=["Total deposits $8M+", "Active users 125k+"]),
    dict(slug="rent-a-car-website", style="showcase", span=7, title="Rent", sub="Car Rental Website · Dubai",
         tags=["Car Rental", "Booking UX", "Next.js"], url="https://rent-a-car-website-eight.vercel.app/",
         bg="#ff8a3d", accent="#1d72e8", year="2026", logo="Rent", cta="Book in 60 sec"),
    dict(slug="nattoral", style="bento", span=5, title="Nattoral", sub="Skincare E-commerce Store",
         tags=["E-commerce", "Beauty", "UI/UX"], url="https://nattoral-zeta.vercel.app/",
         bg="#dfe9e5", accent="#2f4f4a", year="2026", logo="NATTORAL", swatches=["#2f4f4a", "#9bc7c0", "#e9e3d6", "#111111"]),
]

ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'


def shot(p, kind, cls, alt=""):
    return f'<img class="{cls}" src="/assets/work/shots/{p["slug"]}-{kind}.webp" alt="{alt}" loading="lazy" decoding="async">'


def cover(p):
    e = lambda k: html.escape(p.get(k, ""))
    st = p["style"]
    if st == "laptop":
        return (f'<img class="cv-full" src="/assets/work/{p["slug"]}.webp" srcset="/assets/work/{p["slug"]}-800.webp 800w, /assets/work/{p["slug"]}.webp 1200w" '
                f'sizes="(max-width:880px) 92vw, 680px" alt="{e("title")} — {e("sub")} on laptop and phone" loading="lazy" decoding="async">')
    if st == "float":
        chips = ''.join(f'<span class="cv-chip c{i}">{html.escape(c)}</span>' for i, c in enumerate(p["chips"]))
        return f'<div class="cv-float"><div class="cv-screen">{shot(p, "d", "", e("title") + " dashboard")}</div>{chips}</div>'
    if st == "bleed":
        return (f'{shot(p, "d", "cv-bg", e("title") + " website")}<span class="cv-word" aria-hidden="true">{e("word")}</span>'
                f'<div class="cv-peek">{shot(p, "m", "")}</div>')
    if st == "phone":
        chips = ''.join(f'<span class="cv-stat s{i}">{html.escape(c)}</span>' for i, c in enumerate(p["chips"]))
        return f'<div class="cv-glow"></div><div class="cv-phone"><span class="cv-isl"></span>{shot(p, "m", "", e("title") + " mobile")}</div>{chips}'
    if st == "browser":
        return (f'<span class="cv-mark" aria-hidden="true">{e("word")}</span><div class="cv-win"><div class="cv-bar"><i></i><i></i><i></i><span>{e("title").lower()}.com</span></div>'
                f'<div class="cv-view">{shot(p, "d", "", e("title") + " website")}</div></div>')
    if st == "split":
        sw = ''.join(f'<i style="background:{c}"></i>' for c in p["swatches"])
        return (f'<div class="cv-sframe">{shot(p, "d", "", e("title") + " store")}</div>'
                f'<div class="cv-guide"><small>Colors</small><div class="cv-sw">{sw}</div><small>Type</small><b>Aa</b><span>Elegant Serif · Inter</span></div>')
    if st == "rise":
        return (f'<div class="cv-halo"></div><span class="cv-logo" data-d="-0.4">{e("logo")}</span>'
                f'<div class="cv-rise" data-d="0.4">{shot(p, "d", "", e("title") + " website")}</div>'
                f'<div class="cv-rphone" data-d="1">{shot(p, "m", "")}</div>'
                f'<span class="cv-pill" data-d="1.4">{e("cta")} ↗</span>')
    if st == "showcase":
        return (f'<span class="cv-logo dark" data-d="-0.4">{e("logo")}</span>'
                f'<div class="cv-back" data-d="0.3">{shot(p, "d", "", e("title") + " website")}</div>'
                f'<div class="cv-car" data-d="1.2"><img src="/assets/work/shots/{p["slug"]}-car.webp" alt="" loading="lazy"></div>'
                f'<div class="cv-search" data-d="0.8"><img src="/assets/work/shots/{p["slug"]}-search.webp" alt="" loading="lazy"></div>'
                f'<div class="cv-sphone" data-d="1.6">{shot(p, "m", "")}</div>')
    if st == "bento":
        sw = ''.join(f'<i style="background:{c}"></i>' for c in p["swatches"])
        return (f'<div class="cv-bento">'
                f'<div class="bt a" data-d="0.5"><img src="/assets/work/shots/{p["slug"]}-product.webp" alt="{e("title")} products" loading="lazy"></div>'
                f'<div class="bt b" data-d="0.9"><img src="/assets/work/shots/{p["slug"]}-hero.webp" alt="" loading="lazy"></div>'
                f'<div class="bt c" data-d="1.2"><span class="bl">{e("logo")}</span><div class="cv-sw">{sw}</div></div>'
                f'<div class="bt d" data-d="1.5">{shot(p, "m", "")}</div></div>')
    raise ValueError(st)


def card(i, p):
    tags = ''.join(f'<span>{html.escape(t)}</span>' for t in p["tags"])
    style = f'--bg:{p["bg"]};--ac:{p["accent"]}'
    return f'''        <article class="pc s{p["span"]} rv" data-style="{p["style"]}">
          <a class="pc-cover is-{p["style"]}" href="{p["url"]}" target="_blank" rel="noopener" style="{style}" aria-label="Open {html.escape(p["title"])} — {html.escape(p["sub"])} (live site)">
            {cover(p)}
            <span class="pc-live"><i></i>Live</span>
          </a>
          <div class="pc-meta">
            <span class="pc-n">{i:02d}</span>
            <div class="pc-txt"><h3>{html.escape(p["title"])} <em>— {html.escape(p["sub"])}</em></h3><div class="pc-tags">{tags}<span>{p["year"]}</span></div></div>
            <a class="pc-go" href="{p["url"]}" target="_blank" rel="noopener" aria-label="Visit {html.escape(p["title"])} live site">{ARR}</a>
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
.pc.s7{grid-column:span 7}.pc.s5{grid-column:span 5}
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

/* cover: laptop */
.is-laptop .cv-full{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.is-laptop:hover .cv-full{transform:scale(1.05)}
/* cover: float */
.cv-float{position:absolute;inset:0;perspective:1400px;background:radial-gradient(80% 70% at 70% 20%,var(--ac),transparent 60%)}
.cv-float .cv-screen{position:absolute;left:12%;top:18%;width:96%;border-radius:14px;overflow:hidden;box-shadow:0 40px 80px -30px rgba(10,5,40,.75),0 0 0 6px rgba(255,255,255,.18);transform:rotateX(22deg) rotateY(-14deg) rotateZ(6deg);transform-origin:left top;transition:transform 1s cubic-bezier(.2,.8,.2,1)}
.cv-float .cv-screen img{display:block;width:100%}
.pc-cover.is-float:hover .cv-screen{transform:rotateX(10deg) rotateY(-6deg) rotateZ(2deg) translateY(-10px)}
.cv-chip{position:absolute;padding:10px 14px;border-radius:14px;font:600 13px/1 var(--sans);color:#1b1446;background:#fff;box-shadow:0 18px 30px -14px rgba(10,5,40,.6);animation:bob 5s ease-in-out infinite}
.cv-chip.c0{left:8%;top:12%}.cv-chip.c1{left:14%;bottom:12%;animation-delay:-2.5s;background:#1b1446;color:#fff}
/* cover: phone */
.cv-glow{position:absolute;inset:0;background:radial-gradient(40% 55% at 50% 55%,var(--ac),transparent 70%),repeating-linear-gradient(90deg,rgba(255,255,255,.05) 0 1px,transparent 1px 46px),repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 46px);opacity:.9}
.cv-phone{position:absolute;left:50%;top:12%;width:min(34%,230px);margin-left:calc(min(34%,230px) / -2);border-radius:36px;padding:9px;background:#111;box-shadow:0 0 0 2px #2a2a2e inset,0 50px 90px -30px rgba(0,0,0,.85);transform:rotate(-4deg)}
.cv-phone img{display:block;width:100%;border-radius:28px}
.cv-isl{position:absolute;z-index:2;top:18px;left:50%;width:30%;height:16px;margin-left:-15%;border-radius:10px;background:#000}
.pc-cover.is-phone:hover .cv-phone{transform:rotate(0) translateY(-14px) scale(1.03)}
.cv-stat{position:absolute;z-index:3;padding:12px 16px;border-radius:16px;font:600 13px/1.25 var(--sans);color:#fff;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);animation:bob 6s ease-in-out infinite}
.cv-stat.s0{left:8%;top:22%}.cv-stat.s1{right:8%;bottom:20%;animation-delay:-3s}
/* cover: rise (Gymnastic) */
.cv-halo{position:absolute;inset:0;background:radial-gradient(55% 60% at 50% 100%,rgba(34,211,238,.55),transparent 70%),radial-gradient(40% 40% at 85% 10%,rgba(34,211,238,.25),transparent 70%),repeating-linear-gradient(90deg,rgba(255,255,255,.04) 0 1px,transparent 1px 40px),repeating-linear-gradient(0deg,rgba(255,255,255,.04) 0 1px,transparent 1px 40px)}
.cv-logo{position:absolute;z-index:4;left:50%;top:7%;transform:translateX(-50%);padding:9px 16px;border-radius:999px;font:800 13px/1 var(--sans);letter-spacing:.14em;color:#fff;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);white-space:nowrap}
.cv-logo.dark{left:7%;transform:none;color:#1a1208;background:rgba(255,255,255,.55);border-color:rgba(255,255,255,.7);letter-spacing:.02em;font-size:15px}
.cv-rise{position:absolute;left:9%;right:9%;top:22%;bottom:-6%;border-radius:18px 18px 0 0;overflow:hidden;border:6px solid rgba(255,255,255,.12);border-bottom:0;box-shadow:0 -20px 60px -10px rgba(34,211,238,.45)}
.cv-rise{background:#121212}
.cv-rise img{width:100%;height:100%;object-fit:cover;object-position:left top;display:block}
.cv-rphone{position:absolute;z-index:3;right:5%;bottom:-16%;width:25%;border-radius:24px;overflow:hidden;border:5px solid #0b0b0c;box-shadow:0 30px 60px -20px rgba(0,0,0,.8)}
.cv-rphone img{width:100%;display:block}
.cv-pill{position:absolute;z-index:4;left:6%;bottom:12%;padding:12px 18px;border-radius:999px;font:700 13px/1 var(--sans);color:#06292e;background:#22d3ee;box-shadow:0 14px 30px -10px rgba(34,211,238,.8)}
/* cover: showcase (Rent) */
.is-showcase{background:linear-gradient(140deg,#ffb37a 0%,#ff8a3d 45%,#f26b1d 100%)!important}
.is-showcase::before{content:"";position:absolute;inset:0;background:radial-gradient(50% 60% at 75% 30%,rgba(255,255,255,.45),transparent 70%)}
.cv-back{position:absolute;left:7%;top:20%;width:62%;border-radius:14px;overflow:hidden;box-shadow:0 30px 60px -24px rgba(120,40,0,.55);border:5px solid rgba(255,255,255,.7)}
.cv-back img{width:100%;display:block}
.cv-car{position:absolute;z-index:2;right:6%;top:13%;width:44%;border-radius:22px;overflow:hidden;background:#f3f4f8;box-shadow:0 30px 60px -20px rgba(120,40,0,.6)}
.cv-car img{width:100%;display:block}
.cv-search{position:absolute;z-index:3;left:9%;right:27%;bottom:9%;border-radius:14px;overflow:hidden;box-shadow:0 26px 50px -16px rgba(80,25,0,.55)}
.cv-search img{width:100%;display:block}
.cv-sphone{position:absolute;z-index:4;right:6%;bottom:-18%;width:19%;border-radius:22px;overflow:hidden;border:5px solid #111;box-shadow:0 30px 60px -20px rgba(0,0,0,.6)}
.cv-sphone img{width:100%;display:block}
/* cover: bento (Nattoral) */
.cv-bento{position:absolute;inset:6%;display:grid;grid-template-columns:1.05fr 1fr .7fr;grid-template-rows:1fr 1fr;gap:10px}
.bt{border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 18px 36px -24px rgba(20,40,36,.55)}
.bt img{width:100%;height:100%;object-fit:cover;display:block}
.bt.a{grid-row:span 2}
.bt.b{grid-column:span 2}
.bt.b img{object-position:85% center}
.bt.c{display:flex;flex-direction:column;justify-content:space-between;padding:14px;background:#2f4f4a;color:#e9e3d6}
.bl{font:500 15px/1 Georgia,var(--serif);letter-spacing:.18em}
.bt.c .cv-sw{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.bt.c .cv-sw i{aspect-ratio:1;border-radius:8px;box-shadow:0 0 0 1px rgba(255,255,255,.25)}
.bt.d{position:relative;background:#111;padding:4px}
.bt.d img{border-radius:12px;object-position:top}
/* parallax layers */
.pc-cover [data-d]{transition:transform .7s cubic-bezier(.2,.8,.2,1);transform:translate(calc(var(--px,0) * var(--dd,0) * 10px),calc(var(--py,0) * var(--dd,0) * 10px))}
.cv-logo[data-d]{transform:translate(calc(-50% + var(--px,0) * var(--dd,0) * 10px),calc(var(--py,0) * var(--dd,0) * 10px))}
.cv-logo.dark[data-d]{transform:translate(calc(var(--px,0) * var(--dd,0) * 10px),calc(var(--py,0) * var(--dd,0) * 10px))}
.pc-cover:hover .cv-rise{bottom:-2%}
.pc-cover:hover .cv-rphone,.pc-cover:hover .cv-sphone{bottom:-10%}
.pc-cover:hover .bt{box-shadow:0 26px 44px -22px rgba(20,40,36,.6)}

/* cursor bubble */
.pc-cursor{position:fixed;left:0;top:0;z-index:60;width:104px;height:104px;margin:-52px 0 0 -52px;border-radius:50%;display:grid;place-items:center;align-content:center;gap:2px;pointer-events:none;
  background:var(--accent);color:#fff;font:600 13px/1.1 var(--sans);text-align:center;transform:translate(var(--x,-200px),var(--y,-200px)) scale(0);transition:transform .35s cubic-bezier(.2,.8,.2,1);box-shadow:0 16px 40px -12px rgba(255,90,31,.8)}
.pc-cursor svg{width:16px;height:16px;justify-self:center}
.pc-cursor.on{transform:translate(var(--x),var(--y)) scale(1)}
@media (hover:none),(pointer:coarse){.pc-cursor{display:none}}

@media (max-width:880px){.pc.s7,.pc.s5{grid-column:span 12}.pc-cover{height:clamp(280px,64vw,420px)}}
@media (max-width:560px){.cv-bento{grid-template-columns:1fr 1fr}.bt.c{display:none}.cv-rphone{width:30%}.cv-sphone{width:24%}.cv-pill{font-size:11px;padding:9px 13px}.cv-chip{font-size:11px}.cv-stat{font-size:11px;padding:9px 12px}}
@media (prefers-reduced-motion:reduce){.pc-cover{clip-path:none!important;transition:none}.pc-cover>*,.pc-cover *{transition:none!important;animation:none!important;transform:none!important}}

'''

JS = r'''  (() => {
    const cur = document.querySelector('.pc-cursor'); if (!cur || matchMedia('(hover: none)').matches) return;
    document.querySelectorAll('.pc-cover [data-d]').forEach((el) => el.style.setProperty('--dd', el.dataset.d));
    document.querySelectorAll('.pc-cover').forEach((c) => {
      c.addEventListener('pointermove', (e) => { const r = c.getBoundingClientRect(); c.style.setProperty('--px', ((e.clientX - r.left) / r.width - .5) * 2); c.style.setProperty('--py', ((e.clientY - r.top) / r.height - .5) * 2); });
      c.addEventListener('pointerleave', () => { c.style.setProperty('--px', 0); c.style.setProperty('--py', 0); });
    });
    document.querySelectorAll('.pc-cover').forEach((c) => {
      c.addEventListener('pointerenter', () => cur.classList.add('on'));
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
