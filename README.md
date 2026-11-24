# The Vijayran Palace: website v2 (Sujan design system, full replica)

A static website for The Vijayran Palace that re-creates the design system of **thesujanlife.com**: fluid type scale, palette, spacing, section layouts, image placements, scroll animations and interactions. All content and photography are Vijayran's own. The design and motion were rebuilt from scratch. No Sujan code, text, images or logos are included.

## Run it
**Windows, one click:** double-click `Start-Vijayran-Website.bat`. It starts a local server (no installs needed) and opens http://localhost:8080 in your browser.

Other setups:
1. Unzip.
2. The photos the site uses are already in `media/`. The full original media library is in **RoyalQuestResorts_Website_Extract.zip** if you need more.
3. Run a local server for best results (smooth scroll and animations need it): `npx serve .` or `python3 -m http.server`, then open http://localhost:3000 (or :8000). Double-clicking `index.html` also works.

## Repository layout
```
/                     the deployable site: upload everything except _build/ to any web host
├── index.html, <page>/index.html   19 pages (old royalquestresorts.com URLs kept)
├── assets/           css, js, vendor (GSAP, Lenis), img (logo, crest, map), video (hero)
├── media/            68 client photos (same paths as the old WordPress uploads)
├── sitemap.xml, robots.txt
├── Start-Vijayran-Website.bat + serve.ps1   one-click local preview on Windows
└── _build/           generator: data.py (all text/content), build.py (templates), make_map.py (to-scale map)
```
To edit content, change `_build/data.py` (or the templates in `_build/build.py`), then run `python3 _build/build.py`. The pages at the repo root are regenerated in place; assets/ and media/ are untouched. Run `python3 _build/make_map.py` after changing map landmarks.

## Motion system (Sujan behaviour → this build)
| Sujan behaviour | Where | Implementation (assets/js/site.js) |
|---|---|---|
| Lenis smooth scrolling | all pages | Lenis 1.3, synced to the GSAP ticker |
| Line-by-line text reveal (lines rise from a mask, y 110%→0, power4.out, 1.8s / stagger .1 for titles, 2.4s / stagger .04 for paragraphs) | every `[data-split]` | GSAP SplitText `mask:"lines"` + ScrollTrigger |
| Intro card scales 0.8→1 and slides up over the hero (scrub 2); hero video zooms 1→1.5 | home | ScrollTrigger scrub |
| Full-bleed quote: gold line draws in, label rises, image parallax (scale 1→1.2, y 0→10%) | `.cert` | timeline + scrub |
| Draggable collection rail with inertia, cards rise 50%→0 as the section enters, progress bar, arrows | `.coll`, `.exp`, `.gal` | Draggable + InertiaPlugin |
| Sticky centred story text, photos drift past left and right with staggered parallax and zoom | `.story` | `position:sticky` + scrubbed timeline |
| Full-screen stacking cards with a floating info panel (Sujan "Tents & tented suites") | `.stack` (Our Stays, room pages, wedding venues) | sticky stacking + image zoom-in + panel rise |
| Red feature band with image parallax | `.feat` | scrub |
| Menu: clip-path wipe from the top, then links, labels and images reveal in sequence; burger morphs to ×; MENU rolls to CLOSE | `.menu` | GSAP timeline |
| Book Now: panel unfolds (scaleY), thumbnails slide in, text rises | `.book-panel` | GSAP timeline |
| Button text rolls on hover; links underline from left to right | `.btn`, `.ul` | CSS |
| Accordion opens with eased height | `.acc` | GSAP |
| Line illustrations draw themselves | jharokha sketch, map | stroke-dashoffset |

Everything respects `prefers-reduced-motion`, and the site still works if JavaScript fails.

## Design tokens
- **Type scale (1rem = 16px at 1440px, fluid):** hero 72px · intro 64.8px · section 57.6px · 43.2px · 36px · 32.4px (uppercase) · body 16px / 14.4px / 12.8px
- **Colours:** cream `#F6F3EF` · off-white `#FBF9F7` · gold `#D7B46A` · espresso `#322B26` · cocoa footer `#3E362F` · text `#5C544D` / `#79716A` · Rajasthani red `#8D1711` · quote background `#F9F9F9`
- **Fonts:** Sujan uses licensed fonts. This build uses free equivalents:
  - Minion Pro → **Crimson Pro**
  - Brandon Grotesque → **Jost**
  - Roboto Flex, Italianno and Inter are identical to Sujan's.
  - For a pixel-exact match, license Minion Pro and Brandon Grotesque (Adobe Fonts / HvD) and change `--f-display` and `--f-head` in site.css.

## Pages (all existing URLs are kept, so SEO carries over)
Home · /accommodation/ (new) · 6 room pages · weddings · activities · dining · attractions · day outing · gallery · about · contact · FAQ · careers · terms, plus sitemap.xml and robots.txt.

## Libraries (bundled in assets/vendor, so no CDN is needed)
GSAP 3.13 with ScrollTrigger, SplitText, Draggable and InertiaPlugin (free under GSAP's standard "no charge" licence), and Lenis 1.3.4 (MIT).

## Before launch
- **Forms:** connect them by setting `data-endpoint="…"` on each `<form>` (wedding enquiry, contact, careers, newsletter).
- **Booking:** confirm which engine is live; all Book buttons use STAAH (`BOOK` in data.py).
- **Photography:** Sujan's look depends on large, high-quality photography. Most current Vijayran room photos are 1000×600 px or smaller and will look soft in full-screen sections. A new shoot (or the original high-res files) is strongly recommended.
- **Hero video:** `assets/video/hero.mp4` (client footage, H.264 1080p, 10.5 MB) with `hero-poster.jpg`.
- **Logo:** replace the text wordmark with the client's SVG logo if preferred.
- **Analytics:** add GA4 `G-8SM4L2Y9QJ`.
- **Content to confirm with the client:**
  - tariffs (not shown)
  - spa status (left out)
  - twin vs king beds in the Haveli Room
  - the +91 99997 66809 number on the terms page
