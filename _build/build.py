#!/usr/bin/env python3
"""The Vijayran Palace — static site generator (Sujan design system).
python3 build.py  ->  ./dist   (every page keeps its existing royalquestresorts.com URL)"""
import os, shutil, html, json
from data import *
from gen_sketch_svg import get_sketch_svg
from gen_map_svg import get_map_svg

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

MAP = open(os.path.join(ROOT, "assets", "img", "map-jaipur.svg"), encoding="utf-8").read().replace("<svg ", '<svg class="map-ill" ', 1)

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
 ("Experience", [("Royal Palace Stroll","royal-heritage-stroll"),("Weddings","best-destination-wedding-venues-in-jaipur"),("Activities & Spa","yoga-spa-pool-luxury-resort-jaipur-rajasthan"),("Dining","best-luxury-dining-resort-in-jaipur"),
                 ("Attractions","top-holiday-resort-in-jaipur-for-family"),("Day Outing","resort-near-jaipur-for-day-outing"),("Packages & Offers","winter-summer-package"),("Gallery","heritage-wedding-resort-jaipur-rajasthan")]),
]
MENU_SM = [("Our Story","about-us-luxury-resort-of-jaipur"),("Royal Palace Stroll","royal-heritage-stroll"),("Guest Reviews","testimonial"),("Contact","get-in-touch-resort-in-kukas-jaipur"),("FAQ","faq"),("Careers","career")]

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
 <div class="nav-l"><button class="nav-menu" aria-label="Menu" aria-expanded="false"><span class="burger"><i></i><i></i><i></i></span><span class="roll"><span>Menu</span><span>Close</span></span></button><button class="wx-chip" data-wx="chip" aria-label="Live weather at the palace, tap to switch °C/°F" hidden><span class="wx-ico" data-wx="icon"></span><span data-wx="place">Kukas, Jaipur</span><b data-wx="temp"></b></button></div>
 <a class="logo" href="{u()}" aria-label="The Vijayran Palace by Royal Quest Resorts — home"><img class="lg-w" src="{P.R}assets/img/logo-white.svg" alt="The Vijayran Palace by Royal Quest Resorts" width="323" height="72"><img class="lg-g" src="{P.R}assets/img/logo-gold.svg" alt="" aria-hidden="true" width="323" height="72"></a>
 <div class="book"><button class="btn btn-gold" aria-haspopup="true">{roll('Book now')}{ARW}</button><div class="book-panel">{bk}</div></div>
</header>
<div class="menu" aria-label="Site menu"><div class="menu-in"><div class="menu-grid">{cols}{sm}<div class="m-feat">{fc}</div></div>{m_bot}</div></div>"""

def footer():
    links = [("Our Stays","accommodation"),("Royal Palace Stroll","royal-heritage-stroll"),("Our Story","about-us-luxury-resort-of-jaipur"),("Weddings","best-destination-wedding-venues-in-jaipur"),
             ("Activities & Spa","yoga-spa-pool-luxury-resort-jaipur-rajasthan"),("Dining","best-luxury-dining-resort-in-jaipur"),("Attractions","top-holiday-resort-in-jaipur-for-family"),
             ("Day Outing","resort-near-jaipur-for-day-outing"),("Packages & Offers","winter-summer-package"),("Gallery","heritage-wedding-resort-jaipur-rajasthan"),
             ("Guest Reviews","testimonial"),("FAQ","faq"),("Careers","career"),("Contact","get-in-touch-resort-in-kukas-jaipur"),("Terms & Conditions","terms-and-conditions")]
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

def intro(title_html, text, tpl=False, sketch=True, ornament=True, kicker="THE ROYAL SANCTUARY &middot; KUKAS, JAIPUR"):
    t = f'<h2 class="{"h-xl" if tpl else "t-xl"}" data-split>{title_html}</h2>'
    sk = sketch_markup() if sketch else "<span></span>"
    body_html = text if "<p>" in text else f"<p>{text}</p>"
    return (f'<div class="intro-wrap"><section class="intro{" c-tpl" if tpl else ""}">{ORN if ornament and tpl else ""}<div class="intro-title">{t}</div>'
            f'<div class="intro-row"><div class="intro-copy"><p class="lbl intro-kicker">{kicker}</p><div class="p-l" data-split="text">{body_html}</div>'
            f'<p class="intro-foot">Kukas &middot; Aravalli Foothills &middot; 12 km North of Amber Fort</p></div><span></span>{sk}</div></section></div>')

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

def collection(title, text, cta, items, bg="", extra_attrs="", kicker="SANCTUARY &amp; ACCOMMODATION"):
    k_html = f'<p class="lbl">{kicker}</p>' if kicker else ""
    return (f'<section class="coll" data-rail{bg}{extra_attrs}><div class="coll-head"><div class="tx">{k_html}<h2 class="coll-title" data-split>{title}</h2><p class="p" data-split="text">{text}</p></div>{cta}</div>'
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
    # Curate 4 rich, descriptive, alternating horizontal chapters tailored to each page
    first_img = images[0].split("/")[-1] if images else ""
    if "In-Yoga" in first_img:
        chapters = [
            {
                "roman": "I",
                "nav": "Dawn Rituals",
                "kicker": "CHAPTER I &middot; DAWN IN THE ARAVALLIS",
                "title": title_html,
                "p1": text,
                "p2": "As golden morning light spills across the palace lawns and ancient mountain ridges, guided pranayama and hatha yoga awaken the senses to birdsong and crisp Aravalli air.",
                "img": "2021/05/In-Yoga-1.jpg",
                "cap": "Sunrise Yoga &amp; Pranayama on the Palace Lawns",
                "details": [("Dawn", "Guided Yoga"), ("150+", "Native Birdlife"), ("Open Sky", "Garden Lawns")]
            },
            {
                "roman": "II",
                "nav": "Equestrian Trails",
                "kicker": "CHAPTER II &middot; ROYAL MARWARI RIDES",
                "title": 'Spirited <span class="soft">Marwari</span> trails &amp; desert excursions',
                "p1": "Saddle up on Rajasthan's noble inward-eared Marwari horses or set out on a unhurried camel excursion along historic foothill paths and quiet rural hamlets.",
                "p2": "Accompanied by seasoned palace grooms, every trail winds past wild khejri groves, ancient watchtowers, and timeless pastoral landscapes untouched by city haste.",
                "img": "2021/06/horse-img.jpg",
                "cap": "Equestrian &amp; Camel Trails Through Kukas",
                "details": [("Marwari", "Thoroughbreds"), ("Foothills", "Guided Trails"), ("Bespoke", "Sunset Carriages")]
            },
            {
                "roman": "III",
                "nav": "Wilderness Safaris",
                "kicker": "CHAPTER III &middot; INTO THE WILDERNESS",
                "title": 'Open-air <span class="soft">Aravalli</span> jeep safaris &amp; birding',
                "p1": "Venture off the beaten track in custom open-top 4x4 jeeps across rugged dry-deciduous valleys, rocky escarpments, and hidden waterholes around Amer and Kukas.",
                "p2": "Spot peacocks, nilgai, and migratory flocks in their natural sanctuary before returning for a private bush high tea overlooking the hills.",
                "img": "2021/05/jeep-safari.jpg",
                "cap": "Off-Road 4x4 Wilderness Expeditions",
                "details": [("4x4", "Open Jeep"), ("Amer", "Valley Routes"), ("Golden Hour", "High Tea")]
            },
            {
                "roman": "IV",
                "nav": "Dusk & Folk Nights",
                "kicker": "CHAPTER IV &middot; TWILIGHT AT AMBAR TAAL",
                "title": 'Mirror-still waters &amp; <span class="soft">folk music</span> under the stars',
                "p1": "Unwind beside the turquoise expanse of Ambar Taal as palace domes and carved chhatris shimmer across the water in the amber glow of dusk.",
                "p2": "By nightfall, lanterns flicker to life across the courtyard for soul-stirring Ravanahatha ballads, swirling Kalbeliya, and Ghoomar beneath a canopy of desert stars.",
                "img": "2021/06/ambertallpool-img.jpg",
                "cap": "Ambar Taal Infinity Reflections at Dusk",
                "details": [("Ambar Taal", "Palace Pool"), ("Kalbeliya", "Live Folk Arts"), ("Starlit", "Courtyards")]
            }
        ]
    elif "g2.jpg" in first_img:
        chapters = [
            {
                "roman": "I",
                "nav": "Our Philosophy",
                "kicker": "CHAPTER I &middot; A FORTRESS OF SOLITUDE",
                "title": title_html,
                "p1": text,
                "p2": "Conceived as an intimate sanctuary far from urban clamour, every courtyard, archway, and colonnade invites guests to slow down and inhabit the poise of royal Rajasthan.",
                "img": "2021/06/g2.jpg",
                "cap": "Raj Mahal &amp; Artisanal Rajasthani Interiors",
                "details": [("Kukas", "Aravalli Estate"), ("35", "Suites &amp; Villas"), ("Heritage", "Architecture")]
            },
            {
                "roman": "II",
                "nav": "Living Craft",
                "kicker": "CHAPTER II &middot; ARTISANAL HERITAGE",
                "title": 'Hand-chiselled <span class="soft">jharokhas</span> &amp; royal tapestries',
                "p1": "Generations of Rajasthani stone-carvers, fresco painters, and textile masters shaped our cusped arches, pierced lattice screens, and mirror-inlaid chambers.",
                "p2": "Sunlight filters through carved sandstone balconies onto hand-knotted carpets and period furnishings, turning every corridor into a living gallery of Rajputana craft.",
                "img": "2021/06/g4.jpg",
                "cap": "Hand-Carved Sandstone Jharokhas &amp; Courtyards",
                "details": [("Sandstone", "Carved Jali"), ("Artisanal", "Fresco &amp; Mirror"), ("Bespoke", "Tapestries")]
            },
            {
                "roman": "III",
                "nav": "Grand Lawns",
                "kicker": "CHAPTER III &middot; PALATIAL COURTS &amp; GARDENS",
                "title": 'Illuminated <span class="soft">amphitheatres</span> &amp; Mughal gardens',
                "p1": "From the terraced stone stage of Rang Mahal to the geometric fountain courts of Char Bagh, seven distinct outdoor and indoor settings unfold across the estate.",
                "p2": "Fragrant frangipani, bougainvillea cascades, and torchlit walkways frame intimate family gatherings and grand royal celebrations alike.",
                "img": "2021/06/g5.jpg",
                "cap": "Rang Mahal Heritage Stage &amp; Manicured Lawns",
                "details": [("7", "Palace Venues"), ("1,500", "Guest Capacity"), ("Char Bagh", "Fountain Courts")]
            },
            {
                "roman": "IV",
                "nav": "Aravalli Vistas",
                "kicker": "CHAPTER IV &middot; THE ANCIENT RIDGE",
                "title": 'Cradled by India’s <span class="soft">oldest</span> mountain range',
                "p1": "Rising straight behind our domes, the timeless Aravalli hills wrap the palace in emerald monsoon greens and warm golden-ochre winter light.",
                "p2": "Only twelve kilometres from historic Amber Fort yet worlds apart in stillness, The Vijayran Palace welcomes every guest with open arms and courtly grace.",
                "img": "2021/05/view.jpg",
                "cap": "Unbroken Aravalli Mountain Panorama",
                "details": [("12 km", "To Amber Fort"), ("19 km", "To Pink City"), ("Atithi", "Devo Bhava")]
            }
        ]
    else:
        chapters = [
            {
                "roman": "I",
                "nav": "Architecture",
                "kicker": "CHAPTER I &middot; IMPERIAL ARCHITECTURE",
                "title": title_html,
                "p1": text,
                "p2": "Beyond the ceremonial yellow-sandstone Gajdwar portal, soaring chhatri cupolas, scalloped Mehrab colonnades, and hand-carved jharokhas rise in quiet majesty against the ancient Aravalli ridge.",
                "img": "2021/06/Main-Gate.jpg",
                "cap": "The Imperial Gajdwar Sandstone Portal at Kukas",
                "details": [("Kukas", "Aravalli Foothills"), ("Rajputana", "Carved Sandstone"), ("12 km", "North of Amer")]
            },
            {
                "roman": "II",
                "nav": "Private Sanctuaries",
                "kicker": "CHAPTER II &middot; THIRTY-FIVE ROYAL ABODES",
                "title": 'Private-pool villas &amp; <span class="soft">carved haveli</span> suites',
                "p1": "Each of our thirty-five residences is conceived as a private royal sanctuary—from sprawling Presidential Villas with secluded plunge pools and walled gardens to sunlit Terrace and Courtyard Haveli Suites.",
                "p2": "Period furnishings, hand-loomed Rajasthani tapestries, and deep marble baths pair effortlessly with attentive round-the-clock palace service.",
                "img": "2021/04/Villa-Master-Room.jpg",
                "cap": "Presidential Villas &amp; Heritage Haveli Suites",
                "details": [("35", "Villas &amp; Suites"), ("Private", "Pools &amp; Aangans"), ("1,345 sq ft", "Courtyard Suites")]
            },
            {
                "roman": "III",
                "nav": "Ambar Taal",
                "kicker": "CHAPTER III &middot; SERENITY &amp; REFLECTION",
                "title": 'Turquoise stillness <span class="soft">beneath</span> palace chhatris',
                "p1": "At the heart of the estate, the mirror-still waters of Ambar Taal reflect golden sandstone baradaris, white marble finials, and drifting mountain clouds from dawn until starlight.",
                "p2": "Mornings unfold with birdsong yoga on dewy lawns and horseback rides through rural trails, giving way to lazy poolside afternoons and candlelit dining.",
                "img": "2021/06/ambertallpool-img.jpg",
                "cap": "Ambar Taal Reflecting the Palace Baradari",
                "details": [("Ambar Taal", "Infinity Pool"), ("Organic", "Kitchen Gardens"), ("Starlit", "Al Fresco Dining")]
            },
            {
                "roman": "IV",
                "nav": "Courtly Grace",
                "kicker": "CHAPTER IV &middot; LIVING RAJPUTANA HOSPITALITY",
                "title": 'Where <span class="soft">atithi devo bhava</span> is a living art',
                "p1": "Rooted in the timeless Indian ethos of honouring every guest as royalty, our culinary brigade, folk musicians, and concierges craft stays that linger in memory long after departure.",
                "p2": "Whether arriving for a quiet mountain retreat, a family celebration, or a grand destination wedding, you are welcomed into the warmth of a living palace.",
                "img": "2021/06/g4.jpg",
                "cap": "Saffron-Draped Sandstone Pavilions &amp; Courtyards",
                "details": [("7", "Palatial Venues"), ("24/7", "Royal Concierge"), ("100%", "Bespoke Service")]
            }
        ]

    nav_btns = "".join(
        f'<button type="button" class="sc-step{" is-active" if i == 0 else ""}" data-sc-step="{i}">'
        f'<span class="sc-step-num">{c["roman"]}</span>'
        f'<span class="sc-step-lbl">{c["nav"]}</span>'
        f'</button>'
        for i, c in enumerate(chapters)
    )

    chapters_html = ""
    for i, c in enumerate(chapters):
        alt_cls = " is-reverse" if i % 2 == 1 else ""
        act_cls = " is-active" if i == 0 else ""
        details_html = "".join(
            f'<div class="sc-detail"><span class="sc-det-v">{v}</span><span class="sc-det-k">{k}</span></div>'
            for v, k in c["details"]
        )
        chapters_html += f"""
      <article class="sc-chapter{alt_cls}{act_cls}" data-chapter="{i}">
        <div class="sc-text">
          <p class="sc-kicker">{c["kicker"]}</p>
          <h2 class="sc-title">{c["title"]}</h2>
          <div class="sc-ornament">{ORN}</div>
          <p class="sc-p">{c["p1"]}</p>
          <p class="sc-p sc-p-sub">{c["p2"]}</p>
          <div class="sc-details">{details_html}</div>
          <div class="sc-cta">{cta}</div>
        </div>
        <div class="sc-media">
          <div class="sc-frame">
            {img(c["img"], c["cap"], cls="sc-img")}
          </div>
          <div class="sc-cap-row">
            <span class="sc-cap-idx">{c["roman"]} / IV</span>
            <span class="sc-cap-txt">{c["cap"]}</span>
          </div>
        </div>
      </article>"""

    return f"""<section class="story-chronicle" id="story">
  <div class="sc-pin">
    <div class="sc-topbar">
      <span class="sc-brand">THE PALACE CHRONICLE &middot; KUKAS, JAIPUR</span>
      <div class="sc-steps" role="navigation" aria-label="Story Chapters">
        {nav_btns}
        <div class="sc-progress"><i class="sc-progress-fill"></i></div>
      </div>
    </div>
    <div class="sc-stage">
      {chapters_html}
    </div>
  </div>
</section>"""

DAY_CLOCK_ACTIVITIES = [
  {"time": "5:30 AM",  "period": "Dawn",      "angle_h": 162.5, "angle_m": 180,
   "label": "Sunrise Yoga & Pranayama",
   "img":   "2021/05/In-Yoga-1.jpg",
   "desc":  "Begin with guided yoga to birdsong as the sun crests the Aravalli ridge. Breathe in the cool dawn air and greet the day in stillness.",
   "palette": "#e8b89a", "txt": "#5c2f1a"},
  {"time": "8:00 AM",  "period": "Morning",   "angle_h": 240,   "angle_m": 0,
   "label": "Marwari Horseback Ride",
   "img":   "2021/06/horse-img.jpg",
   "desc":  "Saddle up on a noble Marwari stallion and trot through ancient Aravalli trails as golden morning light dapples the foothills.",
   "palette": "#f4e3b2", "txt": "#5a3e10"},
  {"time": "2:00 PM",  "period": "Afternoon", "angle_h": 60,    "angle_m": 0,
   "label": "Royal Jeep Safari",
   "img":   "2021/05/jeep-safari.jpg",
   "desc":  "Venture deep into the Aravallis on an open jeep safari. Spot migratory birds, ancient rock formations and wild Rajasthan in full afternoon light.",
   "palette": "#f0ead8", "txt": "#3a2a10"},
  {"time": "6:30 PM",  "period": "Evening",   "angle_h": 195,   "angle_m": 180,
   "label": "Rajasthani Folk Evening",
   "img":   "2021/05/rajfolk.jpg",
   "desc":  "As dusk paints the hills amber, the palace courtyard comes alive with Kalbeliya dance, Ravanahatha strings and the warm glow of diyas.",
   "palette": "#c96a2a", "txt": "#fff3e8"},
  {"time": "9:00 PM",  "period": "Night",     "angle_h": 270,   "angle_m": 0,
   "label": "Starlit Palace Dinner",
   "img":   "2021/06/g3.jpg",
   "desc":  "Dine under a canopy of stars in the palace lawns. Crystal candelabras, royal thalis and the quiet symphony of the Aravalli night sky.",
   "palette": "#152038", "txt": "#d4af6e"},
]

def day_clock_section():
    slots_js = json.dumps([
        {"period": s["period"], "time": s["time"],
         "angle_h": s["angle_h"], "angle_m": s["angle_m"],
         "palette": s["palette"], "txt": s["txt"]}
        for s in DAY_CLOCK_ACTIVITIES
    ])
    import math as _m
    CX, CY = 100, 100

    # ── ORNATE VINTAGE ROYAL CLOCK DIAL ──────────────────────────────
    # SVG gradients (pure vector enamel & bezel gradients, no clipped filter)
    dial_defs = (
      '<defs>'
      '<radialGradient id="dcsDial" cx="42%" cy="35%" r="68%">'
        '<stop offset="0%" stop-color="#fffef8"/>'
        '<stop offset="55%" stop-color="#f9f4e6"/>'
        '<stop offset="100%" stop-color="#ede4cc"/>'
      '</radialGradient>'
      '<radialGradient id="dcsBezel" cx="38%" cy="30%" r="72%">'
        '<stop offset="0%" stop-color="#2e1c0c"/>'
        '<stop offset="100%" stop-color="#0e0908"/>'
      '</radialGradient>'
      '</defs>'
    )

    # Outer dark ormolu bezel
    bezel = (
      f'<circle cx="{CX}" cy="{CY}" r="98" fill="url(#dcsBezel)"/>'
      f'<circle cx="{CX}" cy="{CY}" r="96" fill="none" stroke="#d4aa50" stroke-width="1.6"/>'
      f'<circle cx="{CX}" cy="{CY}" r="93.5" fill="none" stroke="#8a6520" stroke-width="0.4"/>'
    )

    # 12 diamond gems + 12 accent circles on the bezel at every 15°
    gems = ""
    for i in range(24):
        a = _m.radians(i * 15)
        bx = CX + 90 * _m.sin(a); by = CY - 90 * _m.cos(a)
        if i % 2 == 0:
            # Larger diamond at every 30° (gem setting)
            s = 3.4
            gems += (f'<polygon points="{bx:.1f},{by-s:.1f} {bx+s*0.65:.1f},{by:.1f} '
                     f'{bx:.1f},{by+s:.1f} {bx-s*0.65:.1f},{by:.1f}" fill="#d4aa50" opacity="0.95"/>'
                     f'<line x1="{bx-s+0.5:.1f}" y1="{by:.1f}" x2="{bx+s-0.5:.1f}" y2="{by:.1f}" '
                     f'stroke="#8a6520" stroke-width="0.4" opacity="0.6"/>')
        else:
            # Small accent circle between gems
            gems += f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="1.1" fill="#c9a24e" opacity="0.55"/>'

    # Inner bezel rings (double-line border, classic watchmaking detail)
    inner_bezel = (
      f'<circle cx="{CX}" cy="{CY}" r="84" fill="none" stroke="#c9a24e" stroke-width="2.2"/>'
      f'<circle cx="{CX}" cy="{CY}" r="82" fill="none" stroke="#f8f0d0" stroke-width="0.6"/>'
      f'<circle cx="{CX}" cy="{CY}" r="81.3" fill="none" stroke="#8a6520" stroke-width="0.4"/>'
    )

    # Cream enamel dial face
    dial_face = f'<circle cx="{CX}" cy="{CY}" r="80.5" fill="url(#dcsDial)"/>'

    # Guilloche sunburst — 72 gold radial lines from center, fading out at r=52
    guilloche = ""
    for i in range(72):
        a = _m.radians(i * 5)
        x2 = CX + 52 * _m.sin(a); y2 = CY - 52 * _m.cos(a)
        guilloche += (f'<line x1="{CX}" y1="{CY}" x2="{x2:.1f}" y2="{y2:.1f}" '
                      f'stroke="#c9a24e" stroke-width="0.3" opacity="0.13"/>')

    # Chapter ring (outer + inner boundary rings)
    chapter_rings = (
      f'<circle cx="{CX}" cy="{CY}" r="79" fill="none" stroke="#c9a24e" stroke-width="0.75"/>'
      f'<circle cx="{CX}" cy="{CY}" r="70" fill="none" stroke="#c9a24e" stroke-width="0.5"/>'
    )

    # 60-minute ticks along the chapter ring
    ticks = ""
    for i in range(60):
        a = _m.radians(i * 6)
        is_hour = i % 5 == 0
        r_out, r_in = 79, (72 if is_hour else 76)
        sw = "1.7" if is_hour else "0.8"
        sc = "#c9a24e" if is_hour else "#9a8040"
        x1 = CX + r_out * _m.sin(a); y1 = CY - r_out * _m.cos(a)
        x2 = CX + r_in  * _m.sin(a); y2 = CY - r_in  * _m.cos(a)
        ticks += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                  f'stroke="{sc}" stroke-width="{sw}" stroke-linecap="round"/>')

    # All 12 Roman numerals at r=63 (italic serif, royal)
    roman_all = ["XII","I","II","III","IV","V","VI","VII","VIII","IX","X","XI"]
    nums = ""
    for i, r in enumerate(roman_all):
        a = _m.radians(i * 30)
        rx = CX + 63 * _m.sin(a); ry = CY - 63 * _m.cos(a)
        nums += (f'<text x="{rx:.1f}" y="{ry:.1f}" text-anchor="middle" '
                 f'dominant-baseline="middle" class="dcs-num">{r}</text>')

    # Inner decorative ring + 8-petal lotus medallion
    medallion = f'<circle cx="{CX}" cy="{CY}" r="52" fill="none" stroke="#c9a24e" stroke-width="0.5" opacity="0.5"/>'
    for i in range(8):
        a = _m.radians(i * 45)
        x1 = CX + 4.5 * _m.sin(a); y1 = CY - 4.5 * _m.cos(a)
        x2 = CX + 12  * _m.sin(a); y2 = CY - 12  * _m.cos(a)
        medallion += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                      f'stroke="#c9a24e" stroke-width="1.0" opacity="0.5"/>')
    medallion += f'<circle cx="{CX}" cy="{CY}" r="13" fill="none" stroke="#c9a24e" stroke-width="0.6" opacity="0.4"/>'

    # Manufacturer / palace name on dial (classic watchmaking style, below center)
    brand = (f'<text x="{CX}" y="{CY+34}" text-anchor="middle" class="dcs-brand">VIJAYRAN PALACE</text>'
             f'<text x="{CX}" y="{CY+39.5}" text-anchor="middle" class="dcs-brand-sub">· JAIPUR ·</text>')

    # Assemble full dial layers (without hands — those follow in the HTML template)
    clock_dial = dial_defs + bezel + gems + inner_bezel + dial_face + guilloche + chapter_rings + ticks + nums + medallion + brand
    # Build slides
    slides_html = ""
    for i, s in enumerate(DAY_CLOCK_ACTIVITIES):
        active = " is-active" if i == 0 else ""
        slides_html += f"""
      <div class="dcs-slide{active}" data-idx="{i}">
        <div class="dcs-img-wrap">
          <div class="dcs-img-inner">{img(s["img"], s["label"])}</div>
        </div>
        <div class="dcs-info">
          <span class="dcs-badge">{s["period"]}</span>
          <h3 class="dcs-name">{s["label"]}</h3>
          <p class="dcs-desc">{s["desc"]}</p>
          <a class="dcs-cta" href="{u("yoga-spa-pool-luxury-resort-jaipur-rajasthan")}">Explore All Experiences {ARR_R}</a>
        </div>
      </div>"""
    # Build dot nav
    dots_html = ""
    for i, s in enumerate(DAY_CLOCK_ACTIVITIES):
        active = " is-active" if i == 0 else ""
        dots_html += f'<button class="dcs-dot{active}" data-idx="{i}" aria-label="{s["period"]}"><span class="dcs-dot-label">{s["period"]}</span></button>'

    return f"""
<section class="day-clock-section" id="experiences" data-fade>
  <div class="dcs-eyebrow">
    <p class="lbl">CURATED EXPERIENCES</p>
    <h2 class="dcs-heading">A Day at The Palace</h2>
    <p class="dcs-sub">From the first light of dawn to the stillness of night &mdash; every hour holds a royal experience.</p>
  </div>
  <div class="dcs-inner">
    <!-- LEFT: Animated Analog Clock -->
    <div class="dcs-clock-col">
      <div class="dcs-clock-wrap" id="dcsClockWrap">
        <svg class="dcs-clock-face" id="dcsClockSvg" viewBox="-8 -8 216 216" aria-hidden="true">
          {clock_dial}
          <!-- Hour hand: Breguet spade-style, ornate dark espresso -->
          <g id="dcsHourHand" style="transform:rotate(162.5deg);transform-origin:100px 100px;transition:transform 1.4s cubic-bezier(0.34,1.4,0.64,1)">
            <path class="dcs-hand-hour" d="M100 114 C97.2 110 96.8 105 97.4 100 L98 88 L98.5 70 C98 65 97.5 61 100 59.5 C102.5 61 102 65 101.5 70 L102 88 L102.6 100 C103.2 105 102.8 110 100 114Z"/>
            <!-- Spade tip accent line -->
            <line x1="100" y1="64" x2="100" y2="72" stroke="#c9a24e" stroke-width="0.6" opacity="0.7"/>
          </g>
          <!-- Minute hand: slim gold lance -->
          <g id="dcsMinHand" style="transform:rotate(180deg);transform-origin:100px 100px;transition:transform 1.4s cubic-bezier(0.34,1.4,0.64,1)">
            <path class="dcs-hand-min" d="M100 117 C98.8 112 98.8 106 99.3 102 L99.5 65 L100 24 L100.5 65 L100.7 102 C101.2 106 101.2 112 100 117Z"/>
          </g>
          <!-- Center cap: gold disc with espresso boss -->
          <circle cx="100" cy="100" r="7" class="dcs-pivot-outer"/>
          <circle cx="100" cy="100" r="4.5" class="dcs-pivot-inner"/>
          <circle cx="100" cy="100" r="2" fill="#d4aa50"/>
        </svg>
        <div class="dcs-time-display">
          <span class="dcs-time-period" id="dcsTimePeriod">Dawn</span>
          <span class="dcs-time-val" id="dcsTimeVal">5:30 AM</span>
        </div>
      </div>
      <div class="dcs-dots" role="tablist">
        {dots_html}
      </div>
    </div>

    <!-- RIGHT: Activity Display -->
    <div class="dcs-activity-col" id="dcsActivityCol">
      <div class="dcs-slides">
        {slides_html}
      </div>
    </div>
  </div>
  <script>
  (function(){{
    var SLOTS={slots_js};
    var section=document.getElementById('experiences');
    if(!section)return;
    var slides=[].slice.call(section.querySelectorAll('.dcs-slide'));
    var dots=[].slice.call(section.querySelectorAll('.dcs-dot'));
    var hourHand=section.querySelector('#dcsHourHand');
    var minHand=section.querySelector('#dcsMinHand');
    var timePeriod=section.querySelector('#dcsTimePeriod');
    var timeVal=section.querySelector('#dcsTimeVal');
    var DURATION=6000;
    var current=0;
    var timer=null;
    var hovered=false;
    var currentHourRot=SLOTS[0].angle_h;
    var currentMinRot=SLOTS[0].angle_m;

    function showSlot(idx){{
      slides[current].classList.remove('is-active');
      dots[current].classList.remove('is-active');
      current=(idx+SLOTS.length)%SLOTS.length;
      slides[current].classList.add('is-active');
      dots[current].classList.add('is-active');
      var s=SLOTS[current];

      // Always advance forward continuously (never rotate backwards / reverse)
      var targetH=s.angle_h;
      var deltaH=(targetH - (currentHourRot % 360) + 360) % 360;
      if(deltaH === 0 && idx !== 0) deltaH = 360;
      currentHourRot += deltaH;

      var targetM=s.angle_m;
      var deltaM=(targetM - (currentMinRot % 360) + 360) % 360;
      if(deltaM === 0 && idx !== 0) deltaM = 360;
      currentMinRot += deltaM;

      hourHand.style.transform='rotate('+currentHourRot+'deg)';
      minHand.style.transform='rotate('+currentMinRot+'deg)';
      timePeriod.textContent=s.period;
      timeVal.textContent=s.time;
      section.style.setProperty('--dcs-pal',s.palette);
      section.style.setProperty('--dcs-txt',s.txt);
    }}

    function startTimer(){{
      clearTimeout(timer);
      timer=setTimeout(function(){{
        if(!hovered)showSlot(current+1);
        startTimer();
      }},DURATION);
    }}

    dots.forEach(function(d,i){{
      d.addEventListener('click',function(){{showSlot(i);startTimer();}});
    }});

    section.addEventListener('mouseenter',function(){{hovered=true;clearTimeout(timer);}});
    section.addEventListener('mouseleave',function(){{hovered=false;startTimer();}});

    showSlot(0);
    if(typeof ScrollTrigger!=='undefined'){{
      ScrollTrigger.create({{trigger:'#experiences',start:'top 75%',once:true,onEnter:startTimer}});
    }}else{{setTimeout(startTimer,800);}}
  }})();
  </script>
</section>"""

def royal_expedition_section():
    stops = [
        {
            "id": "airport",
            "num": "01",
            "name": "Jaipur Airport",
            "tag": "30 km · 45m",
            "full_dist": "30 KM FROM PALACE · ~45 MIN DRIVE",
            "role": "Gateway of Rajasthan",
            "desc": "Where your princely journey begins. Chauffeur-driven luxury palace transfers glide northwards along the scenic highway directly into the peaceful Aravalli valley.",
            "tip": "Private airport transfers can be pre-arranged with the palace concierge."
        },
        {
            "id": "pinkcity",
            "num": "02",
            "name": "Hawa Mahal & Pink City",
            "tag": "19 km · 35m",
            "full_dist": "19 KM FROM PALACE · ~35 MIN DRIVE",
            "role": "Palace of Winds & Bazaars",
            "desc": "Maharaja Sawai Pratap Singh's 1799 architectural masterpiece with 953 honeycombed jharokhas, adjacent to the City Palace, Jantar Mantar, and bustling Johari gem bazaar.",
            "tip": "Visit in the morning when the rising sun illuminates the pink sandstone facade."
        },
        {
            "id": "jalmahal",
            "num": "03",
            "name": "Jal Mahal",
            "tag": "15 km · 25m",
            "full_dist": "15 KM FROM PALACE · ~25 MIN DRIVE",
            "role": "Sunlit Water Palace",
            "desc": "An ethereal pale yellow sandstone palace resting gracefully amidst the turquoise waters of Man Sagar Lake, framed by ancient rolling Aravalli peaks.",
            "tip": "A breathtaking photography viewpoint along Amer Road, especially at twilight."
        },
        {
            "id": "amber",
            "num": "04",
            "name": "Amber Fort",
            "tag": "12 km · 18m",
            "full_dist": "12 KM FROM PALACE · ~18 MIN DRIVE",
            "role": "Citadel of the Kachhwahas",
            "desc": "The colossal 16th-century mountain stronghold renowned for the glittering Sheesh Mahal (Mirror Palace), majestic elephant ramparts, and Maota Lake reflections.",
            "tip": "Enjoy the evening sound-and-light show before returning for high tea at the palace."
        },
        {
            "id": "vijayran",
            "num": "05",
            "name": "The Vijayran Palace",
            "tag": "Kukas · Sanctuary",
            "full_dist": "DESTINATION · KUKAS IN THE ARAVALLIS",
            "role": "Your Palatial Sanctuary",
            "desc": "Nestled in secluded tranquility among the ancient Aravalli hills. Thirty-five royal haveli suites and private pool villas, lush Mughal gardens, and timeless Rajasthani royalty.",
            "tip": "The ultimate haven for stillness, royal dining, and bespoke heritage stays."
        }
    ]

    stop_cards_html = ""
    for idx, s in enumerate(stops):
        active_cls = " is-active" if idx == 0 else ""
        stop_cards_html += (
            f'<button class="exp-stop-card{active_cls}" role="tab" data-stop-idx="{idx}" aria-selected="{"true" if idx==0 else "false"}" '
            f'data-name="{s["name"]}" data-dist="{s["full_dist"]}" data-role="{s["role"]}" data-desc="{s["desc"]}" data-tip="{s["tip"]}">'
            f'<span class="exp-stop-top"><span class="exp-stop-num">{s["num"]}</span><span class="exp-stop-tag">{s["tag"]}</span></span>'
            f'<span class="exp-stop-name">{s["name"]}</span>'
            f'<span class="exp-stop-role">{s["role"]}</span>'
            f'<span class="exp-stop-bar"><i class="exp-bar-fill"></i></span>'
            f'</button>'
        )

    s0 = stops[0]
    return f"""<section class="royal-expedition" id="territory-map" data-fade>
  <div class="exp-inner">
    <div class="exp-header" data-fade>
      <p class="exp-kicker lbl">ROYAL ITINERARY &amp; TERRITORY</p>
      <h2 class="exp-title" data-split>A Journey Through the Princely Realm</h2>
      <p class="exp-lead" data-split="text">Follow the historic royal route from the gates of Jaipur through ancient fortresses and serene waters, arriving at the secluded sanctuary of The Vijayran Palace in the Aravalli hills.</p>
    </div>

    <!-- 5-Stop Interactive Milestone Journey Bar -->
    <div class="exp-stop-cards" role="tablist" aria-label="Royal Route Milestones" data-fade>
      {stop_cards_html}
    </div>

    <!-- Interactive Toolbar: Auto-Ride, Reset, Live Status, 3D Perspective Hint -->
    <div class="exp-toolbar" data-fade>
      <div class="exp-tb-left">
        <button class="exp-btn exp-btn-play" id="expPlayBtn" aria-label="Toggle Royal Journey">
          <svg class="exp-icon-play" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M8 5v14l11-7z"/></svg>
          <svg class="exp-icon-pause" viewBox="0 0 24 24" fill="currentColor" width="16" height="16" style="display:none;"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
          <span id="expPlayLabel">Auto-Ride Journey</span>
        </button>
        <button class="exp-btn exp-btn-reset" id="expResetBtn" aria-label="Reset Route">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="15" height="15"><path d="M1 4v6h6M23 20v-6h-6"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/></svg>
          <span>Reset</span>
        </button>
      </div>
      <div class="exp-tb-center">
        <div class="exp-status-pill">
          <span class="exp-status-dot"></span>
          <span id="expStatusText">Embarking from Jaipur Airport (30 km)</span>
        </div>
      </div>
      <div class="exp-tb-right">
        <span class="exp-3d-hint">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" width="16" height="16"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          <span>3D Perspective · Hover to Tilt</span>
        </span>
      </div>
    </div>

    <!-- The Grand 3D Interactive Map Stage -->
    <div class="exp-stage-3d" id="map3DStage" data-fade>
      <div class="exp-card-3d" id="map3DCard">
        <!-- SVG Map Container with Spline & Galloping Horse Rig -->
        <div class="exp-map-wrap">
          {get_map_svg(P.R)}
        </div>

        <!-- 3D Floating Landmark Vignette Card -->
        <div class="exp-float-card" id="expFloatingCard">
          <div class="efc-badge" id="efcBadge">{s0['full_dist']}</div>
          <h3 class="efc-title" id="efcTitle">{s0['name']}</h3>
          <p class="efc-desc" id="efcDesc">{s0['desc']}</p>
          <div class="efc-tip" id="efcTip"><b>Royal Tip:</b> {s0['tip']}</div>
          <div class="efc-actions">
            <a class="efc-link" href="{u('top-holiday-resort-in-jaipur-for-family')}">Explore All Jaipur Attractions &rarr;</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

def itinerary(title_html, text, cta):
    return (f'<section class="itin" id="itinerary"><div>'
            f'<p class="lbl">HERITAGE TERRITORY &middot; EXPLORATION</p>'
            f'<h2 class="t-m" data-split>{title_html}</h2>'
            f'<div class="ico">{ORN}</div>'
            f'<p class="p" data-split="text">{text}</p>'
            f'<div class="itin-milestones">'
            f'<div class="itin-ms"><span class="ims-num">12 km</span><span class="ims-lbl">Amber Fort</span></div>'
            f'<div class="itin-ms"><span class="ims-num">15 km</span><span class="ims-lbl">Jal Mahal</span></div>'
            f'<div class="itin-ms"><span class="ims-num">19 km</span><span class="ims-lbl">Hawa Mahal &amp; Pink City</span></div>'
            f'<div class="itin-ms"><span class="ims-num">30 km</span><span class="ims-lbl">Jaipur Airport</span></div>'
            f'</div>'
            f'{cta}</div><span></span>'
            f'<div class="map">'
            f'<div class="itin-wc-frame">'
            f'<img class="map-ill itin-wc-img" src="{P.R}assets/img/map-jaipur-watercolor.webp" alt="Antique watercolor pictorial map of Jaipur, Amer, and The Vijayran Palace" width="1000" height="1000" loading="lazy">'
            f'</div></div></section>')

def guest_voices():
    contexts = [
        "Presidential Villa &amp; Private Pool",
        "Aravalli Heritage Suite",
        "Royal Destination Wedding",
        "Family Retreat &amp; Bespoke Dining",
        "Folk Evenings &amp; Hospitality",
        "Courtyard &amp; Jharoka Suites",
    ]
    slides = ""
    tabs = ""
    for idx, (q, n) in enumerate(REVIEWS):
        act = " is-active" if idx == 0 else ""
        ctx = contexts[idx % len(contexts)]
        sig = n.split()[0]
        slides += (
            f'<figure class="gs-slide{act}" data-gs-slide="{idx}">'
            f'<blockquote class="gs-quote">“{q}”</blockquote>'
            f'<figcaption class="gs-attr">'
            f'<span class="gs-sig" aria-hidden="true">{sig}</span>'
            f'<span class="gs-name">{n}</span>'
            f'<span class="gs-ctx">{ctx}</span>'
            f'</figcaption>'
            f'</figure>'
        )
        tabs += (
            f'<button type="button" class="gs-tab{act}" role="tab" aria-selected="{"true" if idx == 0 else "false"}" data-gs-tab="{idx}">'
            f'<span>{n}</span>'
            f'<i class="gs-tab-bar"></i>'
            f'</button>'
        )

    return (
        f'<section class="guest-salon" id="guest-reviews">'
        f'<div class="gs-inner">'
        f'<p class="lbl gs-kicker">GUEST CHRONICLES &middot; RATED 4.5 OF 5 ON TRIPADVISOR</p>'
        f'<div class="gs-orn">{ORN}</div>'
        f'<div class="gs-stage">{slides}</div>'
        f'<div class="gs-controls">'
        f'<button type="button" class="gs-arrow" data-gs-prev aria-label="Previous review">{ARR_L}</button>'
        f'<div class="gs-tabs" role="tablist" aria-label="Guest reviews">{tabs}</div>'
        f'<button type="button" class="gs-arrow" data-gs-next aria-label="Next review">{ARR_R}</button>'
        f'</div>'
        f'<div class="gs-foot">{btn("Read all 284 reviews", u("testimonial"), "line")}</div>'
        f'</div></section>'
    )

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

    royal_icos = (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M12 2.5v2.2"/><circle cx="12" cy="2" r="0.9" fill="currentColor" stroke="none"/>'
        '<path d="M5.5 11c0-3.6 2.9-6.2 6.5-6.2s6.5 2.6 6.5 6.2"/><path d="M3.5 11h17"/>'
        '<path d="M7 11v7.5M12 11v7.5M17 11v7.5"/><path d="M4.5 18.5h15M3 21h18"/></svg>',

        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M5 20.5V11c0-2.2 1.5-3.6 3.2-3.8.5-1.8 2.1-3.2 3.8-3.7 1.7.5 3.3 1.9 3.8 3.7 1.7.2 3.2 1.6 3.2 3.8v9.5"/>'
        '<path d="M8.2 20.5v-7.2c0-1.6 1.7-2.9 3.8-3.6 2.1.7 3.8 2 3.8 3.6v7.2"/>'
        '<circle cx="12" cy="6.8" r="0.9" fill="currentColor" stroke="none"/><path d="M3.5 20.5h17"/></svg>',

        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M12 4.2c2.1 2.8 3 5.7 2.2 8.8-.7 1.7-2.2 2.8-2.2 2.8s-1.5-1.1-2.2-2.8C9 9.9 9.9 7 12 4.2z"/>'
        '<path d="M14.4 8.2c2.5.4 4.6 2.1 5.1 4.6-.9 2-3.2 3.1-5.9 3.1"/>'
        '<path d="M9.6 8.2c-2.5.4-4.6 2.1-5.1 4.6.9 2 3.2 3.1 5.9 3.1"/>'
        '<path d="M6.5 18.8c3.4-1 7.6-1 11 0"/><circle cx="12" cy="10.2" r="1" fill="currentColor" stroke="none"/></svg>',
    )

    tabs_html = ""
    for idx, v in enumerate(venues):
        active_cls = " is-active" if idx == 0 else ""
        tabs_html += (f'<button class="hw-tab{active_cls}" role="tab" data-index="{idx}" aria-selected="{"true" if idx==0 else "false"}" '
                      f'data-venue-id="{v["id"]}" data-num="0{idx+1}" data-img="{P.R}media/wp-content/uploads/{v["img"]}" '
                      f'data-title="{v["name"]}" data-tag="{v["tag"]}" data-setting="{v["setting"]}" data-desc="{v["desc"]}" '
                      f'data-hl1="{v["highlights"][0]}" data-hl2="{v["highlights"][1]}" data-hl3="{v["highlights"][2]}">'
                      f'<span class="hw-tab-name">{v["name"]}</span>'
                      f'<span class="hw-tab-cap">{v["tag"]}</span>'
                      f'<span class="hw-tab-progress"><i class="hw-progress-bar"></i></span>'
                      f'</button>')

    v0 = venues[0]
    return f"""<section class="home-wedding" id="weddings">
  <div class="hw-inner">
    <div class="hw-header" data-fade>
      <p class="hw-tag lbl">A ROYAL DESTINATION CELEBRATION</p>
      <h2 class="hw-title" data-split>Weddings at the Palace</h2>
      <div class="hw-ornament">{ORN}</div>
      <p class="hw-lead" data-split="text">Seven palatial venues framed by centuries of Rajputana grandeur and the whispering Aravalli hills.</p>
    </div>

    <div class="hw-nav-tabs" role="tablist" aria-label="Palace Wedding Venues" data-fade>
      {tabs_html}
    </div>

    <div class="hw-stage" id="hwStage" data-fade>
      <div class="hw-stage-media">
        <div class="hw-arch-frame">
          <img id="hwMainImg" class="hw-main-img" src="{P.R}media/wp-content/uploads/{v0['img']}" alt="{v0['name']}">
          <div class="hw-img-overlay"></div>
          <div class="hw-arch-crest">
            <img src="{P.R}assets/img/crest.png" alt="Crest">
          </div>
        </div>
        <button class="hw-arrow hw-arrow-prev" id="hwPrevBtn" aria-label="Previous Venue">
          <svg viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M6 1 1 6l5 5M1 6h15"/></svg>
        </button>
        <button class="hw-arrow hw-arrow-next" id="hwNextBtn" aria-label="Next Venue">
          <svg viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="1.3"><path d="m10 1 5 5-5 5M15 6H0"/></svg>
        </button>
      </div>

      <div class="hw-stage-info">
        <div class="hw-venue-meta">
          <span class="hw-venue-setting" id="hwBadgeSetting">{v0['setting']}</span>
          <span class="hw-venue-sep">&middot;</span>
          <span class="hw-venue-cap" id="hwBadgeTag">{v0['tag']}</span>
        </div>
        <h3 class="hw-stage-title" id="hwCardTitle">{v0['name']}</h3>
        <p class="hw-stage-desc" id="hwCardDesc">{v0['desc']}</p>
        
        <div class="hw-features" id="hwFeatures">
          <div class="hw-feat-item"><span class="hw-royal-ico">{royal_icos[0]}</span> <span id="hwHl1">{v0['highlights'][0]}</span></div>
          <div class="hw-feat-item"><span class="hw-royal-ico">{royal_icos[1]}</span> <span id="hwHl2">{v0['highlights'][1]}</span></div>
          <div class="hw-feat-item"><span class="hw-royal-ico">{royal_icos[2]}</span> <span id="hwHl3">{v0['highlights'][2]}</span></div>
        </div>

        <div class="hw-actions">
          <a class="btn btn-gold btn-shimmer" href="{u('best-destination-wedding-venues-in-jaipur')}#enquire">Plan Your Royal Wedding</a>
          <a class="btn btn-line" href="{u('best-destination-wedding-venues-in-jaipur')}">Explore All 7 Venues</a>
        </div>
      </div>
    </div>

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

KOS_MINAR_SVG = (
    '<svg class="ms-kos-ico" viewBox="0 0 36 52" fill="none" aria-hidden="true">'
    '<path d="M18 3c-4.5 2.5-7 6.2-7 10.2h14C25 9.2 22.5 5.5 18 3z" fill="rgba(184,142,61,0.22)" stroke="#8D1711" stroke-width="1.2"/>'
    '<line x1="18" y1="0.5" x2="18" y2="3.5" stroke="#8D1711" stroke-width="1.2"/>'
    '<path d="M9 13.2h18M11.5 13.2L9.5 44h17l-2-30.8" stroke="#7A4B1E" stroke-width="1.25" fill="rgba(215,180,106,0.16)"/>'
    '<path d="M14.5 24c0-2.2 1.6-3.8 3.5-4.6 1.9.8 3.5 2.4 3.5 4.6v7h-7v-7z" stroke="#8D1711" stroke-width="1.1"/>'
    '<path d="M6 44h24M4 47.5h28" stroke="#7A4B1E" stroke-width="1.3" stroke-linecap="round"/>'
    '</svg>'
)

SURYA_SEAL_SVG = (
    '<svg class="ms-surya-svg" viewBox="0 0 120 120" fill="none" aria-hidden="true">'
    '<circle cx="60" cy="60" r="54" stroke="#8D1711" stroke-width="1.2" stroke-dasharray="3 3"/>'
    '<circle cx="60" cy="60" r="47" stroke="#9C7832" stroke-width="1.4"/>'
    '<path d="M60 6l4 11 9-8-2 11 11-4-6 10 12 1-9 7 10 6-11 3 7 9-11-1 3 11-10-5-2 11-7-9-6 10-3-11-9 7 1-12-10 4 5-10-11 0 9-7-10-6 11-3-7-9 11 1-3-11 10 5 2-11 7 9 6-10 3 11 9-7-1 12 10-4-5 10 11 0-9 7z" fill="rgba(215,180,106,0.22)" stroke="#9C7832" stroke-width="0.9"/>'
    '<circle cx="60" cy="60" r="21" fill="#F3E9D4" stroke="#8D1711" stroke-width="1.4"/>'
    '<circle cx="53.5" cy="56" r="1.6" fill="#8D1711"/><circle cx="66.5" cy="56" r="1.6" fill="#8D1711"/>'
    '<path d="M49 53c2.5-2.2 6-2.2 8.5 0M62.5 53c2.5-2.2 6-2.2 8.5 0" stroke="#7A4B1E" stroke-width="1.2" stroke-linecap="round"/>'
    '<path d="M60 55v7.5M54 66c3.5 2.4 8.5 2.4 12 0" stroke="#8D1711" stroke-width="1.3" stroke-linecap="round"/>'
    '</svg>'
)

SCROLL_TRAIL_SVG = (
    '<svg class="ms-trail-svg" viewBox="0 0 600 150" fill="none" preserveAspectRatio="none" aria-hidden="true">'
    '<path d="{d}" stroke="rgba(141,23,17,0.24)" stroke-width="1.4" stroke-dasharray="5 7"/>'
    '<path class="ms-trail-draw" d="{d}" stroke="#8D1711" stroke-width="1.8" stroke-linecap="round"/>'
    '</svg>'
)

def ms_trail(verse, note, flip=False):
    d = "M 430 4 C 430 72, 170 78, 170 146" if flip else "M 170 4 C 170 72, 430 78, 430 146"
    return f"""<div class="ms-trail">
  {SCROLL_TRAIL_SVG.format(d=d)}
  <div class="ms-trail-verse">
    <span class="ms-trail-note">{note}</span>
    <p class="ms-verse-words" data-ms-words>{verse}</p>
  </div>
</div>"""

def royal_stroll_section():
    kos_milestones = [
        ("30 km", "10 Royal Kos South", "Jaipur Airport · Sanganer", "Southern aerial & highway gateway to the princely state of Jaipur"),
        ("22 km", "7.5 Kos South", "Birla Marble Mandir", "Gleaming white marble shrine beneath Moti Dungri hill"),
        ("19 km", "6.5 Kos South", "Hawa Mahal & Pink City", "Five-storey terracotta Crown of Winds & vibrant Johari bazaars"),
        ("19 km", "6.5 Kos South", "City Palace & Chandra Mahal", "Royal court of the Kachhwaha Maharajas & Jantar Mantar"),
        ("16 km", "5.5 Kos South", "Gaitore Royal Cenotaphs", "Hand-carved marble chhatris of Jaipur's kings in a quiet valley"),
        ("15 km", "5 Kos · Aravalli Crest", "Nahargarh & Jaigarh Forts", "Twin mountain citadels standing watch along the folded ridge"),
        ("15 km", "5 Kos South", "Jal Mahal · Man Sagar Lake", "The floating sandstone pleasure palace mirrored in turquoise waters"),
        ("12 km", "4 Kos South", "Historic Amber Fort (Amer)", "Ancestral stronghold of Sheesh Mahal, Ganesh Pol & Maota Lake"),
        ("0 km", "Sanctuary Reached", "The Vijayran Palace · Kukas", "Cradled in the emerald Aravalli amphitheatre off the royal Amer pass"),
    ]

    kos_html = "".join(
        f'<div class="ms-kos-item{" is-sanctuary" if km == "0 km" else ""}" data-ms-kos>'
        f'{KOS_MINAR_SVG}'
        f'<div class="ms-kos-body">'
        f'<div class="ms-kos-dist"><b>{km}</b><span>{kos}</span></div>'
        f'<h4>{place}</h4>'
        f'<p>{desc}</p>'
        f'</div></div>'
        for km, kos, place, desc in kos_milestones
    )

    chapters = [
        {
            "khand": "Khand II &middot; The Northern Threshold of Kukas",
            "title": "Gajdwar &mdash; The Portal of Elephants &amp; Suryavanshi Forecourt",
            "rubric": "Where nagada kettle-drums thunder and the lotus channel reflects twin domes",
            "painting": f"{P.R}assets/img/scroll/02-gajdwar-arrival.webp",
            "paint_alt": "Hand-painted Jaipur miniature of Gajdwar elephant portal, nagada drummers and lotus water channel at The Vijayran Palace",
            "p1": (
                "Twelve kilometres north of Amber Fort, where the ancient Aravalli hills curve into a hushed green amphitheatre at Kukas, the Maharaja's road arrives beneath Gajdwar—the monumental yellow-sandstone Portal of Elephants. "
                "Up in the arched naqqarkhana gallery above the gate, musicians strike deep nagada kettle-drums and blow silver-rimmed trumpets while crimson rose petals rain down upon arriving carriages and caparisoned elephants."
            ),
            "p2": (
                "Passing under the soaring cusped mehrab arch unveils the full Suryavanshi symmetry of The Vijayran Palace: twin octagonal corner towers crowned with ribbed chhatri cupolas, deep stone chhajja eaves engineered to tame the Rajasthan noon, and a tranquil Mughal water parterre blooming with pink lotuses between rows of slender cypress."
            ),
            "callouts": [
                ("Architecture", "Khatu &amp; Dholpur yellow sandstone dressed by hereditary Rajasthani silavats"),
                ("Ceremony", "Traditional tilak, aarti, nagada drum &amp; rose-petal royal welcome"),
                ("Sanctuary Scale", "35 palatial haveli suites &amp; private-pool villas set across quiet gardens"),
            ],
            "peep_img": "2021/06/Main-Gate.jpg",
            "peep_cap": "The living sandstone Gajdwar gate at Kukas today",
            "trail_after": (
                "Step off the sunlit forecourt terrace and turn beneath a cool scalloped arch—where bright desert gold softens into lime-plastered shade and the gentle murmur of marble water.",
                "Thirty Paces Inward · Entering the Aangans",
            ),
            "reverse": False,
        },
        {
            "khand": "Khand III &middot; The Inner Haveli Aangans",
            "title": "Char Bagh Lotus Fountain, Haveli Chowk &amp; Stone-Lace Jharokhas",
            "rubric": "Peacocks along the chhajja eaves and mountain breezes spun through carved jaali",
            "painting": f"{P.R}assets/img/scroll/03-charbagh-haveli.webp",
            "paint_alt": "Hand-painted Jaipur miniature of saffron sandstone Haveli Chowk, Char Bagh marble lotus fountain, jharokhas and peacocks",
            "p1": (
                "Inside the palace walls, cool stone-flagged corridors open into sky-lit courtyards modeled on the royal havelis of Rajputana: Haveli Chowk and the four-quartered Char Bagh garden. "
                "At the crossing of four marble water rills, a hand-carved white lotus fountain murmurs day and night amid white frangipani blossoms, hosting intimate Mehendi and Haldi gatherings of 100 to 250 guests."
            ),
            "p2": (
                "Raise your eyes to the upper storeys where peacocks rest along the warm sandstone parapets. Cantilevered jharokha balconies and pierced geometric jaali lattices overhang the square—filtering bright sun into lacework while cooling the expansive 1,345 sq ft Courtyard Haveli Suites, 800 sq ft Balcony Suites, 600 sq ft Jharokha Suites and 450 sq ft Haveli Rooms."
            ),
            "callouts": [
                ("Char Bagh &amp; Chowk", "Four-quartered Mughal fountain garden for 100–250 royal guests"),
                ("Pierced Stone Craft", "Hand-carved jharokha balconies &amp; geometric jaali wind-screens"),
                ("Haveli Residences", "Courtyard, Balcony &amp; Jharokha suites opening onto private aangans"),
            ],
            "peep_img": "2021/06/g4.jpg",
            "peep_cap": "Saffron sandstone arcades &amp; jharokhas framing the inner chowk",
            "trail_after": (
                "Follow the warm fragrance of roasted cloves, saffron and woodsmoke through brass-studded teakwood doors into the painted durbar chambers—and onward to the lantern-lit garden stage.",
                "Through the Vaulted Durbar to the Eastern Arcade",
            ),
            "reverse": True,
        },
        {
            "khand": "Khand IV &middot; Royal Dastarkhwan &amp; Living Arts",
            "title": "Swarn Mahal Feasts, Raj Mahal Durbar &amp; Rang Mahal Nights",
            "rubric": "Heirloom recipes by candlelight and whirling Kalbeliya skirts to the bowed Ravanahatha",
            "painting": f"{P.R}assets/img/scroll/04-durbar-rangmahal.webp",
            "paint_alt": "Hand-painted Jaipur miniature showing floral-frescoed Swarn and Raj Mahal banquet hall flowing into Rang Mahal folk dance courtyard",
            "p1": (
                "At the ceremonial heart of the scroll lie Raj Mahal—our grand tapestry banquet hall welcoming 250 to 300 guests beneath crystal chandeliers and hand-painted floral vaults—and Swarn Mahal, the palace dining salon. "
                "Here our Executive Chef revives guarded recipes of Mewar, Marwar and Awadh alongside global classics, harvesting crisp herbs and seasonal vegetables each dawn from the palace's own organic kitchen gardens."
            ),
            "p2": (
                "Stepping eastward through cusped sandstone colonnades brings you to Rang Mahal, an open-air heritage amphitheatre for 400 to 500 guests. By day, hushed suites along this wing house the Rang Mahal Spa for restorative sixty-minute Ayurvedic therapies; at dusk, rows of brass diyas awaken as folk musicians play the ancient Ravanahatha and Ghoomar and Kalbeliya dancers spin beneath the moon."
            ),
            "callouts": [
                ("Swarn &amp; Raj Mahal", "Painted durbar banquet (250–300 guests) &amp; organic garden gastronomy"),
                ("Rang Mahal Stage", "Open-air sandstone heritage amphitheatre for 400–500 guests"),
                ("Spa &amp; Folk Arts", "60-minute Ayurvedic wellness by day; Ravanahatha &amp; Ghoomar by starlight"),
            ],
            "peep_img": "2021/06/g2.jpg",
            "peep_cap": "Tapestry arches &amp; chandeliers inside Raj Mahal",
            "trail_after": (
                "One final winding path leads past bougainvillea-draped garden walls to secluded plunge-pool estates, turquoise sky-waters, spirited Marwari stables and the grand lamp-lit palace lawn.",
                "Outward to the Valley Rim &amp; Starlit Horizon",
            ),
            "reverse": False,
        },
        {
            "khand": "Khand V &middot; Waters of the Sky &amp; Starlit Finale",
            "title": "Presidential Pool Enclaves, Ambar Taal, Marwari Trails &amp; Mahal Bagh",
            "rubric": "Turquoise baradari reflections at dusk and a hundred golden lamps across the Aravallis",
            "painting": f"{P.R}assets/img/scroll/05-ambartaal-mahalbagh.webp",
            "paint_alt": "Hand-painted Jaipur miniature of Ambar Taal marble baradari pool, private pool villas, Marwari horses in Aravalli hills and illuminated palace lawn",
            "p1": (
                "Along the quiet western sanctuary stand five walled Presidential Villas—private royal estates each enclosing its own manicured garden and shimmering plunge pool—beneath elevated Terrace Haveli Suites gazing straight across India's oldest mountain range. "
                "Just below, white marble baradari arches frame the turquoise stillness of Ambar Taal, where morning swims give way to artisanal high tea and rose-strewn candlelit dinners beside the water."
            ),
            "p2": (
                "Where the gardens meet the foothills, noble sickle-eared Marwari horses, camels and safari jeeps set out along khejri-shaded trails alive with over 150 species of native birds. "
                "Finally, step onto the vast emerald carpet of Vijayran Mahal Bagh—capable of hosting 1,500 wedding guests under open skies—and look back as a hundred golden lamps set every dome, arch and jharokha of The Vijayran Palace aglow against the indigo Rajasthan night."
            ),
            "callouts": [
                ("Private Pool Enclaves", "5 walled Presidential Villas with private plunge pools &amp; sunset terraces"),
                ("Ambar Taal &amp; Trails", "Infinity sky-pool, Marwari horse safaris, cycling &amp; 150+ bird species"),
                ("Vijayran Mahal Bagh", "Grand emerald palace front lawn welcoming 1,000–1,500 royal guests"),
            ],
            "peep_img": "2021/06/ambertallpool-img.jpg",
            "peep_cap": "Ambar Taal mirroring the Aravalli hills at Kukas",
            "trail_after": None,
            "reverse": True,
        },
    ]

    chapters_html = ""
    for ch in chapters:
        rev_cls = " is-reverse" if ch["reverse"] else ""
        calls_html = "".join(
            f'<div class="ms-callout"><b>{k}</b><span>{v}</span></div>'
            for k, v in ch["callouts"]
        )
        chapters_html += f"""
      <section class="ms-chapter{rev_cls}" data-ms-chapter>
        <header class="ms-ch-head">
          <p class="ms-khand">{ch["khand"]}</p>
          <h2 class="ms-ch-title">{ch["title"]}</h2>
          <p class="ms-ch-rubric">{ch["rubric"]}</p>
        </header>

        <figure class="ms-fresco" data-ms-fresco>
          <img class="ms-fresco-img" src="{ch["painting"]}" alt="{e(ch["paint_alt"])}" loading="lazy" decoding="async">
        </figure>

        <div class="ms-story-grid">
          <div class="ms-story-prose">
            <p class="ms-dropcap">{ch["p1"]}</p>
            <p>{ch["p2"]}</p>
            <div class="ms-callouts">{calls_html}</div>
          </div>
          <aside class="ms-peep-card" data-ms-peep>
            <div class="ms-peep-arch">
              {img(ch["peep_img"], ch["peep_cap"], cls="ms-peep-img")}
            </div>
            <p class="ms-peep-cap">{ch["peep_cap"]}</p>
          </aside>
        </div>
      </section>"""

        if ch["trail_after"]:
            t_v, t_n = ch["trail_after"]
            chapters_html += ms_trail(t_v, t_n, flip=not ch["reverse"])

    return f"""<div class="ms-stage">
  <div class="maharaja-scroll" id="maharaja-scroll">
    <div class="ms-roller ms-roller-top" aria-hidden="true">
      <span class="ms-finial ms-finial-l"></span>
      <span class="ms-rod"></span>
      <span class="ms-finial ms-finial-r"></span>
    </div>

    <div class="ms-parchment">
      <div class="ms-hashiya ms-hashiya-l" aria-hidden="true"></div>
      <div class="ms-hashiya ms-hashiya-r" aria-hidden="true"></div>

      <div class="ms-inner">
        <!-- ROYAL FARMAN INVOCATION & UNROLLING HEADER -->
        <header class="ms-header">
          <div class="ms-seal-top">{SURYA_SEAL_SVG}</div>
          <p class="ms-invocation">Shahi Chitramala &middot; Royal Painted Scroll of Jaipur &amp; Kukas</p>
          <h1 class="ms-main-title">The Maharaja’s Stroll <span class="soft">from the Pink City to</span> Vijayran</h1>
          <div class="ms-orn-crimson">{ORN}</div>
          <p class="ms-preamble">
            In the royal courts of Rajasthan, when a Maharaja rode north from his capital to inspect his mountain pleasure-palace, court painters (<em>chiteras</em>) recorded every league, fort, lake, gateway and courtyard in mineral pigments and gold leaf upon handmade <em>wasli</em> parchment. Unroll this painted chronicle to follow the ancient royal route out of Jaipur—past every sentinel fort and water palace—and walk chamber by chamber through the complete living story of <strong>The Vijayran Palace</strong> at Kukas.
          </p>
        </header>

        <!-- KHAND I: HAND-PAINTED CAVALCADE FROM PINK CITY TO AMER & KOS MINAR DISTANCES -->
        <section class="ms-chapter ms-route-chapter" data-ms-chapter>
          <header class="ms-ch-head">
            <p class="ms-khand">Khand I &middot; The Royal Cavalcade Northward from Jaipur</p>
            <h2 class="ms-ch-title">From Hawa Mahal &amp; Jal Mahal <span class="soft">past</span> Amber Fort to Kukas</h2>
            <p class="ms-ch-rubric">Every fort, temple and royal cenotaph measured in leagues along the Aravalli pass</p>
          </header>

          <figure class="ms-fresco ms-fresco-hero" data-ms-fresco>
            <img class="ms-fresco-img" src="{P.R}assets/img/scroll/01-pinkcity-amer.webp" alt="Hand-painted Jaipur miniature scroll of the Maharaja's elephant and Marwari horse procession from Hawa Mahal past Jal Mahal to Amber Fort" decoding="async">
          </figure>

          <div class="ms-cartography-row">
            <div class="ms-map-vignette" data-ms-peep>
              <img src="{P.R}assets/img/map-jaipur-watercolor.webp" alt="Hand-painted watercolour heritage map of Jaipur, Jal Mahal, Amber Fort and The Vijayran Palace at Kukas" loading="lazy" decoding="async">
            </div>
            <div class="ms-route-story">
              <p class="ms-dropcap">
                Setting forth at dawn beneath the rose-terracotta honeycomb of <em>Hawa Mahal</em> and the courtyards of <em>City Palace</em>, the royal procession winds northward between folded ochre hills. At <em>Gaitore</em>, carved marble cenotaphs honour the Kachhwaha kings; ahead, <em>Jal Mahal</em> floats motionless upon the turquoise waters of Man Sagar Lake while <em>Nahargarh</em> and <em>Jaigarh</em> guard the high mountain rim.
              </p>
              <p>
                Climbing past the mighty ramparts and mirrored halls of <em>Amber Fort</em>—just twelve kilometres south of our gates—the highway gives way to quiet khejri groves and emerald crags until the sandstone domes of <strong>The Vijayran Palace, Kukas</strong> appear in serene mountain solitude.
              </p>
            </div>
          </div>

          <div class="ms-kos-band">
            <p class="ms-kos-heading"><span>Kos Minar &middot; Hand-Painted Royal Milestones to The Vijayran Palace</span></p>
            <div class="ms-kos-grid">
              {kos_html}
            </div>
          </div>
        </section>

        {ms_trail("Leaving the ramparts of Amer twelve kilometres behind, the royal standards turn into the quiet valley of Kukas—where kettle-drums awaken above a towering yellow-sandstone gate.", "4 Royal Kos North of Amber Fort · Arriving at Kukas", flip=False)}

        <!-- KHAND II TO V: COMPLETE HAND-PAINTED PALACE TOUR -->
        {chapters_html}

        <!-- SHAHI MOHAR COLOPHON -->
        <footer class="ms-colophon" data-fade>
          <div class="ms-mohar">
            <img src="{P.R}assets/img/crest.png" alt="Royal Quest Resorts Crest" width="84" height="86">
            <span>Shahi Mohar &middot; Kukas, Samvat Chronicle</span>
          </div>
          <p class="ms-colophon-script" aria-hidden="true">Padharo Mhare Des</p>
          <h2 class="ms-colophon-title">Step Into the <span class="soft">Living Scroll.</span></h2>
          <p class="ms-colophon-text">
            Thus concludes the painted stroll from the Pink City to Kukas. Thirty-five sunlit haveli suites and private-pool villas, seven palatial celebration venues and the timeless hospitality of Rajasthan await your arrival.
          </p>
          <div class="ms-colophon-acts">
            {btn("Reserve Your Royal Stay", BOOK, "gold")}
            {btn("Explore 35 Suites & Villas", u("accommodation"), "dark")}
            {btn("Plan a Palace Wedding", u("best-destination-wedding-venues-in-jaipur"), "line")}
          </div>
        </footer>
      </div>
    </div>

    <div class="ms-roller ms-roller-bot" aria-hidden="true">
      <span class="ms-finial ms-finial-l"></span>
      <span class="ms-rod"></span>
      <span class="ms-finial ms-finial-r"></span>
    </div>
  </div>
</div>"""

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
              "<p>To stay at The Vijayran Palace is to live like royalty in the lap of the ancient Aravalli hills: soaring yellow-sandstone chhatris, hand-carved jharokha balconies and tranquil Mughal courtyards, infused with the warmth of true Rajasthani hospitality.</p>"
              "<p>Cradled across lush, manicured lawns in Kukas—just twelve kilometres north of historic Amber Fort yet worlds removed from urban haste—our thirty-five private-pool villas and haveli suites pair regal Rajputana tapestries and period craftsmanship with effortless contemporary comfort.</p>"
              "<p>Begin your mornings with guided yoga to birdsong, ride spirited Marwari horses along mountain trails, savour heirloom recipes harvested from our organic kitchen gardens, and gather beneath desert stars for folk music and candlelit feasts.</p>")
      + cert("2023/05/banner-01-1.jpg", "Tripadvisor · 4.5 of 5", f"“{REVIEWS[1][0]}”")
      + collection("Our Stays", "Thirty-five villas, suites and rooms set around courtyards, terraces and gardens. Each offers a different way of living like royalty, from a private-pool villa to a suite framed by a hand-carved jharoka.",
                   btn("Discover our stays", u("accommodation")), room_items(ROOMS))
      + story('A heritage palace <span class="soft">woven into</span> the Aravalli hills',
              "Royal Quest Resorts created The Vijayran Palace around a simple idea: luxury, world-class service and an atmosphere of solitude. It is where old-world vibes and a glorious past meet the new age, an amalgamation of culture, tradition and contemporary comfort.",
              btn("Discover our story", u("about-us-luxury-resort-of-jaipur"), "dark") + btn("Royal Palace Stroll", u("royal-heritage-stroll"), "line"), STORY_IMGS)
      + day_clock_section()
      + wedding_home()
      + itinerary('Discover the <span class="soft">royal heritage</span> of Jaipur from our doorstep.',
                  "Amber Fort is about 12 km away and the walled Pink City around 19 km. Hawa Mahal, City Palace, Jal Mahal and the cenotaphs of Gaitore are all within easy reach, with fairytale palaces, colourful temples and splendid havelis to explore before returning to the calm of the palace.",
                  btn("Explore", u("top-holiday-resort-in-jaipur-for-family"), "line"))
      + guest_voices())
    page("index.html", "The Vijayran Palace | 5 Star Luxury Heritage Resort in Jaipur",
         "The Vijayran Palace by Royal Quest Resorts: a royal heritage resort in Jaipur, Rajasthan, with private pool villas, haveli suites and destination weddings.", body, schema=HOTEL_LD)

    # OUR STAYS — stacking full-screen cards (Sujan "Tents & tented suites")
    P.R = "../"
    st_items = [{"img": r["hero"], "name": r["name"], "tag": r["count"], "text": r["body"][0], "facts": r["facts"][:6],
                 "acts": [("Discover", u(r["slug"]), "line"), ("Book", BOOK, "gold")]} for r in ROOMS]
    body = (hero("2021/05/img01.jpg", "Our Stays", "Villas, haveli suites & rooms")
      + intro("Thirty-five ways to live like royalty, each with its own courtyard, terrace, jharoka or private pool.",
              "<p>From the Presidential Villas with their secluded plunge pools and walled gardens to haveli suites framed by hand-carved sandstone jharokas, every residence pairs fine Rajasthani tapestry and period artistry with generous sunlit proportions.</p>"
              "<p>Thoughtfully arranged across quiet courtyards and mountain-facing terraces, each stay includes round-the-clock palace service and unhurried access to Ambar Taal, Swarn Mahal dining and curated Aravalli experiences.</p>", tpl=True, kicker="ROYAL ACCOMMODATION &middot; 35 SUITES &amp; VILLAS")
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
              "<p>Have you ever wondered what an escape from your demanding life would feel like, in the lap of nature, with luxurious service and a peaceful environment? At Vijayran, the dream of a relaxed holiday where you are king comes true.</p>"
              "<p>Set amidst emerald Aravalli peaks and quiet stone-paved courtyards at Kukas, our heritage estate brings together centuries-old Rajputana architecture, organic garden gastronomy and heartfelt, unhurried hospitality.</p>")
      + cert("2021/06/g8.jpg", "Royal Quest Resorts", "“Rich heritage, natural beauty and a refreshing ambience, combined with remarkable service.”")
      + story('Old-world vibes <span class="soft">meet</span> the new age',
              "Royal Quest Resorts developed The Vijayran Palace around a unique idea: an experience laden with luxury, world-class service and an atmosphere of solitude. Away from the worldly chaos, lose yourself in a fortress of solitude and magnificence. We await all our guests with open arms and excellent hospitality, because you deserve it.",
              btn("Explore our stays", u("accommodation"), "dark") + btn("Take the Palace Stroll", u("royal-heritage-stroll"), "line"), ["2021/06/g2.jpg","2021/06/g4.jpg","2021/06/g11.jpg","2021/06/g5.jpg","2021/05/view.jpg"])
      + feature("2021/05/wedding01.jpg", "For every traveller", "Suites for every kind of stay",
                "Vijayran strikes a delicate balance between culture, tradition and modern luxury. Our luxury suites, honeymoon suites, junior suites and double rooms suit every budget, from those seeking the ultimate indulgence to those travelling light.",
                ("Plan a wedding", u("best-destination-wedding-venues-in-jaipur")))
      + quote(2))
    page("about-us-luxury-resort-of-jaipur/index.html", "About The Vijayran Palace | Luxury Heritage Resort in Jaipur",
         "One of Jaipur's most luxurious heritage resorts, with palace architecture, luxury accommodation, huge lawns, banquet venues and restaurants.", body)

    # ROYAL HERITAGE STROLL (/royal-heritage-stroll/)
    P.R = "../"
    stroll_body = (royal_stroll_section()
      + collection("Step Inside Our Residences", "Thirty-five private-pool villas, terrace suites and haveli rooms await along the palace courtyards you have just walked.",
                   btn("Explore all stays", u("accommodation")), room_items(ROOMS), kicker="CONTINUE YOUR JOURNEY &middot; 35 SUITES &amp; VILLAS"))
    page("royal-heritage-stroll/index.html", "The Royal Heritage Stroll | Complete Palace Tour | The Vijayran Palace Jaipur",
         "Walk step by step through The Vijayran Palace in Kukas, Jaipur—an immersive first-person Rajasthani stroll from Gajdwar portal through Char Bagh, Swarn Mahal, Presidential Villas and Ambar Taal.", stroll_body, light=True)

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
              "<p>Medieval interiors for a palatial royal wedding, and sprawling manicured gardens for starlit outdoor ceremonies. Whether it is a contemporary celebration, a traditional Hindu wedding, a Christian ceremony or a nikah, you can trust The Vijayran Palace to weave its magic.</p>"
              "<p>Across seven distinct indoor and outdoor venues accommodating from 100 to 1,500 guests, our creative planners, master chefs and palace concierges choreograph every ritual from the welcoming baraat to the final farewell.</p>", kicker="ROYAL CELEBRATIONS &middot; SEVEN PALATIAL VENUES")
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
              "<p>A village safari, a majestic elephant ride, a trail on spirited Marwari horses, an open jeep expedition, or simply gazing at the magnificent night sky. Set in a culturally vibrant region, the palace introduces its guests to an India rich in customs, traditions and living artistry.</p>"
              "<p>Every day unfolds at the pace you choose—from dawn pranayama on dewy lawns and birdwatching across over 150 native species to evening Ravanahatha and Kalbeliya performances around flickering lanterns.</p>", kicker="CURATED EXPERIENCES &middot; CULTURE &amp; WILDERNESS")
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
              "<p>Our Executive Chef and his brigade combine authentic royal cuisines of Rajasthan and India with global culinary classics—crafted daily with fresh spices, herbs and seasonal produce harvested straight from our organic kitchen gardens.</p>"
              "<p>Savour slow-cooked Awadhi and Mewari delicacies inside tapestry-draped Swarn Mahal, share a poolside feast beside Ambar Taal, or reserve a private candlelit table strewn with roses beneath the Aravalli stars.</p>", kicker="CULINARY HERITAGE &middot; SWARN MAHAL &amp; AL FRESCO")
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
              "<p>Time stands still in our quiet Aravalli valley. Take in unbroken views of India's oldest mountain range, then set out at leisure for fairytale forts, colourful bazaars, sacred marble temples and storied royal cenotaphs.</p>"
              "<p>Positioned just twelve kilometres north of Amber Fort and nineteen kilometres from the walled Pink City, our concierge gladly arranges private chauffeurs, historians and bespoke heritage itineraries.</p>", kicker="THE PRINCELY REALM &middot; AMER &amp; THE PINK CITY")
      + itinerary('Explore the <span class="soft">Pink City</span> and its forts.', "The palace is about 12 km from Amber Fort and around 19 km from Hawa Mahal in the walled city. Our team will happily arrange cars and guides.", btn("Contact us", u("get-in-touch-resort-in-kukas-jaipur"), "line"))
      + experiences("Nearby", "Five landmarks within easy reach of The Vijayran Palace.", [{"img": p, "title": t, "text": d} for t, p, d in ATTRACTIONS])
      + cert("2021/05/AmberFort.jpg", "Amber Fort", "“The fort still stands as a perfect picture of ancient Indian architecture.”")
      + info("Getting here", "Directions, timings and travel tips for exploring Jaipur from the palace.", INFO))
    page("top-holiday-resort-in-jaipur-for-family/index.html", "Attractions near The Vijayran Palace | Holiday Resort in Jaipur for Families",
         "Amber Fort, Hawa Mahal, City Palace, Birla Mandir and Gaitore: discover Jaipur's attractions from The Vijayran Palace.", body)

    # DAY OUTING & STAY PACKAGES
    pk = [("Summer Splash","Day Outing · 2:00 PM – 9:00 PM","Ambar Taal swimming pool access, artisanal evening high tea and a curated set-menu dinner at Swarn Mahal, paired with horse riding and light poolside music.","₹2,500 + taxes per person","Add a day-use heritage room for ₹5,000 + taxes."),
          ("Family Fiesta","Royal Stay Package","Daily breakfast and one additional meal at Swarn Mahal, a complimentary 60-minute Rang Mahal spa treatment for mothers, daily supervised Kids' Hour with games and goodies, and an Elephant Safari in the Aravalli hills with transfers.","Special Courtesies · On Request",f"Call {PHONE_PACKAGES} or email {EMAIL_SALES}."),
          ("Horse Safari in Jaipur","Couples & Family Stay Package","Daily breakfast and one additional meal at Swarn Mahal, a complimentary 60-minute Rang Mahal spa treatment for each partner, daily supervised Marwari horse riding, and Kids' Hour with games and goodies.","Special Courtesies · On Request",f"Call {PHONE_PACKAGES} or email {EMAIL_SALES}."),
          ("Elephant Safari in Jaipur","Heritage Stay Package","Daily breakfast and one additional meal at Swarn Mahal, complimentary round-trip Jaipur International Airport transfers, and a guided Elephant Safari in the scenic Aravalli hills near Amer.","Special Courtesies · On Request",f"Call {PHONE_PACKAGES} or email {EMAIL_SALES}.")]
    pks = "".join(f'<article data-fade><p class="lbl">{k}</p><h3>{t}</h3><p class="p">{d}</p><p class="price">{pr}</p><p class="p-s">{n}</p></article>' for t, k, d, pr, n in pk)
    body = (hero("2021/04/LUCK7602.jpg", "Day Outing", "Just outside Jaipur")
      + intro('Spend a day <span class="soft">like royalty.</span>',
              "<p>Turquoise waters at Ambar Taal, emerald Aravalli vistas, artisanal high tea and starlit dining—all an effortless scenic drive from Jaipur. Thoughtfully curated for families, couples and gatherings of friends.</p>"
              "<p>Enjoy full access to our palace gardens, poolside leisure, equestrian rides and Swarn Mahal hospitality, with optional day rooms and private safaris tailored to your group.</p>", kicker="ROYAL DAY RETREATS &middot; JUST OUTSIDE JAIPUR")
      + f'<section class="pk">{pks}</section><div style="display:flex;gap:1rem;justify-content:center;padding:0 var(--g) 6rem;flex-wrap:wrap">{btn("Book Online", BOOK, "gold")}{btn("Call " + PHONE_PACKAGES, "tel:" + TEL_PACKAGES, "dark")}{btn("Email Packages Desk", "mailto:" + EMAIL_SALES, "line")}</div>'
      + feature("2021/06/riding.jpg", "Add-ons", "Horse riding, games and the Ambar Taal pool", "Round off your day with a horse ride, games on the lawns or a swim, then dinner with a view of the Aravallis.", rev=True)
      + info("Good to know", "Everything you need before you visit.", INFO))
    page("resort-near-jaipur-for-day-outing/index.html", "Day Outing Resort near Jaipur | Packages | The Vijayran Palace",
         "Day outing packages near Jaipur at The Vijayran Palace: pool access, high tea and dinner, plus family, horse riding and elephant safari packages.", body)

    # SEASONAL & STAY PACKAGES (/winter-summer-package/)
    pkg_body = (hero("2021/06/horse-img.jpg", "Curated Palace Packages", "Seasonal stays & royal courtesies")
      + intro('Bespoke <span class="soft">holiday packages</span> with spa, safaris &amp; Swarn Mahal dining.',
              "<p>Whether planning a family escape, an equestrian retreat or a celebratory weekend in the Aravallis, our seasonal stay packages bundle our most-loved experiences with thoughtful palace courtesies.</p>"
              "<p>Enjoy daily dining at Swarn Mahal, complimentary sixty-minute Rang Mahal spa therapies, supervised children's hours, airport transfers and guided horse or elephant safaris.</p>", kicker="SPECIAL OFFERS &middot; WINTER &amp; SUMMER PACKAGES")
      + f'<section class="pk">{pks}</section><div style="display:flex;gap:1rem;justify-content:center;padding:0 var(--g) 6rem;flex-wrap:wrap">{btn("Check Rates & Book", BOOK, "gold")}{btn("Call " + PHONE_PACKAGES, "tel:" + TEL_PACKAGES, "dark")}{btn("Email " + EMAIL_SALES, "mailto:" + EMAIL_SALES, "line")}</div>'
      + experiences("Included Experiences", "Signature palace activities woven into our curated stay packages.", [{"img": p, "title": t, "text": d} for t, p, d in EXPERIENCES[:6]])
      + quote(4))
    page("winter-summer-package/index.html", "Resort Packages & Offers in Jaipur | Family, Spa & Safari Stays | The Vijayran Palace",
         "Explore winter, summer and weekend stay packages at The Vijayran Palace, Jaipur: Swarn Mahal dining, 60-minute spa treatments, horse riding and elephant safaris.", pkg_body)

    # GUEST TESTIMONIALS (/testimonial/)
    rev_contexts = [
        "Presidential Villa &amp; Private Pool",
        "Aravalli Heritage Suite",
        "Royal Destination Wedding",
        "Family Retreat &amp; Bespoke Dining",
        "Folk Evenings &amp; Hospitality",
        "Courtyard &amp; Jharoka Suites",
    ]
    rev_rows = "".join(
        f'<article class="gs-ledger-item" data-fade>'
        f'<div class="gs-orn">{ORN}</div>'
        f'<blockquote class="gs-quote">“{q}”</blockquote>'
        f'<div class="gs-attr">'
        f'<span class="gs-sig" aria-hidden="true">{n.split()[0]}</span>'
        f'<span class="gs-name">{n}</span>'
        f'<span class="gs-ctx">{rev_contexts[i % len(rev_contexts)]} &middot; Verified Tripadvisor Review</span>'
        f'</div></article>'
        for i, (q, n) in enumerate(REVIEWS)
    )
    rev_body = (ph("Guest Chronicles", 'Words from those who called <span class="soft">the palace</span> home.')
      + f'<section class="gs-ledger">{rev_rows}</section>'
      + cert("2023/05/banner-01-1.jpg", "Tripadvisor · 4.5 of 5 from 284 Reviews", f"“{REVIEWS[4][0]}”")
      + f'<div style="display:flex;gap:1rem;justify-content:center;padding:5rem var(--g) 6rem;flex-wrap:wrap">{btn("Book Your Stay", BOOK, "gold")}{btn("Plan a Celebration", u("best-destination-wedding-venues-in-jaipur"), "line")}</div>')
    page("testimonial/index.html", "Guest Reviews & Testimonials | The Vijayran Palace, Jaipur",
         "Read verified guest reviews and wedding testimonials for The Vijayran Palace by Royal Quest Resorts in Kukas, Jaipur.", rev_body, light=True)

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
