#!/usr/bin/env python3
"""The Vijayran Palace — static site generator (Sujan design system).
python3 build.py  ->  ./dist   (every page keeps its existing royalquestresorts.com URL)"""
import os, shutil, html, json
from data import *
from gen_sketch_svg import get_sketch_svg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = OUT = os.path.dirname(HERE)          # pages are written to the repository root (the deployable site)
e = html.escape

class P: R = ""
def u(slug=""): return P.R + (slug + "/" if slug else "")
def img(path, alt="", eager=False, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{P.R}media/wp-content/uploads/{path}" data-live="{LIVE}{path}" alt="{e(alt)}"'
            f'{"" if eager else " loading=\"lazy\""} decoding="async">')
def roll(t): return f'<span class="roll"><span>{t}</span><span aria-hidden="true">{t}</span></span>'
def btn(t, href, kind="gold", extra=""): return f'<a class="btn btn-{kind}" href="{href}"{extra}>{roll(t)}</a>'
ARW = '<svg class="arw" viewBox="0 0 8 6" fill="currentColor"><path d="M7.06.73 4 3.78.94.73 0 1.67l4 4 4-4z"/></svg>'
ARR_L = '<svg viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M6 1 1 6l5 5M1 6h15"/></svg>'
ARR_R = '<svg viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="1.2"><path d="m10 1 5 5-5 5M15 6H0"/></svg>'
ORN = '<svg class="orn" viewBox="0 0 72 18" fill="none" stroke="currentColor" stroke-width="1"><path d="M1 9h22M49 9h22"/><path d="M36 2c-6 0-9 7-9 7s3 7 9 7 9-7 9-7-3-7-9-7z"/><circle cx="36" cy="9" r="2.2" fill="currentColor" stroke="none"/></svg>'

SKETCH = open(os.path.join(ROOT, "assets", "img", "palace-sketch.svg"), encoding="utf-8").read()

MAP = open(os.path.join(ROOT, "assets", "img", "map-jaipur.svg")).read().replace("<svg ", '<svg class="map-ill" ', 1)

ICONS = {
 "Instagram": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm5 3.5a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zm0 2a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM17.5 5.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg>',
 "Facebook": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8V6.5c0-.8.2-1.5 1.5-1.5H17V2h-2.6C11.6 2 11 3.9 11 5.9V8H9v3h2v11h3V11h2.4l.6-3z"/></svg>',
 "YouTube": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 8.2s-.2-1.6-.9-2.3c-.8-.9-1.8-.9-2.2-1C15.8 4.7 12 4.7 12 4.7s-3.8 0-6.9.2c-.4.1-1.4.1-2.2 1C2.2 6.6 2 8.2 2 8.2S1.8 10 1.8 12v1.7c0 1.8.2 3.6.2 3.6s.2 1.6.9 2.3c.8.9 1.9.9 2.4 1 1.7.2 6.7.2 6.7.2s3.8 0 6.9-.3c.4 0 1.4-.1 2.2-1 .7-.7.9-2.3.9-2.3s.2-1.8.2-3.6V12c0-1.9-.2-3.8-.2-3.8zM9.9 15.3V8.9l6 3.2z"/></svg>',
 "Pinterest": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12.2 2C6.7 2 4 5.9 4 9.2c0 2 .8 3.7 2.3 4.4.3.1.5 0 .6-.3l.2-.9c.1-.3 0-.4-.2-.7-.5-.6-.8-1.3-.8-2.4 0-3.1 2.3-5.8 6-5.8 3.3 0 5.1 2 5.1 4.7 0 3.5-1.6 6.5-3.9 6.5-1.3 0-2.2-1-1.9-2.3.4-1.5 1.1-3.2 1.1-4.3 0-1-.5-1.8-1.6-1.8-1.3 0-2.3 1.3-2.3 3.1 0 1.1.4 1.9.4 1.9L7.5 18c-.4 1.8-.1 4 0 4.2 0 .1.2.2.3.1.1-.1 1.4-1.8 1.9-3.4l.7-2.8c.4.7 1.4 1.3 2.6 1.3 3.4 0 5.7-3.1 5.7-7.3C18.7 5 16.1 2 12.2 2z"/></svg>',
 "X": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.3L5.3 21H2.2l7.2-8.3L2 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/></svg>',
}

# ---------------------------------------------------------------- extra content
WEATHER = ("Jaipur is at its best from October to March: warm, sunny days and cool evenings, with winter nights in December and January turning chilly. "
           "April to June is hot and dry, and the monsoon arrives from July to September, turning the Aravalli hills green.")
PACK = ("Light cottons and linens for the day; a shawl or light jacket for winter evenings and early-morning safaris. "
        "Swimwear for the pool, comfortable walking shoes for heritage walks, a hat and sunscreen for jeep and camel safaris, and something festive for folk evenings.")
NEED = (f"Check-in is at 2:00 PM and check-out at 11:00 AM. {FAQ[3][1]} {FAQ[4][1]} Wi-Fi is available across the resort, and vegetarian and Jain meals are prepared on request.")
DIRECTIONS = (f"{ADDRESS}. The palace sits in the Aravalli hills at Kukas, off the Jaipur–Delhi highway (NH-48), about 12 km north of Amber Fort and a short drive from Jaipur city and Jaipur International Airport. "
              f"<a href='https://www.google.com/maps/search/?api=1&query=The+Vijayran+Palace+Kukas+Jaipur'>Open in Google Maps</a>.")
INFO = [("Maps and directions", DIRECTIONS), ("Need to know", NEED), ("What to pack", PACK), ("Weather", '<span class="wx-inline" data-wx="inline" hidden></span>' + WEATHER)]

# ---------------------------------------------------------------- chrome
MENU_COLS = [
 ("Stay", [("Our Stays","accommodation")] + [(r["name"], r["slug"]) for r in ROOMS]),
 ("Experience", [("Weddings","best-destination-wedding-venues-in-jaipur"),("Activities","yoga-spa-pool-luxury-resort-jaipur-rajasthan"),("Dining","best-luxury-dining-resort-in-jaipur"),
                 ("Attractions","top-holiday-resort-in-jaipur-for-family"),("Day Outing","resort-near-jaipur-for-day-outing"),("Gallery","heritage-wedding-resort-jaipur-rajasthan")]),
]
MENU_SM = [("Our Story","about-us-luxury-resort-of-jaipur"),("Contact","get-in-touch-resort-in-kukas-jaipur"),("FAQ","faq"),("Careers","career")]

def nav(light):
    cols = "".join(f'<div class="m-col"><h4><span>{g}</span></h4>' + "".join(f'<a class="m-link" href="{u(s)}"><span>{n}</span></a>' for n, s in it) + "</div>" for g, it in MENU_COLS)
    fc = f'''<a class="m-card" href="{u('presidential-villas')}">
  <div class="im">{img('2021/04/Villa-Master-Room.jpg', 'Presidential Villas')}</div>
  <div class="m-card-body">
    <span class="m-tag">Royal Residence</span>
    <p><span>Presidential Villas</span></p>
    <small>5 villas · Private plunge pool &amp; garden</small>
  </div>
</a>
<a class="m-card" href="{u('best-destination-wedding-venues-in-jaipur')}">
  <div class="im">{img('2021/06/g10.jpg', 'Weddings at the Palace')}</div>
  <div class="m-card-body">
    <span class="m-tag">Destination Celebrations</span>
    <p><span>Weddings at the Palace</span></p>
    <small>Palatial lawns &amp; banquet for 100–1,500 guests</small>
  </div>
</a>'''
    sm = (f'<div class="m-col sm"><h4><span>The Palace</span></h4>'
          + "".join(f'<a class="m-link" href="{u(s)}"><span>{n}</span></a>' for n, s in MENU_SM)
          + f'''<div class="m-concierge">
  <span class="mc-tag">Palace Concierge</span>
  <p>24/7 Reservations &amp; Inquiries</p>
  <a class="mc-tel" href="tel:{TEL_ROOMS}">{PHONE_ROOMS}</a>
</div></div>''')
    m_bot = f'''<div class="menu-bot">
  <div class="mb-col mb-res">
    <span class="mb-lbl">Direct Reservations</span>
    <div class="mb-links">
      <a href="tel:{TEL_ROOMS}">{PHONE_ROOMS}</a>
      <span class="mb-sep">·</span>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
  </div>
  <div class="mb-col mb-loc">
    <span class="mb-lbl">Palace Location</span>
    <div class="mb-links">
      <span>NH-8, Kukas, Jaipur · Near Amber Fort</span>
    </div>
  </div>
  <div class="mb-col mb-soc">
    <span class="mb-lbl">Connect with the Palace</span>
    <div class="m-social">''' + "".join(f'<a href="{h}" target="_blank" rel="noopener"><span>{n}</span></a>' for n, h in SOCIAL) + '''</div>
  </div>
</div>'''
    books = [("Book a stay","Check rates & availability",BOOK,"2021/05/img01.jpg"),
             ("Weddings & events","Send an enquiry",u("best-destination-wedding-venues-in-jaipur")+"#enquire","2021/06/g5.jpg"),
             ("Day outing","Pool, high tea & dinner",u("resort-near-jaipur-for-day-outing"),"2021/04/LUCK7602.jpg"),
             ("Call reservations",PHONE_ROOMS,f"tel:{TEL_ROOMS}","2021/06/Main-Gate.jpg")]
    bk = "".join(f'<a class="book-item" href="{h}"><div class="im">{img(p,t)}</div><div class="tx"><b>{t}</b><small>{s}</small></div></a>' for t, s, h, p in books)
    return f"""<header class="nav{' is-light' if light else ''}">
 <div class="nav-l"><button class="nav-menu" aria-label="Menu" aria-expanded="false"><span class="burger"><i></i><i></i><i></i></span><span class="roll"><span>Menu</span><span>Close</span></span></button></div>
 <a class="logo" href="{u()}" aria-label="The Vijayran Palace by Royal Quest Resorts — home"><img class="lg-w" src="{P.R}assets/img/logo-white.svg" alt="The Vijayran Palace by Royal Quest Resorts" width="323" height="72"><img class="lg-g" src="{P.R}assets/img/logo-gold.svg" alt="" aria-hidden="true" width="323" height="72"></a>
 <div class="book"><button class="btn btn-gold" aria-haspopup="true">{roll('Book now')}{ARW}</button><div class="book-panel">{bk}</div></div>
</header>
<div class="menu" aria-label="Site menu"><div class="menu-in"><div class="menu-grid">{cols}{sm}<div class="m-feat">{fc}</div></div>{m_bot}</div></div>"""

def footer():
    links = [("Our Stays","accommodation"),("Our Story","about-us-luxury-resort-of-jaipur"),("Weddings","best-destination-wedding-venues-in-jaipur"),
             ("Activities","yoga-spa-pool-luxury-resort-jaipur-rajasthan"),("Dining","best-luxury-dining-resort-in-jaipur"),("Attractions","top-holiday-resort-in-jaipur-for-family"),
             ("Day Outing","resort-near-jaipur-for-day-outing"),("Gallery","heritage-wedding-resort-jaipur-rajasthan"),("FAQ","faq"),("Careers","career"),
             ("Contact","get-in-touch-resort-in-kukas-jaipur"),("Terms & Conditions","terms-and-conditions")]
    li = "".join(f'<li><a class="ul" href="{u(s)}">{n}</a></li>' for n, s in links)
    soc = "".join(f'<a href="{h}" aria-label="{n}">{ICONS[n]}</a>' for n, h in SOCIAL)
    return f"""<footer class="footer">
 <div class="f-top"><a class="f-logo" href="{u()}"><img class="f-crest" src="{P.R}assets/img/crest.png" alt="Royal Quest Resorts & Hotels crest" width="210" height="214"><img class="f-word" src="{P.R}assets/img/logo-gold.svg" alt="The Vijayran Palace by Royal Quest Resorts" width="323" height="72"></a>
  <div class="f-badges"><span class="f-badge"><span>4.5<small>Trip-<br>advisor</small></span></span><span class="p-s" style="color:var(--sand)">Rated 4.5 of 5 on Tripadvisor<br>from 284 guest reviews</span></div></div>
 <div class="f-grid">
  <div><p class="f-h">Contact Us</p>
   <p class="f-lbl">Reservations:</p><p class="f-txt"><a class="ul" href="mailto:{EMAIL}">{EMAIL}</a><br><a class="ul" href="tel:{TEL_ROOMS}">{PHONE_ROOMS}</a></p>
   <p class="f-lbl">Weddings &amp; events:</p><p class="f-txt"><a class="ul" href="mailto:{EMAIL_SALES}">{EMAIL_SALES}</a><br><a class="ul" href="tel:{TEL_EVENTS}">{PHONE_EVENTS}</a></p>
   <p class="f-lbl">Address:</p><p class="f-txt">{ADDRESS}</p>
   {btn('Contact us', u('get-in-touch-resort-in-kukas-jaipur'), 'line lt')}
   <p class="f-h" style="margin:3rem 0 0">Follow Us</p><div class="f-social" style="margin-top:1.5rem">{soc}</div></div>
  <div><p class="f-h">Explore</p><ul class="f-links" style="grid-template-columns:repeat(2,auto)">{li}</ul></div>
  <div class="news"><p class="f-h">Stay Connected with Vijayran</p>
   <form data-form data-endpoint=""><p class="p-l">Please share your contact details with us if you'd like to be a part of our community.</p>
    <input type="email" required placeholder="Email address" aria-label="Email address">
    <small>I would like to be kept updated on seasonal packages, celebrations and offers from The Vijayran Palace. I can opt out at any time.</small>
    <label class="chk"><input type="checkbox" required> I accept the <a href="{u('terms-and-conditions')}">Terms &amp; Conditions</a></label>
    {'<button class="btn btn-gold" type="submit">' + roll('Subscribe') + '</button>'}</form>
   <p class="form-ok" style="background:rgba(238,232,223,.1);color:#fff">Thank you, you're on the list.</p></div>
 </div>
 <div class="f-bot"><span>© <span data-year>2026</span> Royal Quest Resorts. All rights reserved.</span><span>The Vijayran Palace · Kukas, Jaipur</span></div>
</footer>
<div class="lightbox" aria-hidden="true"><button aria-label="Close">×</button><img alt=""></div>"""

def page(path, title, desc, body, light=False, schema=None):
    P.R = "../" * path.count("/")
    canon = SITE + (path[:-10] if path.endswith("index.html") else path)
    ld = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    V = P.R + "assets/vendor/"
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:site_name" content="The Vijayran Palace"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canon}">
<link rel="icon" href="{P.R}assets/img/crest.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Italianno&family=Jost:wght@300;400;500&family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Roboto+Flex:opsz,wght@8..144,300;8..144,400&display=swap">
{(f'<link rel="preconnect" href="https://use.typekit.net" crossorigin><link rel="stylesheet" href="https://use.typekit.net/{ADOBE_FONTS_KIT}.css">' if ADOBE_FONTS_KIT else "")}
<link rel="stylesheet" href="{P.R}assets/css/site.css">
{ld}
</head>
<body>
<svg width="0" height="0" style="position:absolute;left:-9999px;top:-9999px;overflow:hidden;" aria-hidden="true">
  <defs>
    <clipPath id="mehrabClip" clipPathUnits="objectBoundingBox">
      <path d="M 0 1 L 1 1 L 1 0.40 C 1 0.32, 0.93 0.26, 0.86 0.26 C 0.86 0.19, 0.77 0.13, 0.68 0.13 C 0.68 0.07, 0.58 0.02, 0.50 0.00 C 0.42 0.02, 0.32 0.07, 0.32 0.13 C 0.23 0.13, 0.14 0.19, 0.14 0.26 C 0.07 0.26, 0 0.32, 0 0.40 Z" />
    </clipPath>
  </defs>
</svg>
{nav(light)}
<main id="main">
{body}
</main>
{footer()}
<script src="{V}gsap.min.js"></script><script src="{V}ScrollTrigger.min.js"></script><script src="{V}SplitText.min.js"></script>
<script src="{V}Draggable.min.js"></script><script src="{V}InertiaPlugin.min.js"></script><script src="{V}lenis.min.js"></script>
<script src="{P.R}assets/js/site.js"></script>
</body>
</html>"""
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    open(full, "w", encoding="utf-8").write(doc)

# ---------------------------------------------------------------- components (mirroring Sujan sections)
def hero(media, title, label="", video=None):
    lab = f'<p class="lbl">{label}</p>' if label else ""
    if video:
        if video.startswith("assets/"):
            m = (f'<video autoplay muted loop playsinline preload="auto" poster="{P.R}{media}">'
                 f'<source src="{P.R}{video}" type="video/mp4"></video>')
        else:
            m = (f'<video autoplay muted loop playsinline preload="metadata" poster="{P.R}media/wp-content/uploads/{media}">'
                 f'<source src="{P.R}media/wp-content/uploads/{video}" type="video/mp4"><source src="{LIVE}{video}" type="video/mp4"></video>')
        snd = '<button class="sound" aria-label="Toggle sound" aria-pressed="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="m17 9 4 6M21 9l-4 6"/></svg></button>'
    else:
        m, snd = img(media, title, eager=True), ""
    wx = ('<aside class="wx-hero" data-wx="hero" aria-live="polite" hidden><p class="lbl">At the palace now</p>'
          '<div class="wx-row"><span class="wx-ico" data-wx="icon"></span><button class="wx-temp" data-wx="temp" aria-label="Switch °C/°F"></button></div>'
          '<p class="wx-desc"><span data-wx="desc"></span> · <span data-wx="hilo"></span></p><p class="wx-time"><span data-wx="time"></span> IST · Kukas, Jaipur</p></aside>') if video else ""
    return f'<section class="hero"><div class="hero-media">{m}</div><div class="hero-cap">{lab}<h1 class="t-hero" data-split="hero">{title}</h1></div>{wx}{snd}</section>'

def sketch_markup():
    return f'<div class="sk-wrap" aria-label="Architectural engraving of The Vijayran Palace">{get_sketch_svg(P.R)}</div>'

def intro(title_html, text, tpl=False, sketch=True, ornament=True):
    t = f'<h2 class="{"h-xl" if tpl else "t-xl"}" data-split>{title_html}</h2>'
    sk = sketch_markup() if sketch else "<span></span>"
    return (f'<div class="intro-wrap"><section class="intro{" c-tpl" if tpl else ""}">{ORN if ornament and tpl else ""}<div class="intro-title">{t}</div>'
            f'<div class="intro-row"><div class="p-l" data-split="text">{text}</div><span></span>{sk}</div></section></div>')

def cert(image, label, quote):
    return (f'<section class="cert"><div class="cert-img">{img(image, label)}</div><div class="cert-in">'
            f'<div class="cert-lbl"><i></i><span class="lbl">{label}</span></div><p class="cert-q" data-split>{quote}</p></div></section>')

def rail_items(items, link=True):
    out = ""
    for it in items:
        inner = f'<div class="im">{img(it["img"], it["title"])}</div><div class="ca-line"></div><h3>{it["title"]}</h3>' + (f'<p>{it["text"]}</p>' if it.get("text") else "")
        out += (f'<a class="ca-item" href="{it["href"]}" draggable="false">{inner}</a>' if link and it.get("href") else f'<div class="ca-item">{inner}</div>')
    return out

def rail_ui(dots=False):
    if dots: return '<div class="dots"></div>'
    return f'<div class="rail-ui"><div class="rail-bar"><i></i></div><div class="rail-btns"><button data-prev aria-label="Previous">{ARR_L}</button><button data-next aria-label="Next">{ARR_R}</button></div></div>'

def collection(title, text, cta, items, bg="", extra_attrs=""):
    return (f'<section class="coll" data-rail{bg}{extra_attrs}><div class="coll-head"><div class="tx"><h2 class="t-s" data-split>{title}</h2><p class="p" data-split="text">{text}</p></div>{cta}</div>'
            f'<div class="rail"><div class="rail-track">{rail_items(items)}</div></div>{rail_ui()}</section>')

def experiences(title, text, items):
    return (f'<section class="exp" data-rail><div class="exp-head"><h2 class="h-m" data-split>{title}</h2><p class="p-s" data-split="text">{text}</p></div>'
            f'<div class="rail"><div class="rail-track">{rail_items(items, link=False)}</div></div>{rail_ui()}</section>')

def gallery(paths, alts=None, title="Gallery"):
    alts = alts or ["The Vijayran Palace"] * len(paths)
    items = [{"img": p, "title": a} for p, a in zip(paths, alts)]
    tr = "".join(f'<div class="ca-item"><div class="im">{img(i["img"], i["title"])}</div></div>' for i in items)
    return f'<section class="gal" data-rail><h2 class="h-s" data-split>{title}</h2><div class="rail"><div class="rail-track">{tr}</div></div>{rail_ui(dots=True)}</section>'

def story(title_html, text, cta, images, head="t-l"):
    its = "".join(f'<div class="story-item"><div class="im">{img(p, "The Vijayran Palace")}</div></div>' for p in images)
    return (f'<section class="story"><div class="story-stck"><div class="in"><h2 class="{head}" data-split>{title_html}</h2><p class="p" data-split="text">{text}</p>{cta}</div></div>'
            f'<div class="story-imgs">{its}</div></section>')

def itinerary(title_html, text, cta):
    return (f'<section class="itin"><div><h2 class="t-m" data-split>{title_html}</h2><div class="ico">{ORN}</div><p class="p" data-split="text">{text}</p>{cta}</div><span></span>'
            f'<div class="map" data-fade>{MAP}</div></section>')

def feature(image, label, title, text, cta=None, rev=False, short=False):
    c = cta and btn(cta[0], cta[1], "line lt") or ""
    cls = "feat" + (" rev" if rev else "") + (" short" if short else "")
    return (f'<section class="{cls}"><div class="im">{img(image, title)}</div><div class="tx"><p class="lbl" data-fade>{label}</p>'
            f'<h2 class="h-m" data-split>{title}</h2><p class="p-l" data-split="text">{text}</p>{c}</div></section>')

def stack(title, text, items):
    out = f'<section class="stack"><div class="stack-head"><h2 class="h-m" data-split>{title}</h2><p class="p-l" data-split="text">{text}</p></div>'
    for i, it in enumerate(items):
        facts = "".join(f"<li>{f}</li>" for f in it.get("facts", []))
        acts = "".join(btn(t, h, k) for t, h, k in it.get("acts", []))
        out += (f'<div class="stack-item">{img(it["img"], it["name"])}<div class="stack-panel{" dark" if i % 2 else ""}"><p class="tag">{it.get("tag", it["name"])}</p>'
                f'<h3>{it["name"]}</h3><p class="p-s">{it["text"]}</p>' + (f"<ul>{facts}</ul>" if facts else "<div style='height:1.75rem'></div>") + f'<div class="acts">{acts}</div></div></div>')
    return out + "</section>"

def info(title, text, items, cta=None):
    acc = "".join(f'<div class="acc-i"><button class="acc-q" aria-expanded="false">{q}<span class="pl"></span></button><div class="acc-a"><div class="in"><p>{a}</p></div></div></div>' for q, a in items)
    c = cta or ""
    return f'<section class="info"><div><h2 class="h-m" data-split>{title}</h2><p class="p-l" data-split="text">{text}</p></div><div style="align-self:end;justify-self:end">{c}</div><div class="acc">{acc}</div></section>'

def quote(i=0):
    t, n = REVIEWS[i]
    return (f'<section class="quote"><p class="quote-t" data-split>“{t}”</p><p class="sig" data-fade>{n.split()[0]}</p>'
            f'<cite data-fade>{n}<small>Guest of The Vijayran Palace</small></cite></section>')

def ph(label, title_html):
    return f'<section class="ph"><p class="lbl" data-fade>{label}</p><h1 class="t-xl" data-split>{title_html}</h1></section>'

def room_items(rooms):
    return [{"img": r["card"], "title": r["name"], "text": f'{r["short"]} · {r["count"]}', "href": u(r["slug"])} for r in rooms]

def wedding_home():
    venues = [
        {
            "id": "vmb",
            "name": "Vijayran Mahal Bagh",
            "tag": "1,000–1,500 Guests",
            "setting": "Grand Front Lawn · Open Sky",
            "img": "2021/06/g10.jpg",
            "desc": "The grand palace front lawn framed by the ancient Aravalli peaks. Designed for majestic royal baraat processions, colossal mandaps, and imperial banquets under the starlit sky.",
            "highlights": ["Capacity for up to 1,500 royal guests", "Regal elephant & horse procession entryway", "Starlit amphitheatre & banquet layout"]
        },
        {
            "id": "rm",
            "name": "Rang Mahal",
            "tag": "400–500 Guests",
            "setting": "Heritage Amphitheatre & Lawns",
            "img": "2021/06/g5.jpg",
            "desc": "Featuring an illuminated heritage jharokha stage and manicured royal gardens under the starlit sky. Ideal for sangeet spectacles, musical nights, and grand varmala ceremonies.",
            "highlights": ["Inbuilt architectural stone stage", "Acoustically tuned garden setting", "Dedicated cocktail pavilions & gazebos"]
        },
        {
            "id": "rajm",
            "name": "Raj Mahal Grand Banquet",
            "tag": "250–300 Guests",
            "setting": "Palatial Tapestry Hall",
            "img": "2021/06/g2.jpg",
            "desc": "An opulent indoor banquet hall embellished with authentic Rajasthani tapestries, crystal chandeliers, hand-carved stone arches, and climate-controlled comfort.",
            "highlights": ["Artisanal gold-leafing & authentic mirrors", "Complete climate-controlled luxury", "Seamless foyer for royal receptions"]
        },
        {
            "id": "cbp",
            "name": "Char Bagh & Poolside",
            "tag": "100–250 Guests",
            "setting": "Mughal Fountain Courts & Ambar Taal",
            "img": "2021/06/g6.jpg",
            "desc": "Char Bagh's geometric fountain courtyards and the turquoise Ambar Taal pool deck. The ultimate intimate backdrop for vibrant Mehendi festivities and sun-drenched Haldi mornings.",
            "highlights": ["Four-quadrant Mughal fountain symmetry", "Turquoise reflection poolside setting", "Authentic Rajasthani shamiana setups"]
        }
    ]

    cards_html = ""
    for idx, v in enumerate(venues):
        active_cls = " is-active" if idx == 0 else ""
        cards_html += (f'<div class="hw-vcard{active_cls}" data-venue-id="{v["id"]}" data-img="{P.R}media/wp-content/uploads/{v["img"]}" '
                       f'data-title="{v["name"]}" data-tag="{v["tag"]}" data-setting="{v["setting"]}" data-desc="{v["desc"]}" '
                       f'data-hl1="{v["highlights"][0]}" data-hl2="{v["highlights"][1]}" data-hl3="{v["highlights"][2]}">'
                       f'<div class="hw-vcard-thumb"><img src="{P.R}media/wp-content/uploads/{v["img"]}" alt="{v["name"]}" loading="lazy"></div>'
                       f'<div class="hw-vcard-text"><h4>{v["name"]}</h4><p>{v["tag"]} · {v["setting"]}</p></div>'
                       f'<div class="hw-vcard-arr"><svg viewBox="0 0 8 12" width="8" height="12" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1.5 1.5l4.5 4.5-4.5 4.5"/></svg></div></div>')

    v0 = venues[0]
    return f"""<section class="home-wedding" id="weddings">
  <div class="hw-bg-crest"></div>
  <div class="hw-inner">
    <div class="hw-header" data-fade>
      <div class="hw-tag"><span class="hw-gem">✦</span> A Royal Destination Celebration <span class="hw-gem">✦</span></div>
      <h2 class="hw-title" data-split>Weddings at the Palace</h2>
      <p class="hw-lead" data-split="text">Walk into marital bliss surrounded by centuries of Rajputana grandeur, whispering Aravalli hills, and palatial splendour. Where fairytale dreams transform into royal heritage memories.</p>
    </div>

    <div class="hw-showcase" data-fade>
      <!-- Featured Interactive Venue Card -->
      <div class="hw-card-main" data-tilt>
        <div class="hw-arch-frame">
          <div class="hw-img-wrap">
            <img id="hwMainImg" class="hw-main-img" src="{P.R}media/wp-content/uploads/{v0['img']}" alt="{v0['name']}">
          </div>
          <div class="hw-img-overlay"></div>
          <div class="hw-arch-crest">
            <img src="{P.R}assets/img/crest.png" alt="Crest">
          </div>
        </div>
        <div class="hw-card-info">
          <div class="hw-badge-row">
            <span id="hwBadgeTag" class="hw-badge gold">{v0['tag']}</span>
            <span id="hwBadgeSetting" class="hw-badge outline">{v0['setting']}</span>
          </div>
          <h3 id="hwCardTitle" class="hw-card-title">{v0['name']}</h3>
          <p id="hwCardDesc" class="hw-card-desc">{v0['desc']}</p>
          <div class="hw-card-highlights">
            <div class="hw-hl-item"><span class="hw-hl-ico">✦</span> <span id="hwHl1">{v0['highlights'][0]}</span></div>
            <div class="hw-hl-item"><span class="hw-hl-ico">✦</span> <span id="hwHl2">{v0['highlights'][1]}</span></div>
            <div class="hw-hl-item"><span class="hw-hl-ico">✦</span> <span id="hwHl3">{v0['highlights'][2]}</span></div>
          </div>
          <div class="hw-actions">
            <a class="btn btn-gold btn-shimmer" href="{u('best-destination-wedding-venues-in-jaipur')}#enquire">Plan Your Royal Wedding</a>
            <a class="btn btn-line" href="{u('best-destination-wedding-venues-in-jaipur')}">Explore All 7 Venues</a>
          </div>
        </div>
      </div>

      <!-- Interactive Venue Switcher Column -->
      <div class="hw-venues-grid" id="hwVenuesGrid">
        {cards_html}
      </div>
    </div>

    <!-- Royal Wedding Stats Strip -->
    <div class="hw-stats-strip" data-fade>
      <div class="hw-stat">
        <span class="hw-stat-n">1,500</span>
        <span class="hw-stat-l">Max Guest Capacity</span>
      </div>
      <div class="hw-stat">
        <span class="hw-stat-n">7</span>
        <span class="hw-stat-l">Distinct Royal Venues</span>
      </div>
      <div class="hw-stat">
        <span class="hw-stat-n">35</span>
        <span class="hw-stat-l">Luxury Haveli Suites &amp; Villas</span>
      </div>
      <div class="hw-stat">
        <span class="hw-stat-n">100%</span>
        <span class="hw-stat-l">Bespoke Royal Hospitality</span>
      </div>
    </div>
  </div>
</section>"""

HOTEL_LD = {"@context":"https://schema.org","@type":"Resort","name":"The Vijayran Palace by Royal Quest Resorts","url":SITE,"telephone":PHONE_ROOMS,"email":EMAIL,
 "address":{"@type":"PostalAddress","streetAddress":"NH-8, Kukas, Village Kacherawala","addressLocality":"Jaipur","addressRegion":"Rajasthan","postalCode":"302028","addressCountry":"IN"},
 "checkinTime":"14:00","checkoutTime":"11:00","aggregateRating":{"@type":"AggregateRating","ratingValue":"4.5","reviewCount":"284","bestRating":"5"},"sameAs":[h for _, h in SOCIAL]}

STORY_IMGS = ["2021/06/Main-Gate.jpg","2021/06/g3.jpg","2021/06/g9.jpg","2021/06/g6.jpg","2021/05/wedding01.jpg"]

# ---------------------------------------------------------------- pages
def build():
    pass  # assets/ and media/ live at the repo root and are served as-is

    # HOME — same section order as thesujanlife.com
    P.R = ""
    exp_items = [{"img": p, "title": t, "text": d} for t, p, d in EXPERIENCES]
    body = (hero("assets/video/hero-poster.jpg", "Where dreams come true and once-in-a-lifetime memories are born.", video="assets/video/hero.mp4")
      + intro('A palace for the <span class="soft">romantic,</span> the <span class="soft">celebrant,</span> and those in search of <span class="soft">stillness.</span>',
              "To stay at The Vijayran Palace is to live like royalty in the lap of the ancient Aravalli hills: regal architecture, refreshing views and lush gardens, with the warmth of true Rajasthani hospitality.")
      + cert("2021/06/g6.jpg", "Tripadvisor · 4.5 of 5", f"“{REVIEWS[1][0]}”")
      + collection("Our Stays", "Thirty-five villas, suites and rooms set around courtyards, terraces and gardens. Each offers a different way of living like royalty, from a private-pool villa to a suite framed by a hand-carved jharoka.",
                   btn("Discover our stays", u("accommodation")), room_items(ROOMS))
      + story('A heritage palace <span class="soft">woven into</span> the Aravalli hills',
              "Royal Quest Resorts created The Vijayran Palace around a simple idea: luxury, world-class service and an atmosphere of solitude. It is where old-world vibes and a glorious past meet the new age, an amalgamation of culture, tradition and contemporary comfort.",
              btn("Discover our story", u("about-us-luxury-resort-of-jaipur"), "dark"), STORY_IMGS)
      + collection("Activities & Experiences", "Choose your pace: guided morning yoga, horseback rides into the hills, folk music under the stars, or peaceful moments in our gardens and courtyards.",
                   btn("Explore all activities", u("yoga-spa-pool-luxury-resort-jaipur-rajasthan")),
                   [{"img": p, "title": t, "text": d, "slug": "yoga-spa-pool-luxury-resort-jaipur-rajasthan"} for t, p, d in EXPERIENCES],
                   extra_attrs=' data-auto-scroll="true"')
      + wedding_home()
      + itinerary('Discover the <span class="soft">royal heritage</span> of Jaipur from our doorstep.',
                  "Amber Fort is about 12 km away and the walled Pink City around 19 km. Hawa Mahal, City Palace, Jal Mahal and the cenotaphs of Gaitore are all within easy reach, with fairytale palaces, colourful temples and splendid havelis to explore before returning to the calm of the palace.",
                  btn("Explore", u("top-holiday-resort-in-jaipur-for-family"), "line")))
    page("index.html", "The Vijayran Palace | 5 Star Luxury Heritage Resort in Jaipur",
         "The Vijayran Palace by Royal Quest Resorts: a royal heritage resort in Jaipur, Rajasthan, with private pool villas, haveli suites and destination weddings.", body, schema=HOTEL_LD)

    # OUR STAYS — stacking full-screen cards (Sujan "Tents & tented suites")
    P.R = "../"
    st_items = [{"img": r["hero"], "name": r["name"], "tag": r["count"], "text": r["body"][0], "facts": r["facts"][:6],
                 "acts": [("Discover", u(r["slug"]), "line"), ("Book", BOOK, "gold")]} for r in ROOMS]
    body = (hero("2021/05/img01.jpg", "Our Stays", "Villas, haveli suites & rooms")
      + intro("Thirty-five ways to live like royalty, each with its own courtyard, terrace, jharoka or private pool.",
              "From the Presidential Villas with their private pools to suites framed by carved jharokas, every room pairs tasteful interiors and fine tapestry with modern comfort and prompt, warm service.", tpl=True)
      + stack("Villas, suites & rooms", "Six categories across the palace, each designed around the needs of our guests, for every kind of traveller from those seeking the ultimate indulgence to those on a lighter budget.", st_items)
      + info("Palace Information", "Everything you need to plan your stay, from directions and check-in times to what to pack and the best time to visit.", INFO, btn("Read all FAQs", u("faq"), "line"))
      + quote(0) + gallery(GALLERY[:8], GALLERY_ALT[:8]))
    page("accommodation/index.html", "Rooms, Suites & Private Pool Villas | The Vijayran Palace Jaipur",
         "All stays at The Vijayran Palace: Presidential Villas with private pools, Terrace, Courtyard, Balcony and Jharoka Haveli Suites, and Haveli Rooms.", body)

    # ROOM PAGES — Sujan camp template
    for r in ROOMS:
        P.R = "../"
        others = [x for x in ROOMS if x is not r]
        body = (hero(r["hero"], r["name"], r["count"])
          + intro(r["lead"], "".join(f"<p>{p}</p>" for p in r["body"]), tpl=True)
          + feature(r["panel"], r["short"], r["name"], r["body"][1], ("Check availability", BOOK))
          + stack("In the suite" if "Suite" in r["name"] else "In the room" if "Room" in r["name"] else "In the villa",
                  f'{r["count"]}. Every stay includes round-the-clock service and access to the palace pool, gardens, dining and activities.',
                  [{"img": r["gallery"][0], "name": r["name"], "tag": r["count"], "text": r["body"][0], "facts": r["facts"],
                    "acts": [("Book now", BOOK, "gold"), ("Call " + PHONE_ROOMS, f"tel:{TEL_ROOMS}", "line")]}])
          + experiences("Experiences", "Every stay at The Vijayran Palace is an invitation to explore Rajasthan's culture, its hills and its wildlife, or simply to slow down.",
                        [{"img": p, "title": t, "text": d} for t, p, d in EXPERIENCES])
          + feature("2021/05/rajfolk.jpg", "Every evening", "Rajasthani folk music under the stars",
                    "The land of the Ravanahatha, Kalbeliya and Ghoomar. The palace comes alive with an evening of dance, music and festivity, filled with traditional Rajasthani folk songs.", rev=True, short=True)
          + info("Palace Information", "Everything you need to prepare for your stay, from directions to what to pack and the best time to visit.", INFO, btn("Read all FAQs", u("faq"), "line"))
          + quote(0)
          + gallery(r["gallery"] + [r["card"]], [r["name"]] * (len(r["gallery"]) + 1))
          + collection("Our Stays", "Discover the other villas, suites and rooms of The Vijayran Palace.", btn("All stays", u("accommodation")), room_items(others)))
        page(f'{r["slug"]}/index.html', r["seo"], r["desc"], body,
             schema={"@context":"https://schema.org","@type":"HotelRoom","name":r["name"],"description":r["desc"],"containedInPlace":{"@type":"Resort","name":"The Vijayran Palace"}})

    # ABOUT
    P.R = "../"
    body = (hero("2021/06/Main-Gate.jpg", "Our Story", "The Vijayran Palace by Royal Quest Resorts")
      + intro('An escape from the <span class="soft">busy world,</span> in the lap of <span class="soft">nature.</span>',
              "Have you ever wondered what an escape from your demanding life would feel like, in the lap of nature, with luxurious service and a peaceful environment? At Vijayran, the dream of a relaxed holiday where you are king comes true.")
      + cert("2021/06/g8.jpg", "Royal Quest Resorts", "“Rich heritage, natural beauty and a refreshing ambience, combined with remarkable service.”")
      + story('Old-world vibes <span class="soft">meet</span> the new age',
              "Royal Quest Resorts developed The Vijayran Palace around a unique idea: an experience laden with luxury, world-class service and an atmosphere of solitude. Away from the worldly chaos, lose yourself in a fortress of solitude and magnificence. We await all our guests with open arms and excellent hospitality, because you deserve it.",
              btn("Explore our stays", u("accommodation"), "dark"), ["2021/06/g2.jpg","2021/06/g4.jpg","2021/06/g11.jpg","2021/06/g5.jpg","2021/05/view.jpg"])
      + feature("2021/05/wedding01.jpg", "For every traveller", "Suites for every kind of stay",
                "Vijayran strikes a delicate balance between culture, tradition and modern luxury. Our luxury suites, honeymoon suites, junior suites and double rooms suit every budget, from those seeking the ultimate indulgence to those travelling light.",
                ("Plan a wedding", u("best-destination-wedding-venues-in-jaipur")))
      + quote(2))
    page("about-us-luxury-resort-of-jaipur/index.html", "About The Vijayran Palace | Luxury Heritage Resort in Jaipur",
         "One of Jaipur's most luxurious heritage resorts, with palace architecture, luxury accommodation, huge lawns, banquet venues and restaurants.", body)

    # WEDDINGS
    venue_items = [{"img": "2021/06/g10.jpg", "name": "Vijayran Mahal Bagh", "tag": "1,000–1,500 guests", "text": "The grand front lawn, for the largest celebrations under the open sky."},
                   {"img": "2021/06/g4.jpg", "name": "Rang Mahal", "tag": "400–500 guests", "text": "An inbuilt stage with a heritage backdrop and gardens."},
                   {"img": "2021/06/g2.jpg", "name": "Raj Mahal", "tag": "250–300 guests", "text": "Our grand banquet, styled with royal tapestry and artistic décor."},
                   {"img": "2021/06/g6.jpg", "name": "Courtyards & Pool", "tag": "100–250 guests", "text": "Char Bagh's fountain square, the Trantal pool area, the Royal Courtyard and Haveli Chowk: intimate settings for Mehendi, Haldi and musical nights."}]
    for v in venue_items: v["acts"] = [("Enquire", "#enquire", "gold")]
    wex = [("Pre-wedding shoots","elementor/thumbs/pre-wedding11-q6cb7ilbpp8p9piwagxl8l7o5ryvifoxuqst6hlcm8.jpg","Architecture, lush greenery, jharokas, the rugged hills and poolside sunsets: every frame is a royal portrait."),
           ("Mehendi & Haldi","elementor/thumbs/mehendi-1-q6au76p8igvq9thbll0z25e37xvw8fr4tdwpmv3d40.jpg","A Haldi ceremony in our lush gardens, or a Mehendi in the royal aangan-style courtyard."),
           ("Musical nights","elementor/thumbs/music-night-3-5-pdw9x97p4kl3g5bpogvhsc1t4iodb15iau6llwihb4.jpg","A scintillating musical night with a band or DJ right beside the pool."),
           ("Exclusive cultural show","elementor/thumbs/cal-show-1-q6atsqwhj345xggcwuca9ak6pv1wztfkhx578ui2ow.jpg","On-demand folk songs, folk dances and the much-loved Ghoomar, exclusively for your guests."),
           ("Wedding feasts","elementor/thumbs/dine2-2-pduqgkhrhz9t3tmgxe1d86wdys3ahag145ne1x0qow.jpg","Our chefs craft menus with you, from Awadhi and Hyderabadi delicacies to contemporary cuisine.")]
    vt = "".join(f'<tr><td>{n}</td><td class="n">{c} guests</td><td>{d}</td></tr>' for n, c, d in VENUES)
    form = f"""<section class="split" id="enquire"><div><h2 class="h-m" data-split>Plan your celebration</h2><p class="p-l" data-split="text">Tell us about your event and our weddings team will be in touch.</p>
<p class="p-l" style="margin-top:2rem;color:var(--brown)">Weddings &amp; events<br><a class="ul" href="tel:{TEL_EVENTS}">{PHONE_EVENTS}</a><br><a class="ul" href="mailto:{EMAIL_SALES}">{EMAIL_SALES}</a></p></div>
<div><form class="form" data-form data-endpoint="">
<div class="full checks" role="group" aria-label="Event type"><label><input type="checkbox" name="event[]" value="Wedding"> Wedding</label><label><input type="checkbox" name="event[]" value="Pre-wedding"> Pre-wedding shoot</label><label><input type="checkbox" name="event[]" value="Corporate"> Corporate event</label><label><input type="checkbox" name="event[]" value="Social"> Social gathering</label></div>
<label>Event date*<input type="date" name="event_date" required></label><label>Number of guests*<input type="number" name="guests" min="1" required></label>
<label>Your name*<input name="name" required autocomplete="name"></label><label>Email*<input type="email" name="email" required autocomplete="email"></label>
<label>Phone*<input type="tel" name="phone" required autocomplete="tel"></label><label>Rooms required<input type="number" name="rooms" min="0"></label>
<label class="full">Message<textarea name="message"></textarea></label><div class="full"><button class="btn btn-dark" type="submit">{roll('Send enquiry')}</button></div></form>
<p class="form-ok">Thank you. Our weddings team will contact you shortly.</p></div></section>"""
    body = (hero("2021/06/g5.jpg", "Weddings like the kings and queens of yesteryear", "Destination weddings")
      + intro('More amazing than its <span class="soft">photographs</span> can describe.',
              "Medieval interiors for a palatial royal wedding, and rustic gardens for outdoor settings. Whether it is a modern wedding, a traditional Hindu wedding, a Christian ceremony or a nikah, you can trust The Vijayran Palace to weave its magic.")
      + feature("2021/06/g10.jpg", "Themes & décor", "Awe-inspiring themes, curated by our creative team",
                "Royal tapestry, artistic décor and an exotic ambience. Rustic, authentic feasts, exotic backdrops for pre- and post-wedding shoots, themed décor and a lovely musical night: you ask, and The Vijayran Palace provides.", ("Send an enquiry", "#enquire"))
      + stack("Venues", "Seven venues across the palace, from intimate courtyards for 100 guests to the grand Vijayran Mahal Bagh for up to 1,500.", venue_items)
      + experiences("Celebrations", "From the first Haldi to the last dance, every ritual has its setting at The Vijayran Palace.", [{"img": p, "title": t, "text": d} for t, p, d in wex])
      + f'<section class="split"><div><h2 class="h-m" data-split>Venues &amp; capacity</h2></div><table class="venues"><thead><tr><th>Venue</th><th>Capacity</th><th>Setting</th></tr></thead><tbody>{vt}</tbody></table></section>'
      + quote(2) + form + gallery(GALLERY[1:], GALLERY_ALT[1:]))
    page("best-destination-wedding-venues-in-jaipur/index.html", "Destination Wedding Venues in Jaipur | Palace Weddings at The Vijayran Palace",
         "A palace destination wedding venue in Jaipur for 100 to 1,500 guests, with themed décor, pre-wedding shoots, Mehendi, Haldi, musical nights and cultural shows.", body)

    # ACTIVITIES
    body = (hero("2021/06/ambertallpool-img.jpg", "Activities", "Culture, adventure & stillness")
      + intro('The <span class="soft">“actual India”,</span> at your doorstep.',
              "A village safari, a majestic elephant ride, a ride on the finest horses, an open jeep safari, or simply gazing at the magnificent night sky. Set in a culturally vibrant region, the palace introduces its guests to an India rich in customs, traditions and beliefs.")
      + experiences("Experiences", "Choose your pace: active mornings, cultural evenings and quiet moments in between.", [{"img": p, "title": t, "text": d} for t, p, d in EXPERIENCES])
      + feature("2021/05/rajfolk.jpg", "Every evening", "Rajasthani folk music under the stars",
                "The land of the Ravanahatha, Kalbeliya and Ghoomar. The Vijayran Palace brings you an evening of dance, music and festivity filled with traditional Rajasthani folk songs and dances.")
      + story('Slow mornings, <span class="soft">wild</span> afternoons',
              "Begin with guided yoga to birdsong, spend the afternoon on horseback or on a jeep safari in the Aravallis, and end the day by the Ambar Taal pool as the sun sets over the hills.",
              btn("Explore our stays", u("accommodation"), "dark"), ["2021/05/In-Yoga-1.jpg","2021/06/horse-img.jpg","2021/05/camel-ride.jpg","2021/05/jeep-safari.jpg","2021/05/bird.jpg"])
      + feature("2021/05/Lunch-with-elephant.jpg", "Near Amer", "Elephant ride with lunch or dinner",
                "A short drive takes you through the scenic beauty of Amer. Feed the elephants, ride through the hills, spot birds and finish with local delicacies.", rev=True, short=True)
      + info("Good to know", "Plan your activities with our front office team on arrival.", [("Safety", FAQ[7][1]), ("What to pack", PACK), ("Weather", '<span class="wx-inline" data-wx="inline" hidden></span>' + WEATHER)])
      + quote(1))
    page("yoga-spa-pool-luxury-resort-jaipur-rajasthan/index.html", "Activities at The Vijayran Palace | Yoga, Pool, Safaris & Folk Music, Jaipur",
         "Yoga, the Ambar Taal pool, elephant, horse and camel rides, jeep safaris, village walks, bird watching and Rajasthani folk evenings at The Vijayran Palace.", body)

    # DINING
    body = (hero("2021/05/dining-01.jpg", "Dining", "A paradise for every gourmand")
      + intro('From <span class="soft">Lucknowi kebabs</span> to <span class="soft">Italian ravioli.</span>',
              "Our Executive Chef and his brigade combine authentic cuisines from around the world with fresh spices, herbs and vegetables from our own organic kitchen gardens, from French risotto and Scottish shortbread to a Hyderabadi biryani or a Kashmiri dum aloo.")
      + feature("2021/05/dining-02.jpg", "Dinner under the sky", "A magical evening under the stars",
                "A lavish spread of delicacies and the scent of evening primroses. If this isn't heaven, we don't know what is.", ("Plan an evening", u("get-in-touch-resort-in-kukas-jaipur")))
      + experiences("Ways to dine", "In our restaurant, by the pool, under the sky or in the comfort of your room.", [{"img": p, "title": t, "text": d} for t, p, d in DINING])
      + cert("2021/05/dining-04.jpg", "A curated romantic dinner", "“Tables strewn with roses, aromatic candles and candlelight with a Mughal-e-Azam feel.”")
      + quote(0))
    page("best-luxury-dining-resort-in-jaipur/index.html", "Luxury Dining in Jaipur | Poolside & Romantic Dinners | The Vijayran Palace",
         "Fine dining, dinner under the sky, romantic curated dinners and poolside feasts at The Vijayran Palace, a luxury resort in Jaipur.", body)

    # ATTRACTIONS
    body = (hero("2021/05/view.jpg", "Attractions", "The land of the Maharajas")
      + intro('A destination in itself, with <span class="soft">Jaipur</span> on the doorstep.',
              "Time stands still here. Take in the view of the Aravallis, India's oldest mountain range, then set out for fairytale palaces, colourful temples, historic monuments and splendid havelis.")
      + itinerary('Explore the <span class="soft">Pink City</span> and its forts.', "The palace is about 12 km from Amber Fort and around 19 km from Hawa Mahal in the walled city. Our team will happily arrange cars and guides.", btn("Contact us", u("get-in-touch-resort-in-kukas-jaipur"), "line"))
      + experiences("Nearby", "Five landmarks within easy reach of The Vijayran Palace.", [{"img": p, "title": t, "text": d} for t, p, d in ATTRACTIONS])
      + cert("2021/05/AmberFort.jpg", "Amber Fort", "“The fort still stands as a perfect picture of ancient Indian architecture.”")
      + info("Getting here", "Directions, timings and travel tips for exploring Jaipur from the palace.", INFO))
    page("top-holiday-resort-in-jaipur-for-family/index.html", "Attractions near The Vijayran Palace | Holiday Resort in Jaipur for Families",
         "Amber Fort, Hawa Mahal, City Palace, Birla Mandir and Gaitore: discover Jaipur's attractions from The Vijayran Palace.", body)

    # DAY OUTING
    pk = [("Summer Splash","Day outing","Swimming pool access, high tea and a set-menu dinner, with horse riding and light music at the pool.","₹2,500 + taxes per person","2:00 PM – 9:00 PM. Add a room for ₹5,000 + taxes."),
          ("Family Fiesta","Stay package","Breakfast and one additional meal daily at Swarn Mahal, a supervised kids' hour with goodies, and an elephant safari in the Aravalli hills with transfers.","Price on request","Call or email to book."),
          ("Horse Riding in Jaipur","Stay package","Breakfast and one additional meal daily at Swarn Mahal, daily supervised horse riding and a supervised kids' hour with goodies.","Price on request","Call or email to book."),
          ("Elephant Safari in Jaipur","Stay package","Breakfast and one additional meal daily at Swarn Mahal, round-trip Jaipur airport transfers and an elephant safari near the Aravalli hills.","Price on request","Call or email to book.")]
    pks = "".join(f'<article data-fade><p class="lbl">{k}</p><h3>{t}</h3><p class="p">{d}</p><p class="price">{pr}</p><p class="p-s">{n}</p></article>' for t, k, d, pr, n in pk)
    body = (hero("2021/04/LUCK7602.jpg", "Day Outing", "Just outside Jaipur")
      + intro('Spend a day <span class="soft">like royalty.</span>', "A pool, the hills, high tea and dinner under the sky, all a short drive from the city. Perfect for families, couples and friends.")
      + f'<section class="pk">{pks}</section><div style="display:flex;gap:1rem;justify-content:center;padding:0 var(--g) 6rem">{btn("Call " + PHONE_ROOMS, "tel:" + TEL_ROOMS, "dark")}{btn("Email us", "mailto:" + EMAIL, "line")}</div>'
      + feature("2021/06/riding.jpg", "Add-ons", "Horse riding, games and the Ambar Taal pool", "Round off your day with a horse ride, games on the lawns or a swim, then dinner with a view of the Aravallis.", rev=True)
      + info("Good to know", "Everything you need before you visit.", INFO))
    page("resort-near-jaipur-for-day-outing/index.html", "Day Outing Resort near Jaipur | Packages | The Vijayran Palace",
         "Day outing packages near Jaipur at The Vijayran Palace: pool access, high tea and dinner, plus family, horse riding and elephant safari packages.", body)

    # GALLERY
    figs = "".join(f'<figure data-reveal>{img(p, a)}</figure>' for p, a in zip(GALLERY, GALLERY_ALT))
    body = hero("2021/06/g7-scaled.jpg", "Gallery", "The palace in pictures") + f'<section class="masonry">{figs}</section>'
    page("heritage-wedding-resort-jaipur-rajasthan/index.html", "Gallery | The Vijayran Palace, Heritage & Wedding Resort in Jaipur",
         "Photos of The Vijayran Palace, a luxury heritage and wedding resort in Jaipur, Rajasthan.", body)

    # CONTACT
    body = (ph("Contact", 'We await you with <span class="soft">open arms.</span>')
      + f"""<section class="contact-cols">
 <div data-fade><h3>Reservations</h3><p class="p-l"><a class="ul" href="tel:{TEL_ROOMS}">{PHONE_ROOMS}</a><br><a class="ul" href="mailto:{EMAIL}">{EMAIL}</a></p>{btn('Book a stay', BOOK)}</div>
 <div data-fade><h3>Weddings &amp; events</h3><p class="p-l"><a class="ul" href="tel:{TEL_EVENTS}">{PHONE_EVENTS}</a><br><a class="ul" href="mailto:{EMAIL_SALES}">{EMAIL_SALES}</a></p>{btn('Send an enquiry', u('best-destination-wedding-venues-in-jaipur') + '#enquire', 'line')}</div>
 <div data-fade><h3>The Palace</h3><p class="p-l">The Vijayran Palace by Royal Quest Resorts<br>{ADDRESS}</p></div></section>
<iframe class="map-frame" title="Map to The Vijayran Palace" loading="lazy" src="https://www.google.com/maps?q=The+Vijayran+Palace,+Kukas,+Jaipur&output=embed"></iframe>
<section class="split"><div><h2 class="h-m" data-split>Write to us</h2><p class="p-l" data-split="text">Questions, special requests or feedback: leave your details and we'll respond shortly.</p></div>
<div><form class="form" data-form data-endpoint=""><label>Your name*<input name="name" required autocomplete="name"></label><label>Email*<input type="email" name="email" required autocomplete="email"></label>
<label class="full">Phone<input type="tel" name="phone" autocomplete="tel"></label><label class="full">Message<textarea name="message"></textarea></label>
<div class="full"><button class="btn btn-dark" type="submit">{roll('Send message')}</button></div></form><p class="form-ok">Thank you. We'll be in touch soon.</p></div></section>""")
    page("get-in-touch-resort-in-kukas-jaipur/index.html", "Contact The Vijayran Palace | Resort in Kukas, Jaipur",
         f"Contact The Vijayran Palace for reservations on {PHONE_ROOMS} or {EMAIL}, and for weddings and events on {PHONE_EVENTS}.", body, light=True)

    # FAQ
    body = ph("FAQ", 'Frequently asked <span class="soft">questions</span>') + info("Before you arrive", "Enjoy a holiday in a royal setting, away from the noise and crowds of the city. Here is everything you might want to know.", FAQ, btn("Ask us anything", u("get-in-touch-resort-in-kukas-jaipur"), "line"))
    page("faq/index.html", "FAQ | The Vijayran Palace, Jaipur", "Answers to frequently asked questions about staying at The Vijayran Palace.", body, light=True,
         schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQ]})

    # CAREERS
    body = (hero("2021/05/wedding01.jpg", "Careers", "Grow with The Vijayran Palace")
      + f"""<section class="split"><div><h2 class="h-m" data-split>Work with us</h2><p class="p-l" data-split="text">We believe every guest deserves our very best, and so does every member of our team. If you share our passion for heritage hospitality, we would love to hear from you.</p></div>
<div><form class="form" data-form data-endpoint=""><label>Your name*<input name="name" required autocomplete="name"></label><label>Email*<input type="email" name="email" required autocomplete="email"></label>
<label>Phone<input type="tel" name="phone" autocomplete="tel"></label><label>Your CV<input type="file" name="cv" accept=".pdf,.doc,.docx"></label>
<label class="full">Message*<textarea name="message" required></textarea></label><div class="full"><button class="btn btn-dark" type="submit">{roll('Apply')}</button></div></form>
<p class="form-ok">Thank you for applying. Our HR team will review your profile.</p></div></section>""")
    page("career/index.html", "Careers | The Vijayran Palace, Jaipur", "Build your career in luxury hospitality at The Vijayran Palace, Jaipur.", body)

    # TERMS
    T = [("Proprietary information and copyright","All information on this website, including text, images, videos, animation, sounds, links, software and other materials, is the exclusive property of The Vijayran Palace and its affiliated and related entities. No one may display, recreate, link, publish, broadcast, translate, modify, transfer, sell or otherwise deal with this information by any means without prior written permission from The Vijayran Palace."),
         ("Trademark notice","This website contains the trademarks VIJAYRAN, VIJAYRAN PALACE and other “VIJAYRAN”-prefixed trademarks and business identifiers owned by Vijayran Palace. These are protected under national and international law and may not be reproduced, copied or reused without prior written consent."),
         ("Purchase of service",f"Services are purchased from Vijayran Palace, a company registered in Jaipur with its office at {ADDRESS}. For any queries, contact our customer service team at {EMAIL_SALES} or +91 99997 66809."),
         ("Disclaimer","Every effort is made to ensure that the information on this website, including rooms and availability, is accurate and reliable. However, Vijayran is not bound by any omission or error and is not liable for any loss arising from one. Vijayran makes no warranty regarding this website or any linked site, including merchantability, completeness, fitness for a particular purpose, or freedom from viruses or other harmful code, and may revise these terms or any information at any time without notice. Under no circumstances will Vijayran be liable for any loss, injury, damage, harm or expense, direct or indirect, arising in any way from the unavailability of information, marks, the website or any link, including through the negligence of Vijayran's staff or officers."),
         ("Communications","Communications with Vijayran, including queries, suggestions and feedback, are not treated as confidential. Vijayran may reproduce, use or disclose them, and may use any ideas, concepts or techniques they contain for any purpose. Customers who send confidential, personal or private information by email do so at their own risk."),
         ("Links","This website may include links to sites not connected to Vijayran. Vijayran does not verify or monitor such content and does not endorse or recommend the material or services they provide. Please use your own judgement when visiting them."),
         ("Applicable law and jurisdiction",f"Any dispute relating to this website is governed by the laws of Rajasthan, India, and you agree to submit to the non-exclusive jurisdiction of the courts of Rajasthan. Please direct all enquiries to The Vijayran Palace by Royal Quest Resorts, {ADDRESS}.")]
    body = ph("Legal", "Terms &amp; Conditions") + '<section class="prose"><p>By accessing, viewing or using this website, you confirm that you have read these terms and conditions and agree to be bound by them. If you do not accept any of them, please discontinue your access to and use of the website.</p>' + "".join(f"<h3>{h}</h3><p>{t}</p>" for h, t in T) + "</section>"
    page("terms-and-conditions/index.html", "Terms & Conditions | The Vijayran Palace", "Terms and conditions for using the website of The Vijayran Palace, Jaipur.", body, light=True)

    # sitemap / robots
    locs = []
    for d, _, fs in os.walk(OUT):
        if "index.html" in fs and not any(x in d for x in ("/assets", "/media", "/_build", "/.git")):
            rel = os.path.relpath(d, OUT); locs.append(SITE if rel == "." else SITE + rel + "/")
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{l}</loc></url>\n" for l in sorted(locs)) + "</urlset>\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n")
    print("pages:", len(locs))

if __name__ == "__main__":
    build()
