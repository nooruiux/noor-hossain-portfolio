"""Write the site's security headers (incl. a hash-based CSP) into vercel.json.

Inline <script> blocks are allowed by SHA-256 hash, so any edit to an inline
script needs this to be re-run (scripts/projects.py calls it automatically):

    python3 scripts/csp.py
"""
import base64, hashlib, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

hashes = []
for attrs, body in re.findall(r'<script([^>]*)>(.*?)</script>', html, re.S):
    if 'src=' in attrs:
        continue
    t = re.search(r'type="([^"]+)"', attrs)
    if t and t.group(1) not in ('text/javascript', 'module'):
        continue  # JSON / JSON-LD data blocks are never executed
    hashes.append("'sha256-" + base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode() + "'")

csp = '; '.join([
    "default-src 'self'",
    "script-src 'self' " + ' '.join(hashes),
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data:",
    "connect-src 'self'",
    "frame-src https://calendly.com",
    "child-src https://calendly.com",
    "media-src 'none'",
    "object-src 'none'",
    "worker-src 'none'",
    "manifest-src 'self'",
    "base-uri 'none'",
    "form-action 'self' mailto:",
    "frame-ancestors 'none'",
    "upgrade-insecure-requests",
])

security = [
    {"key": "Content-Security-Policy", "value": csp},
    {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
    {"key": "X-Content-Type-Options", "value": "nosniff"},
    {"key": "X-Frame-Options", "value": "DENY"},
    {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
    {"key": "Permissions-Policy", "value": "accelerometer=(), autoplay=(), camera=(), display-capture=(), encrypted-media=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), midi=(), payment=(), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), xr-spatial-tracking=(), browsing-topics=(), interest-cohort=()"},
    {"key": "Cross-Origin-Opener-Policy", "value": "same-origin"},
    {"key": "Cross-Origin-Resource-Policy", "value": "same-origin"},
    {"key": "X-Permitted-Cross-Domain-Policies", "value": "none"},
    {"key": "X-DNS-Prefetch-Control", "value": "on"},
]

path = os.path.join(ROOT, 'vercel.json')
cfg = json.load(open(path))
cfg['headers'] = [
    {"source": "/(.*)", "headers": security},
    {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
    {"source": "/", "headers": [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]},
]
cfg['redirects'] = [
    {"source": "/index.html", "destination": "/", "permanent": True},
]
json.dump(cfg, open(path, 'w'), indent=2)
open(path, 'a').write('\n')
print('csp: %d inline script hash(es) written to vercel.json' % len(hashes))
