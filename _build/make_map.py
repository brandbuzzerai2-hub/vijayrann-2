#!/usr/bin/env python3
"""Generates assets/img/map-jaipur.svg: an illustrated, TO-SCALE map of The Vijayran Palace and Jaipur.
Coordinates: Google Places (Nov 2026). Projection: equirectangular, cos(lat) corrected, 1 px = 1/18.4 km."""
import math, os

LAT0, LAT1 = 26.872, 27.118          # south / north edge
LON0, LON1 = 75.735, 76.000          # west / east edge
KM_LAT = 110.95
KM_LON = 111.32 * math.cos(math.radians((LAT0 + LAT1) / 2))
PAD = 0
H_KM = (LAT1 - LAT0) * KM_LAT
W_KM = (LON1 - LON0) * KM_LON
K = 560 / H_KM                       # px per km
W, H = round(W_KM * K), 560

def xy(lat, lon):
    return ((lon - LON0) * KM_LON * K, (LAT1 - lat) * KM_LAT * K)

def km(a, b):
    R = 6371.0
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(d))

P = {  # name: (lat, lon)
    "vijayran": (27.0860, 75.8882),
    "amber":    (26.9855, 75.8513),
    "jaigarh":  (26.9816, 75.8448),
    "jalmahal": (26.9535, 75.8461),
    "nahargarh":(26.9402, 75.8170),
    "gaitore":  (26.9432, 75.8245),
    "hawa":     (26.9240, 75.8267),
    "city":     (26.9258, 75.8237),
    "birla":    (26.8922, 75.8153),
    "airport":  (26.8283, 75.8060),
}
D = {k: km(P["vijayran"], v) for k, v in P.items()}

def pt(k): return xy(*P[k])

def path(points):
    pts = [xy(a, b) for a, b in points]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def smooth(points):
    pts = [xy(a, b) for a, b in points]
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        d += f" Q{x0:.1f},{y0:.1f} {mx:.1f},{my:.1f}" if i > 1 else ""
    d += f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f}"
    return d

def hills(cx, cy, n, w, h, seed):
    """a little cluster of hand-drawn hill outlines"""
    out = []
    for i in range(n):
        dx = (i - (n - 1) / 2) * w * .55 + ((seed * (i + 3)) % 7 - 3)
        dy = ((seed * (i + 5)) % 5 - 2) * 2.2
        ww = w * (.8 + ((seed + i) % 3) * .15); hh = h * (.75 + ((seed + 2 * i) % 3) * .18)
        x, y = cx + dx, cy + dy
        out.append(f'<path d="M{x-ww/2:.1f},{y:.1f} Q{x-ww/4:.1f},{y-hh:.1f} {x:.1f},{y-hh:.1f} Q{x+ww/4:.1f},{y-hh:.1f} {x+ww/2:.1f},{y:.1f}"/>')
        out.append(f'<path d="M{x:.1f},{y-hh:.1f} Q{x+ww/8:.1f},{y-hh/2:.1f} {x+ww/6:.1f},{y:.1f}" opacity=".45"/>')
    return "".join(out)

def ridge(points, step=13, h=12, seed=1):
    """hills placed along a ridgeline (lat,lon) polyline"""
    pts = [xy(a, b) for a, b in points]
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0); n = max(1, int(L / step))
        for i in range(n):
            t = i / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            out.append(hills(x, y, 1, step * 1.5, h * (.8 + (i * seed % 4) * .12), seed + i))
    return "".join(out)

# --------------------------------------------------------------------------- features
# Aravalli ridges (approximate ridgelines of the Amer–Jaigarh–Nahargarh hills and the Kukas hills)
RIDGES = [
    [(26.934, 75.800), (26.945, 75.815), (26.958, 75.830), (26.972, 75.840), (26.988, 75.842), (27.002, 75.845), (27.018, 75.852)],
    [(26.990, 75.868), (27.004, 75.875), (27.020, 75.866), (27.036, 75.858), (27.052, 75.860)],
    [(27.062, 75.862), (27.074, 75.866), (27.098, 75.872), (27.110, 75.885)],
]
# NH-48 (Jaipur – Delhi) – approximate alignment through Amer and Kukas
NH48 = [(26.9345, 75.8330), (26.9420, 75.8470), (26.9530, 75.8545), (26.9660, 75.8555),
        (26.985, 75.856), (27.005, 75.868), (27.030, 75.890), (27.055, 75.905), (27.085, 75.925), (27.118, 75.950)]
APPROACH = [(27.050, 75.902), (27.060, 75.897), (27.070, 75.893), (27.079, 75.890), (27.0860, 75.8882)]   # local road into the hills (indicative)
WALLED = [(26.9345, 75.8115), (26.9345, 75.8360), (26.9160, 75.8380), (26.9140, 75.8120)]  # Pink City walled city (approx.)

def lake(lat, lon, rx_km, ry_km, rot=-20):
    x, y = xy(lat, lon)
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx_km*K:.1f}" ry="{ry_km*K:.1f}" transform="rotate({rot} {x:.1f} {y:.1f})"/>'

# --------------------------------------------------------------------------- icons
def fort(x, y, s=1):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" fill="#FBF9F7" stroke="#322B26" stroke-width=".9" stroke-linejoin="round">'
            '<path d="M-9,4 V-4 H-6 V-6 H-4 V-4 H-1 V-8 H1 V-4 H4 V-6 H6 V-4 H9 V4 Z"/><path d="M-1.6,4 V0.5 Q0,-1.4 1.6,0.5 V4" fill="none"/></g>')
def palace(x, y, s=1):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" fill="#FBF9F7" stroke="#322B26" stroke-width=".9" stroke-linejoin="round">'
            '<path d="M-9,5 V-2 H9 V5 Z"/><path d="M-4,-2 Q-4,-8 0,-9 Q4,-8 4,-2"/><path d="M0,-9 V-11"/>'
            '<path d="M-9,-2 Q-9,-5 -7,-5 Q-5,-5 -5,-2 M5,-2 Q5,-5 7,-5 Q9,-5 9,-2"/></g>')
def temple(x, y, s=1):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s})" fill="#FBF9F7" stroke="#322B26" stroke-width=".9" stroke-linejoin="round">'
            '<path d="M-7,5 V0 H7 V5 Z"/><path d="M-4,0 Q-4,-6 0,-10 Q4,-6 4,0"/><path d="M0,-10 V-12.5"/></g>')
def dot(x, y, r=2.6): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#322B26"/>'

def label(x, y, t, size=13, anchor="start", sub=None, col="#322B26", italic=False):
    st = ' font-style="italic"' if italic else ''
    s = f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{col}"{st}>{t}</text>'
    if sub:
        s += f'<text x="{x:.1f}" y="{y+12.5:.1f}" font-size="9.5" text-anchor="{anchor}" fill="#79716A" font-family="Inter,Arial,sans-serif" letter-spacing=".02em">{sub}</text>'
    return s

def build():
    vx, vy = pt("vijayran")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="mt md" font-family="Crimson Pro,Minion Pro,Georgia,serif">',
         '<title id="mt">Map: The Vijayran Palace, Amer and Jaipur</title>',
         f'<desc id="md">To-scale illustrated map. The Vijayran Palace is in the Aravalli hills at Kukas, about {D["amber"]:.0f} km north of Amber Fort and {D["hawa"]:.0f} km from Hawa Mahal in the walled Pink City.</desc>',
         '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0,0 V6" stroke="#C98B7E" stroke-width=".7" opacity=".55"/></pattern>'
         '<radialGradient id="glow"><stop offset="0" stop-color="#D7B46A" stop-opacity=".35"/><stop offset="1" stop-color="#D7B46A" stop-opacity="0"/></radialGradient>'
         '<clipPath id="clip"><rect x="0" y="0" width="100%" height="100%" rx="6"/></clipPath></defs>',
         f'<g clip-path="url(#clip)"><rect width="{W}" height="{H}" fill="#EFE7D8"/>']
    # paper texture lines
    o.append('<g stroke="#e8dfcd" stroke-width=".5" opacity=".6">' + "".join(f'<path d="M0,{y} H{W}"/>' for y in range(14, H, 28)) + '</g>')
    # distance rings
    for r in (5, 10, 15, 20, 25):
        o.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="{r*K:.1f}" fill="none" stroke="#B9822B" stroke-width=".7" stroke-dasharray="2 4" opacity=".55"/>')
        ang = math.radians(208)
        lx, ly = vx + r * K * math.cos(ang), vy - r * K * math.sin(ang)
        if 8 < lx < W - 8 and 12 < ly < H - 8:
            o.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="9" fill="#B9822B" font-family="Inter,Arial,sans-serif" text-anchor="middle">{r} km</text>')
    o.append(f'<circle cx="{vx:.1f}" cy="{vy:.1f}" r="46" fill="url(#glow)"/>')
    # hills
    o.append('<g fill="none" stroke="#9c8468" stroke-width=".9" stroke-linecap="round">' + "".join(ridge(r, seed=i + 2) for i, r in enumerate(RIDGES)) + '</g>')
    # lakes
    o.append('<g fill="#C9D6CF" stroke="#8FA69C" stroke-width=".8">' + lake(26.9535, 75.8470, .55, 1.05, -10) + lake(26.9838, 75.8528, .22, .14, 0) + '</g>')
    # walled Pink City
    wx = [xy(a, b) for a, b in WALLED]
    o.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in wx) + ' Z" fill="url(#hatch)" stroke="#C98B7E" stroke-width="1" stroke-dasharray="3 2"/>')
    o.append(f'<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in wx) + ' Z" fill="#E7B7A9" opacity=".28"/>')
    # roads
    o.append(f'<path d="{smooth(NH48)}" fill="none" stroke="#FBF9F7" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<path d="{smooth(NH48)}" fill="none" stroke="#B9822B" stroke-width="2" stroke-linecap="round"/>')
    o.append(f'<path d="{path(APPROACH)}" fill="none" stroke="#B9822B" stroke-width="1.2" stroke-dasharray="3 3"/>')
    nx, ny = xy(27.100, 75.938)
    o.append(f'<g transform="translate({nx:.1f},{ny:.1f}) rotate(-58)"><rect x="-17" y="-7" width="34" height="14" rx="3" fill="#B9822B"/><text x="0" y="3.6" font-size="9" fill="#FBF9F7" text-anchor="middle" font-family="Inter,Arial,sans-serif">NH 48</text></g>')
    arx, ary = xy(26.9470, 75.8580)
    o.append(f'<text x="{arx+8:.1f}" y="{ary:.1f}" font-size="9" fill="#B9822B" font-family="Inter,Arial,sans-serif" letter-spacing=".08em">AMER ROAD</text>')
    tx, ty = xy(27.108, 75.962)
    o.append(f'<text x="{tx+6:.1f}" y="{ty-8:.1f}" font-size="9.5" fill="#79716A" font-family="Inter,Arial,sans-serif">to Delhi ↗</text>')
    # landmarks + labels
    ax, ay = pt("amber"); jx, jy = pt("jaigarh"); mx, my = pt("jalmahal"); nx2, ny2 = pt("nahargarh"); gx, gy = pt("gaitore")
    hx, hy = pt("hawa"); cx, cy = pt("city"); bx, by = pt("birla")
    o += [fort(ax, ay, 1.15), label(ax + 13, ay + 4, "Amber Fort", 14, sub=f"{D['amber']:.0f} km"),
          fort(jx, jy - 1, .85), label(jx - 12, jy - 6, "Jaigarh", 11.5, "end"),
          palace(mx, my, .8), label(mx - 13, my - 9, "Jal Mahal", 12, "end", italic=True),
          fort(nx2, ny2 + 2, .95), label(nx2 - 12, ny2 + 6, "Nahargarh", 12.5, "end"),
          temple(gx, gy - 2, .7), label(gx + 9, gy + 2, "Gaitore", 11, sub=None),
          palace(hx + 2, hy, .9), label(hx + 14, hy + 4, "Hawa Mahal", 13.5, sub=f"{D['hawa']:.0f} km"),
          dot(cx, cy, 2.4), label(cx - 7, cy - 6, "City Palace", 11.5, "end"),
          temple(bx, by, .9), label(bx + 11, by + 4, "Birla Mandir", 12.5)]
    # Pink City label
    pcx, pcy = xy(26.9040, 75.7700)
    o.append(f'<text x="{pcx:.1f}" y="{pcy:.1f}" font-size="26" fill="#B9822B" letter-spacing="2" text-anchor="middle">JAIPUR</text>')
    o.append(f'<text x="{pcx:.1f}" y="{pcy+14:.1f}" font-size="10" fill="#79716A" text-anchor="middle" font-family="Inter,Arial,sans-serif" letter-spacing=".08em">THE PINK CITY</text>')
    # Amer town label
    amx, amy = xy(26.9960, 75.8600)
    o.append(f'<text x="{amx+12:.1f}" y="{amy:.1f}" font-size="9.5" fill="#79716A" font-family="Inter,Arial,sans-serif" letter-spacing=".12em">AMER</text>')
    kx, ky = xy(27.040, 75.905)
    o.append(f'<text x="{kx+10:.1f}" y="{ky+4:.1f}" font-size="9.5" fill="#79716A" font-family="Inter,Arial,sans-serif" letter-spacing=".12em">KUKAS</text>')
    hlx, hly = xy(27.112, 75.760)
    o.append(f'<text x="{hlx:.1f}" y="{hly:.1f}" font-size="10" fill="#79716A" font-family="Inter,Arial,sans-serif" letter-spacing=".18em">ARAVALLI HILLS</text>')
    # airport (off-map, bottom edge)
    apx, _ = pt("airport")
    o.append(f'<g font-family="Inter,Arial,sans-serif"><path d="M{apx:.1f},{H-30} v18 m-5,-6 l5,6 l5,-6" fill="none" stroke="#322B26" stroke-width="1"/>'
             f'<text x="{apx+10:.1f}" y="{H-18}" font-size="10" fill="#322B26">Jaipur Airport · {D["airport"]:.0f} km</text></g>')
    # the palace marker
    o.append(f'<g transform="translate({vx:.1f},{vy:.1f})"><circle r="15" fill="#8D1711" opacity=".14"/><circle r="9" fill="#8D1711" stroke="#FBF9F7" stroke-width="2.5"/>'
             f'<path d="M-3.5,2.5 V-0.5 Q-3.5,-3.5 0,-4.5 Q3.5,-3.5 3.5,-0.5 V2.5 Z" fill="#FBF9F7"/></g>')
    o.append(f'<rect x="{vx+16:.1f}" y="{vy-23:.1f}" width="170" height="40" rx="4" fill="#FBF9F7" opacity=".92"/>')
    o.append(label(vx + 24, vy - 6, "The Vijayran Palace", 16.5, sub="Kukas · in the Aravalli hills"))
    # compass + scale bar
    o.append(f'<g transform="translate({W-34},46)" font-family="Inter,Arial,sans-serif"><circle r="15" fill="#FBF9F7" stroke="#9c8468" stroke-width=".8"/>'
             '<path d="M0,-11 L4,3 L0,0 L-4,3 Z" fill="#322B26"/><text y="-19" font-size="10" text-anchor="middle" fill="#322B26">N</text></g>')
    sb = 5 * K
    o.append(f'<g transform="translate(22,{H-22})" font-family="Inter,Arial,sans-serif" fill="#322B26"><rect width="{sb/2:.1f}" height="4" fill="#322B26"/><rect x="{sb/2:.1f}" width="{sb/2:.1f}" height="4" fill="#FBF9F7" stroke="#322B26" stroke-width=".6"/>'
             f'<text y="-5" font-size="9">0</text><text x="{sb:.1f}" y="-5" font-size="9" text-anchor="middle">5 km</text></g>')
    o.append('</g>')
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="#d9cbb3"/></svg>')
    svg = "".join(o)
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img", "map-jaipur.svg")
    open(out, "w").write(svg)
    print("map", W, "x", H, "px/km", round(K, 2), {k: round(v, 1) for k, v in D.items()})

if __name__ == "__main__":
    build()
