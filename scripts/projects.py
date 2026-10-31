"""Regenerate the Recent Work section of index.html from PROJECTS data."""
import html, re, sys

PROFILE = "https://www.behance.net/noorxtk"

# Newest first.
PROJECTS = [
    # Direct Behance gallery links (newest first by gallery ID)
    dict(title="Gym Landing Page", cat="Landing Page · Fitness", url="https://www.behance.net/gallery/186135665/Gym-Landing-Page-ui-ui-design-uiux-design", emoji="🏋️",
         head="Build your best body", stat="12k members", a="#ef4444", b="#fb923c", bg1="#140707", bg2="#dc2626"),
    dict(title="Bitcoin Mining Landing Page", cat="Landing Page · Crypto", url="https://www.behance.net/gallery/182492455/Bitcoin-Mining-Landing-Page-UI-Design-UIUX-Design", emoji="₿",
         head="Mine Bitcoin smarter", stat="+24.8% today", a="#f59e0b", b="#fde047", bg1="#0b0b14", bg2="#b45309"),
    dict(title="Car Rental Website Landing Page", cat="Landing Page · Car Rental", url="https://www.behance.net/gallery/179879931/Car-Rental-Website-Landing-Page-UI-Design-UIUX-Design", emoji="🚗",
         head="Drive your dream car", stat="4.9★ rated", a="#ff5a1f", b="#ffb347", bg1="#1a0f0a", bg2="#ff5a1f"),
    dict(title="Storage Management Dashboard", cat="Dashboard · SaaS", url="https://www.behance.net/gallery/168541189/Storage-Management-Dashboard-ui-ui-Design-uiux-Design", emoji="🗂️",
         head="All your files, organized", stat="1.2 TB used", a="#4f46e5", b="#38bdf8", bg1="#0a0c1f", bg2="#4f46e5"),
    dict(title="Cloud Storage Dashboard", cat="Dashboard · SaaS", url="https://www.behance.net/gallery/165367125/Cloud-Storage-Dashboard-UIUX-and-UI-Design", emoji="☁️",
         head="Your cloud, simplified", stat="99.9% uptime", a="#0ea5e9", b="#22d3ee", bg1="#04131c", bg2="#0284c7"),
    # Real projects on the profile; replace url with the gallery link when available
    dict(title="SaaS Landing Page", cat="Landing Page · SaaS", url=PROFILE, emoji="🚀",
         head="Grow your SaaS faster", stat="+38% signups", a="#7c3aed", b="#c084fc", bg1="#100820", bg2="#7c3aed"),
    dict(title="Crypto Management Dashboard", cat="Dashboard · Fintech", url=PROFILE, emoji="📈",
         head="Track every coin", stat="$48,920 balance", a="#16a34a", b="#a3e635", bg1="#06180d", bg2="#15803d"),
    dict(title="Project Management Landing Page", cat="Landing Page · SaaS", url=PROFILE, emoji="✅",
         head="Ship projects on time", stat="98% on time", a="#2563eb", b="#60a5fa", bg1="#06102a", bg2="#1d4ed8"),
    dict(title="Interior Design Landing Page", cat="Landing Page · Interior", url=PROFILE, emoji="🛋️",
         head="Design spaces you love", stat="500+ homes", a="#a16207", b="#fcd34d", bg1="#17110a", bg2="#92400e"),
    dict(title="Marketing Agency Landing Page", cat="Landing Page · Agency", url=PROFILE, emoji="📣",
         head="Marketing that converts", stat="3x ROI", a="#db2777", b="#f9a8d4", bg1="#16061a", bg2="#be185d"),
]

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M8 7h9v9"/></svg>'


def card(i, p):
    e = {k: html.escape(v, quote=True) for k, v in p.items()}
    style = f"--a:{e['a']};--b:{e['b']};--bg1:{e['bg1']};--bg2:{e['bg2']}"
    return f'''        <article class="pj rv">
          <a class="pj-cover" href="{e['url']}" target="_blank" rel="noopener" style="{style}" aria-label="View {e['title']} on Behance">
            <div class="mk" aria-hidden="true">
              <div class="mk-browser">
                <div class="mk-bar"><i></i><i></i><i></i><span></span></div>
                <div class="mk-site">
                  <div class="mk-nav"><b></b><span></span><span></span><span></span><em></em></div>
                  <div class="mk-hero">
                    <div class="mk-copy"><strong>{e['head']}</strong><span></span><span></span><em>Get started</em></div>
                    <div class="mk-visual"><span class="mk-emoji">{e['emoji']}</span><span class="mk-chip">{e['stat']}</span></div>
                  </div>
                  <div class="mk-cards"><i></i><i></i><i></i></div>
                </div>
              </div>
              <div class="mk-phone">
                <div class="mk-notch"></div>
                <div class="mk-app"><span class="mk-emoji">{e['emoji']}</span><strong>{e['head']}</strong><i></i><i></i><i></i><em></em></div>
              </div>
            </div>
            <span class="pj-num">{i:02d}</span>
          </a>
          <div class="pj-meta">
            <div><h3>{e['title']}</h3><p>{e['cat']}</p></div>
            <a class="pj-arrow" href="{e['url']}" target="_blank" rel="noopener" aria-label="Open {e['title']} on Behance">{ARROW}</a>
          </div>
        </article>'''


SECTION = '''  <!-- WORK -->
  <section id="work" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <div class="rv"><span class="eyebrow">Recent work</span><h2 class="h2">Latest <span class="serif">projects</span></h2></div>
        <a href="''' + PROFILE + '''" target="_blank" rel="noopener" class="btn btn-ghost rv">View all on Behance <span class="arr"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><path d="M7 17L17 7M8 7h9v9"/></svg></span></a>
      </div>
      <div class="work">
''' + "\n".join(card(i + 1, p) for i, p in enumerate(PROJECTS)) + '''
      </div>
    </div>
  </section>

'''

CSS = r'''/* Work */
.work{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(20px,2.5vw,32px)}
.pj-cover{position:relative;display:block;aspect-ratio:4/3;border-radius:var(--r-lg);overflow:hidden;container-type:inline-size;isolation:isolate;
  background:radial-gradient(90% 80% at 85% 10%,color-mix(in srgb,var(--bg2) 85%,transparent),transparent 60%),radial-gradient(70% 70% at 0% 100%,color-mix(in srgb,var(--b) 35%,transparent),transparent 60%),var(--bg1)}
.pj-cover::before{content:"";position:absolute;inset:0;z-index:-1;opacity:.5;background:repeating-linear-gradient(90deg,rgba(255,255,255,.05) 0 1px,transparent 1px 8cqw),repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 8cqw);mask-image:radial-gradient(80% 80% at 50% 40%,#000,transparent)}
.pj-cover::after{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08);pointer-events:none}
.pj-num{position:absolute;top:4cqw;left:4.5cqw;font:600 2.6cqw/1 var(--sans);color:rgba(255,255,255,.55);letter-spacing:.05em}
.mk{position:absolute;inset:0;perspective:1400px}
.mk-browser{position:absolute;left:7%;top:15%;width:72%;aspect-ratio:16/10.5;background:#fff;border-radius:1.6cqw;overflow:hidden;
  transform:rotateY(14deg) rotateX(6deg) rotateZ(-2deg);transform-origin:left center;
  box-shadow:0 4cqw 8cqw -2cqw rgba(0,0,0,.55),0 0 0 .3cqw rgba(255,255,255,.15);transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.mk-bar{height:4.2%;min-height:2.4cqw;background:#f1f1f3;display:flex;align-items:center;gap:.7cqw;padding:0 1.4cqw}
.mk-bar i{width:1cqw;height:1cqw;border-radius:50%;background:#ff5f57}.mk-bar i:nth-child(2){background:#febc2e}.mk-bar i:nth-child(3){background:#28c840}
.mk-bar span{margin-left:auto;margin-right:auto;width:30%;height:1.2cqw;border-radius:1cqw;background:#e4e4e7}
.mk-site{padding:2.4cqw 3cqw;height:calc(100% - 2.4cqw);display:flex;flex-direction:column;gap:2.4cqw}
.mk-nav{display:flex;align-items:center;gap:1.6cqw}
.mk-nav b{width:2.6cqw;height:2.6cqw;border-radius:.8cqw;background:linear-gradient(135deg,var(--a),var(--b));margin-right:auto}
.mk-nav span{width:5cqw;height:.9cqw;border-radius:1cqw;background:#e4e4e7}
.mk-nav em{width:8cqw;height:2.6cqw;border-radius:2cqw;background:var(--a)}
.mk-hero{flex:1;display:grid;grid-template-columns:1.15fr 1fr;gap:2.4cqw;align-items:center}
.mk-copy strong{display:block;font:700 3.6cqw/1.02 var(--sans);letter-spacing:-.04em;color:#0b0b0c;margin-bottom:1.6cqw}
.mk-copy span{display:block;height:.9cqw;border-radius:1cqw;background:#e4e4e7;margin-bottom:.9cqw;width:92%}
.mk-copy span+span{width:70%}
.mk-copy em{display:inline-block;margin-top:1.4cqw;font:600 1.5cqw/1 var(--sans);font-style:normal;color:#fff;background:#0b0b0c;padding:1.1cqw 2cqw;border-radius:2cqw}
.mk-visual{position:relative;aspect-ratio:1;border-radius:2cqw;background:radial-gradient(circle at 30% 25%,var(--b),var(--a) 70%);display:grid;place-items:center;overflow:hidden}
.mk-visual::before{content:"";position:absolute;width:70%;aspect-ratio:1;border-radius:50%;border:.3cqw solid rgba(255,255,255,.35)}
.mk-emoji{font-size:9cqw;line-height:1;filter:drop-shadow(0 1cqw 1.5cqw rgba(0,0,0,.3))}
.mk-chip{position:absolute;bottom:6%;left:6%;font:600 1.4cqw/1 var(--sans);background:rgba(255,255,255,.92);color:#0b0b0c;padding:.9cqw 1.4cqw;border-radius:2cqw}
.mk-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6cqw;height:16%}
.mk-cards i{border-radius:1.2cqw;background:#f4f4f5}
.mk-cards i:first-child{background:color-mix(in srgb,var(--a) 14%,#fff)}
.mk-phone{position:absolute;right:7%;bottom:-6%;width:24%;aspect-ratio:9/19;background:#0b0b0c;border-radius:4cqw;padding:1cqw;
  transform:rotate(-7deg) translateY(0);box-shadow:0 4cqw 7cqw -1cqw rgba(0,0,0,.6),inset 0 0 0 .35cqw #2a2a2e;transition:transform .7s cubic-bezier(.2,.8,.2,1)}
.mk-notch{position:absolute;top:2cqw;left:50%;transform:translateX(-50%);width:32%;height:1.8cqw;border-radius:2cqw;background:#0b0b0c;z-index:1}
.mk-app{height:100%;border-radius:3.2cqw;background:linear-gradient(180deg,color-mix(in srgb,var(--b) 30%,#fff),#fff 45%);padding:5.5cqw 1.8cqw 2cqw;display:flex;flex-direction:column;gap:1cqw}
.mk-app .mk-emoji{font-size:5.5cqw}
.mk-app strong{font:700 2cqw/1.05 var(--sans);letter-spacing:-.03em;color:#0b0b0c;margin:.6cqw 0 .8cqw}
.mk-app i{display:block;height:4.4cqw;border-radius:1.2cqw;background:#f4f4f5}
.mk-app i:first-of-type{background:color-mix(in srgb,var(--a) 18%,#fff)}
.mk-app em{margin-top:auto;height:3cqw;border-radius:2cqw;background:var(--a)}
.pj:hover .mk-browser{transform:rotateY(8deg) rotateX(3deg) rotateZ(-1deg) translateY(-1.5cqw)}
.pj:hover .mk-phone{transform:rotate(-3deg) translateY(-3cqw)}
.pj-meta{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:18px}
.pj-meta h3{font-size:clamp(19px,1.8vw,22px);letter-spacing:-.025em;font-weight:600;line-height:1.2}
.pj-meta p{color:var(--ink-3);font-size:14px;margin-top:4px}
.pj-arrow{flex:none;width:52px;height:52px;border-radius:50%;display:grid;place-items:center;background:var(--surface);border:1px solid var(--line);transition:background .3s,color .3s,transform .3s cubic-bezier(.2,.8,.2,1),border-color .3s}
.pj-arrow svg{width:20px;height:20px;transition:transform .3s}
.pj-arrow:hover,.pj:hover .pj-arrow{background:var(--accent);border-color:var(--accent);color:#fff}
.pj-arrow:hover svg{transform:rotate(45deg)}
@media (max-width:760px){.work{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){.pj:hover .mk-browser,.pj:hover .mk-phone{transform:none}}

'''

path = sys.argv[1]
src = open(path, encoding="utf-8").read()
src = re.sub(r"/\* Work \*/.*?(?=/\* Process \*/)", lambda m: CSS, src, count=1, flags=re.S)
src = re.sub(r"  <!-- WORK -->.*?(?=  <!-- PROCESS -->)", lambda m: SECTION, src, count=1, flags=re.S)
open(path, "w", encoding="utf-8").write(src)
print("ok", src.count('class="pj rv"'), "cards")
