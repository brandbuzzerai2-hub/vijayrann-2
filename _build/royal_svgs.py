"""Royal Rajputana Vector SVG Elements & Components for The Vijayran Palace."""
import math

def _gen_sun():
    cx, cy = 80, 80
    rays_svg = []
    for i in range(16):
        angle = i * (360 / 16)
        rad = math.radians(angle)
        rad_f = math.radians(angle + 4)
        rad_b = math.radians(angle - 4)
        
        if i % 2 == 0:
            r_base, r_tip = 38, 74
            x1 = cx + r_base * math.cos(rad_b)
            y1 = cy + r_base * math.sin(rad_b)
            x2 = cx + r_tip * math.cos(rad)
            y2 = cy + r_tip * math.sin(rad)
            x3 = cx + r_base * math.cos(rad_f)
            y3 = cy + r_base * math.sin(rad_f)
            mid_x = cx + (r_tip * 0.95) * math.cos(rad)
            mid_y = cy + (r_tip * 0.95) * math.sin(rad)
            rays_svg.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} L {x3:.1f} {y3:.1f} Z" fill="none" stroke="currentColor" stroke-width="1.2"/>')
            rays_svg.append(f'<line x1="{cx + 38 * math.cos(rad):.1f}" y1="{cy + 38 * math.sin(rad):.1f}" x2="{mid_x:.1f}" y2="{mid_y:.1f}" stroke="currentColor" stroke-width="0.8" opacity="0.6"/>')
        else:
            r_base, r_tip = 37, 68
            rad_mid1 = math.radians(angle - 3)
            rad_mid2 = math.radians(angle + 5)
            x1 = cx + r_base * math.cos(rad_b)
            y1 = cy + r_base * math.sin(rad_b)
            c1x = cx + 50 * math.cos(rad_mid1)
            c1y = cy + 50 * math.sin(rad_mid1)
            c2x = cx + 60 * math.cos(rad_mid2)
            c2y = cy + 60 * math.sin(rad_mid2)
            tip_x = cx + r_tip * math.cos(rad)
            tip_y = cy + r_tip * math.sin(rad)
            rays_svg.append(f'<path d="M {x1:.1f} {y1:.1f} Q {c1x:.1f} {c1y:.1f} {tip_x:.1f} {tip_y:.1f} Q {c2x:.1f} {c2y:.1f} {cx + r_base*math.cos(rad_f):.1f} {cy + r_base*math.sin(rad_f):.1f}" fill="none" stroke="currentColor" stroke-width="1.2"/>')

    beads = [f'<circle cx="{cx + 34.5 * math.cos(math.radians(j * 15)):.1f}" cy="{cy + 34.5 * math.sin(math.radians(j * 15)):.1f}" r="1" fill="currentColor"/>' for j in range(24)]
    petals = []
    for k in range(8):
        pa = math.radians(k * 45)
        px = cx + 22 * math.cos(pa)
        py = cy + 22 * math.sin(pa)
        pa_l, pa_r = math.radians(k * 45 - 15), math.radians(k * 45 + 15)
        cpx1 = cx + 16 * math.cos(pa_l)
        cpy1 = cy + 16 * math.sin(pa_l)
        cpx2 = cx + 16 * math.cos(pa_r)
        cpy2 = cy + 16 * math.sin(pa_r)
        petals.append(f'<path d="M {cx + 10 * math.cos(pa_l):.1f} {cy + 10 * math.sin(pa_l):.1f} Q {cpx1:.1f} {cpy1:.1f} {px:.1f} {py:.1f} Q {cpx2:.1f} {cpy2:.1f} {cx + 10 * math.cos(pa_r):.1f} {cy + 10 * math.sin(pa_r):.1f}" fill="none" stroke="currentColor" stroke-width="1"/>')

    rays_joined = "\n  ".join(rays_svg)
    beads_joined = "".join(beads)
    petals_joined = "\n  ".join(petals)

    return f"""<svg class="royal-sun-svg" viewBox="0 0 160 160" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <g class="sun-ray-group">
  {rays_joined}
  </g>
  <g class="sun-core">
    <circle cx="80" cy="80" r="37" stroke="currentColor" stroke-width="1.2"/>
    <circle cx="80" cy="80" r="32" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 3"/>
    {beads_joined}
    <circle cx="80" cy="80" r="26" stroke="currentColor" stroke-width="1"/>
    {petals_joined}
    <circle cx="80" cy="80" r="10" stroke="currentColor" stroke-width="1.2"/>
    <circle cx="80" cy="80" r="4" fill="currentColor"/>
    <path d="M 80 66 Q 83 72 80 76 Q 77 72 80 66 Z" fill="currentColor"/>
  </g>
</svg>"""

ROYAL_SUN = _gen_sun()

ROYAL_ELEPHANT = """<svg class="royal-elephant-svg" viewBox="0 0 240 180" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <g class="el-back-legs" opacity="0.65">
    <path d="M 160 120 L 163 158 Q 163 166 156 166 L 148 166 Q 146 162 147 155 L 148 125"/>
    <ellipse cx="152" cy="164" rx="6" ry="2"/>
    <path d="M 72 118 L 68 158 Q 67 166 60 166 L 52 166 Q 50 162 52 155 L 58 120"/>
    <ellipse cx="56" cy="164" rx="6" ry="2"/>
  </g>
  <g class="el-tail">
    <path d="M 42 78 Q 30 100 32 125 Q 34 135 32 142" stroke-width="1.4"/>
    <path d="M 32 142 Q 28 148 26 155 M 32 142 Q 33 150 35 156 M 32 142 Q 31 152 29 157" stroke-width="1.2"/>
  </g>
  <path d="M 45 76 Q 55 58 85 54 Q 120 50 150 56 Q 170 60 182 72 Q 192 82 198 94 Q 206 106 208 120 Q 212 136 218 136 Q 225 136 226 128 Q 228 116 224 102 Q 220 90 216 88 Q 210 88 206 95" stroke-width="1.5"/>
  <path d="M 216 114 Q 222 118 226 114 M 214 122 Q 220 126 225 121 M 212 128 Q 216 132 222 128"/>
  <g class="el-tusk">
    <path d="M 188 110 Q 202 114 212 106 Q 205 118 186 116 Z" fill="rgba(255,255,255,0.85)" stroke-width="1.3"/>
    <line x1="196" y1="110" x2="194" y2="114" stroke="currentColor" stroke-width="1.4"/>
  </g>
  <path d="M 172 56 Q 182 50 194 54 Q 204 60 206 70 Q 208 78 202 86" stroke-width="1.4"/>
  <circle cx="188" cy="74" r="2.2" fill="currentColor"/>
  <path d="M 183 71 Q 188 68 193 72"/>
  <path d="M 182 58 Q 190 68 198 62" stroke-width="1" stroke-dasharray="2 3"/>
  <circle cx="190" cy="67" r="2" fill="currentColor"/>
  <path d="M 190 69 L 190 75 M 188 75 L 192 75" stroke-width="1"/>
  <g class="el-ear">
    <path d="M 166 60 Q 158 72 158 90 Q 158 112 172 114 Q 180 114 182 102 Q 184 82 178 68 Z" fill="var(--cream,#fbf9f4)" stroke-width="1.3"/>
    <path d="M 164 74 Q 166 88 174 94" stroke-width="0.8" stroke-dasharray="2 2"/>
    <circle cx="170" cy="85" r="2.5" stroke-width="0.8"/>
  </g>
  <g class="el-foreleg">
    <path d="M 176 116 L 178 156 Q 179 166 172 166 L 160 166 Q 156 162 158 152 L 162 118" stroke-width="1.5"/>
    <ellipse cx="166" cy="164" rx="7" ry="2.2"/>
    <path d="M 158 152 Q 168 155 178 152" stroke-width="1.2"/>
    <circle cx="162" cy="155" r="1.5" fill="currentColor"/>
    <circle cx="168" cy="156" r="1.5" fill="currentColor"/>
    <circle cx="174" cy="155" r="1.5" fill="currentColor"/>
  </g>
  <g class="el-hindleg">
    <path d="M 45 76 Q 42 100 48 120 L 52 156 Q 53 166 62 166 L 74 166 Q 78 162 76 150 L 74 116" stroke-width="1.5"/>
    <ellipse cx="68" cy="164" rx="7" ry="2.2"/>
    <path d="M 52 152 Q 63 155 74 152" stroke-width="1.2"/>
    <circle cx="57" cy="155" r="1.5" fill="currentColor"/>
    <circle cx="63" cy="156" r="1.5" fill="currentColor"/>
    <circle cx="69" cy="155" r="1.5" fill="currentColor"/>
  </g>
  <path d="M 74 120 Q 115 128 158 120" stroke-width="1.4"/>
  <g class="el-jhool">
    <path d="M 78 68 Q 115 65 154 70 L 150 124 Q 114 130 76 122 Z" fill="rgba(215,180,106,0.12)" stroke-width="1.4"/>
    <path d="M 78 74 Q 115 71 152 76" stroke-width="0.8"/>
    <path d="M 76 118 Q 114 125 148 119" stroke-width="1"/>
    <path d="M 77 122 Q 83 128 88 123 Q 94 129 100 124 Q 106 130 112 125 Q 118 131 124 126 Q 130 131 136 126 Q 142 131 147 124" stroke-width="1"/>
    <circle cx="88" cy="129" r="1.5" fill="currentColor"/>
    <circle cx="100" cy="130" r="1.5" fill="currentColor"/>
    <circle cx="112" cy="131" r="1.5" fill="currentColor"/>
    <circle cx="124" cy="132" r="1.5" fill="currentColor"/>
    <circle cx="136" cy="131" r="1.5" fill="currentColor"/>
    <circle cx="114" cy="96" r="14" stroke-width="1"/>
    <circle cx="114" cy="96" r="10" stroke-width="0.8" stroke-dasharray="2 2"/>
    <circle cx="114" cy="96" r="4" fill="currentColor"/>
    <path d="M 114 82 L 114 86 M 114 106 L 114 110 M 100 96 L 104 96 M 124 96 L 128 96" stroke-width="1"/>
  </g>
  <g class="el-howdah">
    <rect x="92" y="44" width="46" height="12" rx="2" fill="var(--cream,#fbf9f4)" stroke-width="1.3"/>
    <line x1="92" y1="50" x2="138" y2="50" stroke-width="0.8"/>
    <path d="M 98 44 L 98 26 M 132 44 L 132 26" stroke-width="1.3"/>
    <path d="M 94 26 Q 115 16 136 26" stroke-width="1.4"/>
    <path d="M 94 26 Q 115 22 136 26" stroke-width="0.8"/>
    <path d="M 115 16 L 115 8" stroke-width="1.3"/>
    <circle cx="115" cy="7" r="1.8" fill="currentColor"/>
    <path class="el-flag" d="M 115 9 Q 126 6 136 10 Q 128 13 115 15 Z" fill="currentColor"/>
  </g>
</svg>"""

ROYAL_HORSE = """<svg class="royal-horse-svg" viewBox="0 0 220 180" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <g class="horse-far-legs" opacity="0.65">
    <path d="M 132 102 L 140 135 L 148 162 L 145 166 L 138 166 L 133 138 L 127 108" stroke-width="1.2"/>
    <rect x="138" y="163" width="8" height="4" rx="1" fill="currentColor"/>
    <path d="M 82 92 L 92 122 L 96 154 L 92 165 L 85 165 L 83 148 L 78 116" stroke-width="1.2"/>
    <rect x="85" y="162" width="8" height="4" rx="1" fill="currentColor"/>
  </g>
  <g class="horse-tail">
    <path d="M 52 74 Q 32 70 24 84 Q 18 100 28 120 Q 32 135 24 152" stroke-width="1.4"/>
    <path d="M 48 76 Q 30 82 26 102 Q 24 122 34 145" stroke-width="1"/>
    <path d="M 44 80 Q 34 94 32 116 Q 30 134 38 150" stroke-width="0.8"/>
  </g>
  <path d="M 50 74 Q 54 62 70 60 Q 94 58 114 68 Q 128 75 138 90" stroke-width="1.5"/>
  <path d="M 114 68 Q 132 46 148 28 Q 156 18 164 16 Q 170 16 174 22" stroke-width="1.5"/>
  <path d="M 138 90 Q 150 78 162 62 L 178 52" stroke-width="1.4"/>
  <path d="M 174 22 L 186 32 Q 198 42 206 48 Q 208 52 204 55 Q 196 58 186 54 L 176 52" stroke-width="1.4"/>
  <circle cx="200" cy="50" r="1.5" fill="currentColor"/>
  <circle cx="180" cy="34" r="2" fill="currentColor"/>
  <path d="M 176 30 Q 182 28 186 32" stroke-width="1"/>
  <g class="horse-ears">
    <path d="M 166 18 Q 168 8 174 4 Q 178 8 176 16 Z" fill="var(--cream,#fbf9f4)" stroke-width="1.3"/>
    <path d="M 162 18 Q 164 6 173 4 Q 172 12 168 20 Z" fill="var(--cream,#fbf9f4)" stroke-width="1.3"/>
  </g>
  <g class="horse-kalgi">
    <path d="M 168 8 Q 166 -2 170 -6 Q 174 -2 172 8 Z" fill="currentColor"/>
    <circle cx="170" cy="-7" r="1.5" fill="currentColor"/>
    <path d="M 170 8 L 170 14" stroke-width="1"/>
  </g>
  <g class="horse-mane">
    <path d="M 162 20 Q 154 26 158 32 M 156 30 Q 146 38 150 44 M 148 42 Q 138 52 142 58 M 140 56 Q 128 66 134 72 M 130 70 Q 120 78 126 84" stroke-width="1.3"/>
  </g>
  <g class="horse-bridle">
    <path d="M 174 22 L 178 52" stroke-width="1"/>
    <path d="M 176 34 L 202 52" stroke-width="1"/>
    <circle cx="175" cy="35" r="2" fill="currentColor"/>
    <circle cx="184" cy="53" r="2.2" stroke-width="1"/>
  </g>
  <g class="horse-breastplate">
    <path d="M 138 90 Q 146 102 152 108" stroke-width="1.4"/>
    <circle cx="146" cy="100" r="3" fill="var(--cream,#fbf9f4)" stroke-width="1.2"/>
    <circle cx="146" cy="100" r="1.2" fill="currentColor"/>
    <circle cx="142" cy="106" r="1.4" fill="currentColor"/>
    <circle cx="150" cy="106" r="1.4" fill="currentColor"/>
  </g>
  <g class="horse-foreleg">
    <path d="M 148 100 Q 152 115 158 128 L 172 144 L 176 156 L 170 158 L 164 148 L 150 130 L 140 106" stroke-width="1.5"/>
    <path d="M 170 158 L 176 156 L 178 162 L 168 163 Z" fill="currentColor"/>
    <path d="M 166 150 Q 172 152 176 148" stroke-width="1"/>
  </g>
  <path d="M 138 108 Q 105 112 76 96" stroke-width="1.4"/>
  <g class="horse-hindleg">
    <path d="M 70 60 Q 62 80 60 102 L 64 128 L 60 156 L 52 166 L 44 166 L 48 152 L 52 124 Q 52 98 62 76" stroke-width="1.5"/>
    <rect x="44" y="163" width="9" height="4" rx="1" fill="currentColor"/>
    <path d="M 52 154 Q 58 156 62 153" stroke-width="1"/>
  </g>
  <g class="horse-saddle">
    <path d="M 86 64 Q 106 60 122 66 L 126 86 Q 104 92 84 84 Z" fill="rgba(215,180,106,0.12)" stroke-width="1.3"/>
    <path d="M 84 84 Q 104 92 126 86" stroke-width="1"/>
    <path d="M 85 86 Q 90 91 95 87 Q 100 92 105 88 Q 110 93 115 89 Q 120 93 125 87" stroke-width="1"/>
    <line x1="104" y1="70" x2="102" y2="100" stroke-width="1"/>
    <path d="M 98 100 L 106 100 Q 102 106 98 100" fill="currentColor"/>
  </g>
</svg>"""

ROYAL_CYCLE = """<svg class="royal-cycle-svg" viewBox="0 0 200 150" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
  <line x1="20" y1="138" x2="185" y2="138" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 6" opacity="0.4"/>
  <g class="cycle-rear-wheel">
    <circle cx="52" cy="102" r="32" stroke-width="1.5"/>
    <circle cx="52" cy="102" r="28" stroke-width="0.8"/>
    <path d="M 22 96 Q 24 68 52 68 Q 72 68 80 82" stroke-width="1.8"/>
    <line x1="52" y1="102" x2="28" y2="82" stroke-width="0.9"/>
    <circle cx="52" cy="102" r="3.5" fill="currentColor"/>
    <g class="wheel-spokes">
      <line x1="52" y1="74" x2="52" y2="130" stroke-width="0.75" opacity="0.7"/>
      <line x1="24" y1="102" x2="80" y2="102" stroke-width="0.75" opacity="0.7"/>
      <line x1="32" y1="82" x2="72" y2="122" stroke-width="0.75" opacity="0.7"/>
      <line x1="32" y1="122" x2="72" y2="82" stroke-width="0.75" opacity="0.7"/>
      <line x1="40" y1="76" x2="64" y2="128" stroke-width="0.75" opacity="0.7"/>
      <line x1="64" y1="76" x2="40" y2="128" stroke-width="0.75" opacity="0.7"/>
    </g>
  </g>
  <g class="cycle-front-wheel">
    <circle cx="154" cy="102" r="32" stroke-width="1.5"/>
    <circle cx="154" cy="102" r="28" stroke-width="0.8"/>
    <path d="M 126 88 Q 140 68 166 72 Q 182 82 186 98" stroke-width="1.8"/>
    <line x1="154" y1="102" x2="178" y2="88" stroke-width="0.9"/>
    <circle cx="154" cy="102" r="3.5" fill="currentColor"/>
    <g class="wheel-spokes">
      <line x1="154" y1="74" x2="154" y2="130" stroke-width="0.75" opacity="0.7"/>
      <line x1="126" y1="102" x2="182" y2="102" stroke-width="0.75" opacity="0.7"/>
      <line x1="134" y1="82" x2="174" y2="122" stroke-width="0.75" opacity="0.7"/>
      <line x1="134" y1="122" x2="174" y2="82" stroke-width="0.75" opacity="0.7"/>
      <line x1="142" y1="76" x2="166" y2="128" stroke-width="0.75" opacity="0.7"/>
      <line x1="166" y1="76" x2="142" y2="128" stroke-width="0.75" opacity="0.7"/>
    </g>
  </g>
  <g class="cycle-frame">
    <line x1="52" y1="102" x2="100" y2="102" stroke-width="1.5"/>
    <line x1="52" y1="102" x2="88" y2="60" stroke-width="1.5"/>
    <line x1="100" y1="102" x2="88" y2="52" stroke-width="1.6"/>
    <line x1="100" y1="102" x2="142" y2="54" stroke-width="1.6"/>
    <line x1="88" y1="60" x2="142" y2="54" stroke-width="1.6"/>
    <line x1="90" y1="65" x2="141" y2="60" stroke-width="1" stroke-dasharray="3 3"/>
    <line x1="142" y1="52" x2="144" y2="62" stroke-width="2"/>
    <path d="M 144 62 L 154 102" stroke-width="1.6"/>
  </g>
  <g class="cycle-pedals">
    <circle cx="100" cy="102" r="8" stroke-width="1.3"/>
    <circle cx="100" cy="102" r="2.5" fill="currentColor"/>
    <line x1="100" y1="102" x2="94" y2="114" stroke-width="1.5"/>
    <rect x="88" y="113" width="12" height="3" rx="1" fill="currentColor"/>
    <path d="M 96 94 Q 108 94 112 102 L 68 104" stroke-width="1"/>
  </g>
  <g class="cycle-saddle">
    <line x1="88" y1="52" x2="87" y2="44" stroke-width="1.5"/>
    <circle cx="83" cy="46" r="2" stroke-width="1"/>
    <circle cx="87" cy="46" r="2" stroke-width="1"/>
    <path d="M 76 43 Q 86 40 102 44 Q 96 46 82 46 Z" fill="currentColor"/>
  </g>
  <g class="cycle-handlebars">
    <line x1="142" y1="52" x2="140" y2="38" stroke-width="1.6"/>
    <path d="M 140 38 Q 134 36 128 40" stroke-width="1.6"/>
    <path d="M 140 38 Q 146 36 150 40" stroke-width="1.6"/>
    <rect x="124" y="38" width="6" height="3" rx="1" fill="currentColor"/>
    <circle cx="138" cy="34" r="2.5" fill="var(--cream,#fbf9f4)" stroke-width="1.2"/>
  </g>
  <g class="cycle-basket">
    <path d="M 148 44 L 174 44 L 170 66 L 152 66 Z" fill="rgba(215,180,106,0.18)" stroke-width="1.2"/>
    <line x1="150" y1="51" x2="172" y2="51" stroke-width="0.8"/>
    <line x1="151" y1="58" x2="171" y2="58" stroke-width="0.8"/>
    <line x1="158" y1="44" x2="158" y2="66" stroke-width="0.8"/>
    <line x1="165" y1="44" x2="165" y2="66" stroke-width="0.8"/>
    <g class="basket-flowers">
      <circle cx="154" cy="41" r="3" fill="var(--cream,#fbf9f4)" stroke-width="1"/>
      <circle cx="154" cy="41" r="1" fill="currentColor"/>
      <circle cx="162" cy="38" r="3.5" fill="var(--cream,#fbf9f4)" stroke-width="1"/>
      <circle cx="162" cy="38" r="1.2" fill="currentColor"/>
      <circle cx="170" cy="40" r="3" fill="var(--cream,#fbf9f4)" stroke-width="1"/>
      <circle cx="170" cy="40" r="1" fill="currentColor"/>
      <path d="M 158 37 Q 160 32 165 34" stroke-width="1"/>
      <path d="M 166 38 Q 174 34 176 42" stroke-width="1"/>
    </g>
  </g>
</svg>"""

def royal_procession_strip():
    caravan_unit = f"""
      <div class="rp-caravan-item" style="width:170px;height:128px;">{ROYAL_ELEPHANT}</div>
      <div class="rp-caravan-item" style="width:155px;height:128px;">{ROYAL_HORSE}</div>
      <div class="rp-caravan-item" style="width:140px;height:105px;margin-bottom:2px;">{ROYAL_CYCLE}</div>"""
    return f"""<div class="royal-procession" data-fade>
  <div class="rp-banner-head">
    <span>✦ The Royal Estate Promenade · Ceremonial Heritage Caravan ✦</span>
  </div>
  <div class="rp-sun-badge">
    {ROYAL_SUN}
  </div>
  <div class="rp-track-wrap">
    <div class="rp-horizon-line"></div>
    <div class="rp-caravan">
      {caravan_unit}
      {caravan_unit}
      {caravan_unit}
      {caravan_unit}
    </div>
  </div>
</div>"""

def royal_pursuits():
    return f"""<section class="royal-pursuits" id="royal-pursuits">
  <div class="rp-head" data-fade>
    <span class="rp-tag">✦ Heritage Living · Rajputana Traditions ✦</span>
    <h2 class="rp-title" data-split>Royal Pursuits of the Estate</h2>
    <p class="rp-sub" data-split="text">Experience the timeless pastimes of Rajasthani royalty: morning rides into the Aravallis, majestic elephant interactions, vintage cycling through countryside trails, and solar yoga at dawn.</p>
  </div>
  <div class="rp-grid" data-fade>
    <div class="rp-card">
      <span class="rp-tag">Equestrian Nobility</span>
      <div class="rp-svg-wrap">
        {ROYAL_HORSE}
      </div>
      <h3>Marwari Stallion</h3>
      <p>Ride purebred Marwari steeds with distinctive lyre-shaped ears through scenic mountain trails and palace grounds.</p>
    </div>
    <div class="rp-card">
      <span class="rp-tag">Ceremonial Majesty</span>
      <div class="rp-svg-wrap">
        {ROYAL_ELEPHANT}
      </div>
      <h3>Gajraj in Motion</h3>
      <p>Gentle walks, feeding, and ceremonial evening processions with adorned palace elephants near ancient Amber.</p>
    </div>
    <div class="rp-card">
      <span class="rp-tag">Estate Exploration</span>
      <div class="rp-svg-wrap">
        {ROYAL_CYCLE}
      </div>
      <h3>Countryside Cycling</h3>
      <p>Crisp morning rides on vintage roadster bicycles along tranquil Kukas trails, organic farms, and bird reserves.</p>
    </div>
    <div class="rp-card">
      <span class="rp-tag">Celestial Wellness</span>
      <div class="rp-svg-wrap">
        {ROYAL_SUN}
      </div>
      <h3>Surya Vandana</h3>
      <p>Guided morning sun salutations and pranayama to birdsong on the dew-kissed lawns under the benevolent Rajasthan sun.</p>
    </div>
  </div>
</section>"""
