#!/usr/bin/env python3
"""Generate the royal architectural sketch of The Vijayran Palace."""
import math, xml.etree.ElementTree as ET

def generate_sketch_svg():
    # 780 x 430 viewBox
    parts = []
    parts.append('<svg class="sk" viewBox="0 0 780 430" fill="none" stroke="currentColor" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round" aria-label="The Vijayran Palace architectural illustration with the royal sun, ceremonial elephant, and running Marwari horses">')

    # 1. ARAVALLI HILLS & BIRDS
    hills = [
        '<g class="sk-hills" stroke-width="0.85" opacity="0.65">',
        '  <path d="M 10 265 Q 110 220 210 248 Q 300 215 390 230 Q 480 205 570 240 Q 660 215 770 248" />',
        '  <path d="M 40 280 Q 150 245 250 262 Q 360 238 480 262 Q 620 235 740 268" stroke-dasharray="3,3" />',
        '  <!-- Soaring royal falcons/birds -->',
        '  <path d="M 160 145 Q 168 138 174 143 Q 180 138 188 145" />',
        '  <path d="M 195 160 Q 201 154 206 158 Q 211 154 217 160" />',
        '  <path d="M 580 130 Q 588 123 594 128 Q 600 123 608 130" />',
        '</g>'
    ]
    parts.extend(hills)

    # 2. ROYAL RAJPUT RADIANT SUN (SURYA)
    # Centered at (390, 72)
    cx, cy = 390, 72
    r_core = 21
    sun = [
        '<g class="sk-sun" style="transform-origin: 390px 72px;">',
        f'  <circle cx="{cx}" cy="{cy}" r="{r_core}" stroke-width="1.3" />',
        f'  <circle cx="{cx}" cy="{cy}" r="15" stroke-dasharray="2,2.5" stroke-width="0.75" opacity="0.75" />',
        '  <!-- Rajput Royal Tilak & Solar Countenance -->',
        '  <path d="M 390 60 Q 393 65 390 71 Q 387 65 390 60 Z" fill="currentColor" />',
        '  <circle cx="390" cy="74.5" r="1.3" fill="currentColor" />',
        '  <path d="M 383.5 70.5 Q 386 68.5 388 70.5" stroke-width="0.9" />',
        '  <path d="M 392 70.5 Q 394 68.5 396.5 70.5" stroke-width="0.9" />',
        '  <path d="M 386.5 76 Q 390 78.5 393.5 76" stroke-width="0.9" />',
        '  <!-- Radiating Ornate Sunbeams -->',
        '  <g class="sk-sun-rays">'
    ]
    # 16 rays around perimeter
    for i in range(16):
        angle = i * (2 * math.pi / 16)
        deg = i * 22.5
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        r_start = r_core + 4
        if i % 2 == 0:
            # Straight pointed primary spear ray
            r_end = r_core + 20
            x1 = cx + r_start * cos_a
            y1 = cy + r_start * sin_a
            x2 = cx + r_end * cos_a
            y2 = cy + r_end * sin_a
            sun.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke-width="1.2" />')
        else:
            # Flame / undulating curved secondary ray
            r_mid = r_core + 9
            r_end = r_core + 15
            perp_cos = -sin_a
            perp_sin = cos_a
            x1 = cx + r_start * cos_a
            y1 = cy + r_start * sin_a
            xm = cx + r_mid * cos_a + 3.5 * perp_cos
            ym = cy + r_mid * sin_a + 3.5 * perp_sin
            x2 = cx + r_end * cos_a
            y2 = cy + r_end * sin_a
            sun.append(f'    <path d="M {x1:.1f} {y1:.1f} Q {xm:.1f} {ym:.1f} {x2:.1f} {y2:.1f}" stroke-width="1.0" />')
    sun.extend([
        '  </g>',
        '</g>'
    ])
    parts.extend(sun)

    # 3. THE VIJAYRAN PALACE FACADE (Faithful to g10.jpg & horse-img.jpg)
    palace = [
        '<g class="sk-palace">',
        '  <!-- Base Plinth & Tiered Courtyard Steps -->',
        '  <rect x="230" y="385" width="320" height="20" rx="1" />',
        '  <line x1="230" y1="395" x2="550" y2="395" stroke-dasharray="6,4" />',
        '  <path d="M 320 385 L 320 405 L 460 405 L 460 385" />',
        '  <line x1="330" y1="392" x2="450" y2="392" />',
        '  <line x1="340" y1="399" x2="440" y2="399" />',
        '  <!-- Carved Stone Jali Lanterns flanking entrance steps -->',
        '  <path d="M 305 385 L 305 368 L 318 368 L 318 385 Z M 302 368 L 321 368 M 307 368 L 311 360 L 316 368" />',
        '  <path d="M 462 385 L 462 368 L 475 368 L 475 385 Z M 459 368 L 478 368 M 464 368 L 468 360 L 473 368" />',
        '',
        '  <!-- Ground Level Main Palace Haveli Wall -->',
        '  <rect x="240" y="260" width="300" height="125" />',
        '  <!-- Projecting Cornice (Chhajja) with stone bracket corbels -->',
        '  <line x1="228" y1="260" x2="552" y2="260" stroke-width="1.6" />',
        '  <line x1="232" y1="264" x2="548" y2="264" />',
        '  <path d="M 248 264 L 248 272 M 275 264 L 275 272 M 305 264 L 305 272 M 475 264 L 475 272 M 505 264 L 505 272 M 532 264 L 532 272" />',
        '',
        '  <!-- Grand Rajput Ceremonial Entrance Portal (Torana / Pol) -->',
        '  <rect x="330" y="275" width="120" height="110" />',
        '  <rect x="335" y="280" width="110" height="105" stroke-dasharray="3,3" />',
        '  <!-- Multi-foil Cusped Royal Arch -->',
        '  <path d="M 345 385 L 345 330 Q 345 315 355 310 Q 365 300 375 296 Q 390 282 390 274 Q 390 282 405 296 Q 415 300 425 310 Q 435 315 435 330 L 435 385" stroke-width="1.4" />',
        '  <!-- Fresco Floral Outer Arch Frame -->',
        '  <path d="M 340 385 L 340 325 Q 340 305 360 295 Q 390 274 390 268 Q 390 274 420 295 Q 440 305 440 325 L 440 385" />',
        '  <!-- Studded Teakwood Heavy Palace Doors -->',
        '  <line x1="390" y1="298" x2="390" y2="385" stroke-width="1.3" />',
        '  <path d="M 355 335 H 380 M 355 360 H 380 M 400 335 H 425 M 400 360 H 425" stroke-width="0.9" />',
        '  <circle cx="367" cy="335" r="1.5" fill="currentColor" /><circle cx="367" cy="360" r="1.5" fill="currentColor" />',
        '  <circle cx="413" cy="335" r="1.5" fill="currentColor" /><circle cx="413" cy="360" r="1.5" fill="currentColor" />',
        '',
        '  <!-- Left Haveli Wing: Hand-carved Jharoka (from Jharoka Suites) -->',
        '  <g class="sk-jharoka-left">',
        '    <!-- Projecting base with elephant-trunk style brackets -->',
        '    <path d="M 262 345 L 298 345 L 294 358 L 266 358 Z" />',
        '    <path d="M 270 358 Q 272 368 280 372 M 290 358 Q 288 368 280 372" />',
        '    <!-- Cusped Window Arch & Jali Screen -->',
        '    <path d="M 266 345 L 266 312 Q 266 300 280 292 Q 294 300 294 312 L 294 345" />',
        '    <line x1="280" y1="295" x2="280" y2="345" stroke-width="0.8" />',
        '    <line x1="266" y1="325" x2="294" y2="325" stroke-width="0.8" />',
        '    <!-- Carved Canopy (Chhajja) -->',
        '    <path d="M 258 292 Q 280 282 302 292" stroke-width="1.3" />',
        '    <path d="M 264 286 Q 280 278 296 286" />',
        '  </g>',
        '',
        '  <!-- Right Haveli Wing: Hand-carved Jharoka (from Jharoka Suites) -->',
        '  <g class="sk-jharoka-right">',
        '    <!-- Projecting base with brackets -->',
        '    <path d="M 482 345 L 518 345 L 514 358 L 486 358 Z" />',
        '    <path d="M 490 358 Q 492 368 500 372 M 510 358 Q 508 368 500 372" />',
        '    <!-- Cusped Window Arch & Jali Screen -->',
        '    <path d="M 486 345 L 486 312 Q 486 300 500 292 Q 514 300 514 312 L 514 345" />',
        '    <line x1="500" y1="295" x2="500" y2="345" stroke-width="0.8" />',
        '    <line x1="486" y1="325" x2="514" y2="325" stroke-width="0.8" />',
        '    <!-- Carved Canopy (Chhajja) -->',
        '    <path d="M 478 292 Q 500 282 522 292" stroke-width="1.3" />',
        '    <path d="M 484 286 Q 500 278 516 286" />',
        '  </g>',
        '',
        '  <!-- Upper Terrace Level & Balustrade with continuous miniature arches (from g10.jpg) -->',
        '  <rect x="238" y="244" width="304" height="16" />',
        '  <path d="M 245 260 L 245 250 Q 248 246 251 250 L 251 260 M 256 260 L 256 250 Q 259 246 262 250 L 262 260 M 267 260 L 267 250 Q 270 246 273 250 L 273 260 M 278 260 L 278 250 Q 281 246 284 250 L 284 260 M 289 260 L 289 250 Q 292 246 295 250 L 295 260 M 300 260 L 300 250 Q 303 246 306 250 L 306 260 M 474 260 L 474 250 Q 477 246 480 250 L 480 260 M 485 260 L 485 250 Q 488 246 491 250 L 491 260 M 496 260 L 496 250 Q 499 246 502 250 L 502 260 M 507 260 L 507 250 Q 510 246 513 250 L 513 260 M 518 260 L 518 250 Q 521 246 524 250 L 524 260 M 529 260 L 529 250 Q 532 246 535 250 L 535 260" stroke-width="0.8" />',
        '',
        '  <!-- Center Rooftop: The 5-Arch Baradari Pavilion (Iconic from horse-img.jpg) -->',
        '  <g class="sk-baradari">',
        '    <rect x="316" y="174" width="148" height="70" />',
        '    <!-- 5 Arched Bays -->',
        '    <path d="M 322 244 L 322 198 Q 322 188 333 182 Q 344 188 344 198 L 344 244" />',
        '    <path d="M 348 244 L 348 198 Q 348 188 359 182 Q 370 188 370 198 L 370 244" />',
        '    <path d="M 374 244 L 374 196 Q 374 184 390 177 Q 406 184 406 196 L 406 244" stroke-width="1.3" />',
        '    <path d="M 410 244 L 410 198 Q 410 188 421 182 Q 432 188 432 198 L 432 244" />',
        '    <path d="M 436 244 L 436 198 Q 436 188 447 182 Q 458 188 458 198 L 458 244" />',
        '    <!-- Bangla Curved Vaulted Roof with Kalash Finials -->',
        '    <path d="M 312 174 Q 390 148 468 174" stroke-width="1.5" />',
        '    <path d="M 314 170 Q 390 142 466 170" />',
        '    <!-- Kalash Finials -->',
        '    <path d="M 390 142 L 390 126 M 387 132 H 393 M 388 128 H 392" />',
        '    <circle cx="390" cy="125" r="1.5" fill="currentColor" />',
        '    <path d="M 345 158 L 345 148 M 435 158 L 435 148" />',
        '  </g>',
        '',
        '  <!-- Left Corner Octagonal Domed Chattri (from Main-Gate.jpg) -->',
        '  <g class="sk-chattri-left">',
        '    <!-- Columns -->',
        '    <line x1="244" y1="244" x2="244" y2="204" />',
        '    <line x1="254" y1="244" x2="254" y2="204" />',
        '    <line x1="266" y1="244" x2="266" y2="204" />',
        '    <line x1="276" y1="244" x2="276" y2="204" />',
        '    <path d="M 244 212 Q 249 205 254 212 M 254 212 Q 260 205 266 212 M 266 212 Q 271 205 276 212" />',
        '    <!-- Chhajja (Eaves) -->',
        '    <path d="M 238 204 Q 260 196 282 204" stroke-width="1.4" />',
        '    <!-- Fluted Rajput Dome Cap -->',
        '    <path d="M 242 204 Q 260 170 278 204" stroke-width="1.3" />',
        '    <path d="M 251 204 Q 260 174 269 204" stroke-width="0.8" />',
        '    <path d="M 260 170 L 260 156" />',
        '    <circle cx="260" cy="155" r="1.4" fill="currentColor" />',
        '    <!-- Royal Pennant Flag (Gentle Wind Flutter) -->',
        '    <path class="sk-flag" d="M 260 156 Q 248 160 236 156 Q 248 164 260 168 Z" fill="rgba(215,180,106,0.3)" />',
        '  </g>',
        '',
        '  <!-- Right Corner Octagonal Domed Chattri (from Main-Gate.jpg) -->',
        '  <g class="sk-chattri-right">',
        '    <!-- Columns -->',
        '    <line x1="504" y1="244" x2="504" y2="204" />',
        '    <line x1="514" y1="244" x2="514" y2="204" />',
        '    <line x1="526" y1="244" x2="526" y2="204" />',
        '    <line x1="536" y1="244" x2="536" y2="204" />',
        '    <path d="M 504 212 Q 509 205 514 212 M 514 212 Q 520 205 526 212 M 526 212 Q 531 205 536 212" />',
        '    <!-- Chhajja (Eaves) -->',
        '    <path d="M 498 204 Q 520 196 542 204" stroke-width="1.4" />',
        '    <!-- Fluted Rajput Dome Cap -->',
        '    <path d="M 502 204 Q 520 170 538 204" stroke-width="1.3" />',
        '    <path d="M 511 204 Q 520 174 529 204" stroke-width="0.8" />',
        '    <path d="M 520 170 L 520 156" />',
        '    <circle cx="520" cy="155" r="1.4" fill="currentColor" />',
        '    <!-- Royal Pennant Flag (Gentle Wind Flutter) -->',
        '    <path class="sk-flag" d="M 520 156 Q 532 160 544 156 Q 532 164 520 168 Z" fill="rgba(215,180,106,0.3)" />',
        '  </g>',
        '</g>'
    ]
    parts.extend(palace)

    # 4. THE ROYAL CEREMONIAL ELEPHANT (Haathi with raised trunk in salutation)
    # Left side: x=35 to 225, y=265 to 405
    elephant = [
        '<g class="sk-elephant">',
        '  <!-- Body Contours & Noble Head -->',
        '  <!-- Back, Hump & Forehead -->',
        '  <path d="M 85 320 Q 110 276 150 282 Q 172 286 186 270 Q 198 260 204 274" stroke-width="1.3" />',
        '  <!-- Serene Eye & Forehead Plate (Mathabandi) -->',
        '  <path d="M 188 280 Q 192 278 196 280" stroke-width="1.0" />',
        '  <circle cx="192" cy="281" r="1.1" fill="currentColor" />',
        '  <!-- Royal Jewel Headgear / Mathabandi -->',
        '  <path d="M 178 274 Q 192 266 202 276" stroke-width="0.85" stroke-dasharray="2,2" />',
        '  <circle cx="192" cy="272" r="1.6" fill="currentColor" />',
        '  <path d="M 192 274 L 192 278" />',
        '',
        '  <!-- Large Royal Ear with Gold Trim Tassel -->',
        '  <path d="M 170 282 Q 152 292 154 330 Q 166 348 178 328 Z" stroke-width="1.15" />',
        '  <path d="M 166 295 Q 160 315 166 325" stroke-width="0.75" />',
        '  <path d="M 160 340 L 158 348" stroke-width="0.9" /><circle cx="158" cy="349" r="1.2" fill="currentColor" />',
        '',
        '  <!-- Auspicious Upraised Saluting Trunk (Gaja-vandana) -->',
        '  <path d="M 204 274 Q 218 300 214 340 Q 210 370 200 380 Q 192 386 188 376 Q 188 360 200 326 Q 206 300 194 290" stroke-width="1.35" />',
        '  <!-- Sacred Lotus bud held at trunk tip -->',
        '  <path d="M 188 376 Q 184 372 182 376 Q 185 382 188 376 Z" fill="rgba(215,180,106,0.5)" />',
        '  <!-- Ivory Gleaming Tusk -->',
        '  <path d="M 195 306 Q 214 316 224 300 Q 210 306 193 312 Z" stroke-width="1.1" fill="rgba(255,255,255,0.7)" />',
        '',
        '  <!-- Stately Legs with Carved Toenails -->',
        '  <!-- Foreleg Front (Planted Firm) -->',
        '  <path d="M 175 342 L 175 405 L 195 405 L 195 338" stroke-width="1.3" />',
        '  <path d="M 178 405 Q 180 400 182 405 M 184 405 Q 186 400 188 405 M 190 405 Q 192 400 194 405" stroke-width="0.8" />',
        '  <!-- Foreleg Back -->',
        '  <path d="M 160 348 L 156 405 L 170 405 L 172 345" stroke-width="1.0" opacity="0.85" />',
        '  <!-- Underbelly Contour -->',
        '  <path d="M 152 352 Q 130 358 114 348" stroke-width="1.1" />',
        '  <!-- Hind Leg Front -->',
        '  <path d="M 114 348 L 114 405 L 134 405 L 138 340" stroke-width="1.3" />',
        '  <path d="M 118 405 Q 120 400 122 405 M 124 405 Q 126 400 128 405 M 130 405 Q 132 400 134 405" stroke-width="0.8" />',
        '  <!-- Hind Leg Back -->',
        '  <path d="M 94 336 L 94 405 L 108 405 L 112 342" stroke-width="1.0" opacity="0.85" />',
        '  <!-- Tail with brush tuft -->',
        '  <path d="M 85 320 Q 80 355 82 380 Q 85 388 81 392" stroke-width="1.0" />',
        '',
        '  <!-- Royal Caparison: The Ceremonial Jhool (Embroidered Saddle Cloth) -->',
        '  <path d="M 104 300 Q 136 295 168 300 L 170 350 Q 136 356 102 350 Z" stroke-width="1.25" fill="rgba(215,180,106,0.12)" />',
        '  <!-- Diamond Lattice Gold Embroidery -->',
        '  <path d="M 112 308 L 162 344 M 124 304 L 168 334 M 138 302 L 169 322 M 106 322 L 140 352 M 158 308 L 108 344 M 146 304 L 104 334 M 132 302 L 103 322 M 164 322 L 130 352" stroke-width="0.65" opacity="0.75" />',
        '  <!-- Ornate Scallop Border with Hanging Bell Tassels -->',
        '  <path d="M 102 350 Q 107 356 112 350 Q 117 356 122 350 Q 127 356 132 350 Q 137 356 142 350 Q 147 356 152 350 Q 157 356 162 350 Q 167 356 170 350" stroke-width="0.9" />',
        '  <!-- Ghungroo Bell Necklace around neck -->',
        '  <path d="M 180 315 Q 168 332 158 340" stroke-width="1.1" stroke-dasharray="3,3" />',
        '</g>'
    ]
    parts.extend(elephant)

    # 5. THE RUNNING MARWARI HORSES (Lyre inward ears, flowing mane, spirited gallop)
    # Right side: x=555 to 765, y=260 to 405
    horses = [
        '<g class="sk-horses">',
        '  <!-- Companion Marwari Horse (Behind, trotting gracefully with arched neck) -->',
        '  <g class="sk-horse-bg" opacity="0.65">',
        '    <!-- Inward curving ears -->',
        '    <path d="M 648 290 Q 646 276 650 272 Q 652 278 650 290" />',
        '    <path d="M 653 290 Q 655 276 651 272 Q 656 279 655 290" />',
        '    <!-- Arched neck & head -->',
        '    <path d="M 618 325 Q 632 300 648 290 Q 662 296 670 306 Q 666 312 658 312 Q 648 318 638 318" />',
        '    <!-- Flowing mane -->',
        '    <path d="M 642 294 Q 634 302 626 312 M 636 302 Q 628 310 620 320" />',
        '    <!-- Body & Legs in stride -->',
        '    <path d="M 618 325 Q 598 330 580 325 L 574 365 M 636 335 L 646 385" stroke-width="0.9" />',
        '  </g>',
        '',
        '  <!-- Lead Royal Marwari Stallion (Full spirited running gallop in foreground!) -->',
        '  <g class="sk-horse-lead">',
        '    <!-- Distinctive Inward-Curving Lyre Ears of the Marwari Breed -->',
        '    <path d="M 698 284 Q 694 266 699 260 Q 702 268 700 284" stroke-width="1.25" fill="rgba(215,180,106,0.2)" />',
        '    <path d="M 703 284 Q 706 266 701 260 Q 707 269 705 284" stroke-width="1.25" fill="rgba(215,180,106,0.2)" />',
        '    <line x1="699" y1="260" x2="701" y2="260" stroke-width="0.8" />',
        '',
        '    <!-- Arched Muscular Neck & Proud Head Profile -->',
        '    <path d="M 654 322 Q 672 294 698 284" stroke-width="1.4" />',
        '    <path d="M 700 284 Q 718 290 730 305 Q 726 312 718 310 Q 706 316 690 312" stroke-width="1.35" />',
        '    <!-- Muzzle, Flaired Nostril & Spirited Eye -->',
        '    <path d="M 724 306 Q 721 310 717 307" stroke-width="1.1" />',
        '    <path d="M 706 292 Q 711 289 713 294" stroke-width="1.1" />',
        '    <circle cx="709.5" cy="292.5" r="1.1" fill="currentColor" />',
        '',
        '    <!-- Flowing Wind-blown Mane streaming behind in gallop -->',
        '    <path d="M 692 288 Q 676 296 662 308" stroke-width="1.2" />',
        '    <path d="M 682 296 Q 666 308 654 320" stroke-width="1.1" />',
        '    <path d="M 672 306 Q 658 318 648 330" stroke-width="1.0" />',
        '    <path d="M 688 290 Q 670 292 658 298" stroke-width="0.9" opacity="0.85" />',
        '',
        '    <!-- Deep Muscular Chest & Stretched Forelegs in Mid-Gallop! -->',
        '    <path d="M 690 312 Q 686 338 674 348" stroke-width="1.35" />',
        '    <!-- Leading Foreleg reaching forward -->',
        '    <path d="M 678 348 L 706 376 L 730 402 L 725 405 L 712 403 L 690 376 L 668 354" stroke-width="1.3" />',
        '    <!-- Trailing Foreleg tucked forward in gallop stride -->',
        '    <path d="M 668 348 Q 656 368 662 384 Q 668 398 660 405" stroke-width="1.15" />',
        '',
        '    <!-- Back, Supple Flank & Powerful Hindquarters -->',
        '    <path d="M 654 322 Q 632 326 610 320" stroke-width="1.35" />',
        '    <path d="M 610 320 Q 586 324 580 346" stroke-width="1.4" />',
        '    <path d="M 664 354 Q 634 362 612 350" stroke-width="1.1" />',
        '',
        '    <!-- Powerful Driving Hind Legs pushing off the ground -->',
        '    <!-- Primary Driving Hind Leg extended back in stride -->',
        '    <path d="M 584 346 L 570 374 L 552 396 L 558 400 L 570 392 L 594 366" stroke-width="1.3" />',
        '    <!-- Companion Hind Leg driving forward -->',
        '    <path d="M 598 350 L 588 382 L 582 405 L 590 405 L 602 380" stroke-width="1.1" />',
        '',
        '    <!-- Majestic Flowing Arched Tail Streaming in the Wind -->',
        '    <path d="M 580 328 Q 550 324 538 348 Q 552 366 564 354 Q 550 338 580 334" stroke-width="1.3" fill="rgba(215,180,106,0.15)" />',
        '    <path d="M 570 335 Q 548 335 542 355" stroke-width="0.85" />',
        '',
        '    <!-- Royal Marwari Bridle & Hemar-band (Tasselled Chest Harness) -->',
        '    <path d="M 700 286 L 712 308 M 703 298 L 720 306" stroke-width="0.8" stroke-dasharray="2,2" />',
        '    <path d="M 686 332 Q 676 342 668 346" stroke-width="0.9" />',
        '    <circle cx="678" cy="340" r="1.3" fill="currentColor" />',
        '  </g>',
        '</g>'
    ]
    parts.extend(horses)

    # 6. FOREGROUND COURTYARD, STEPWELL WATER POOL & LOTUS
    ground = [
        '<g class="sk-ground">',
        '  <!-- Paved Courtyard Lines -->',
        '  <line x1="30" y1="405" x2="750" y2="405" stroke-width="1.3" />',
        '  <line x1="60" y1="413" x2="720" y2="413" stroke-width="0.8" stroke-dasharray="5,4" />',
        '  <!-- Stepwell Water Pool & Blooming Sacred Lotus (Amber Taal) -->',
        '  <path d="M 330 405 Q 390 414 450 405" stroke-width="1.2" />',
        '  <path d="M 350 412 Q 390 419 430 412" stroke-width="0.85" />',
        '  <!-- Sacred Lotus Flower blooming on water -->',
        '  <path d="M 390 398 Q 384 406 380 412 Q 390 410 390 404 Q 390 410 400 412 Q 396 406 390 398 Z" fill="rgba(215,180,106,0.3)" stroke-width="1.1" />',
        '  <path d="M 380 406 Q 372 411 370 415 Q 380 414 382 410" stroke-width="0.9" />',
        '  <path d="M 400 406 Q 408 411 410 415 Q 400 414 398 410" stroke-width="0.9" />',
        '</g>',
        '</svg>'
    ]
    parts.extend(ground)

    svg_content = "\n".join(parts)
    # Validate XML
    ET.fromstring(svg_content)
    return svg_content

if __name__ == '__main__':
    svg = generate_sketch_svg()
    print(f"Generated SVG successfully, length: {len(svg)} chars")
    with open("assets/img/palace-sketch.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Saved to assets/img/palace-sketch.svg")
