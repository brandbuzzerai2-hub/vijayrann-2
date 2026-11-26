# -*- coding: utf-8 -*-
"""
Generates the Royal Pictorial Cartographic Map for The Vijayran Palace.
Embeds the museum-grade antique watercolor pictorial map artwork (map-jaipur-royal.jpg)
with the mathematical spline of the royal highway, animated Marwari horse in motion,
interactive 3D location beacons, and floating royal vignette cards.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Mathematically smooth SVG bezier path following the painted golden highway
SPLINE_D = (
    "M 392.0 915.0 "
    "C 398.3 909.2, 417.8 892.5, 430.0 880.0 "
    "C 442.2 867.5, 457.5 856.7, 465.0 840.0 "
    "C 472.5 823.3, 481.7 800.8, 475.0 780.0 "
    "C 468.3 759.2, 445.0 737.5, 425.0 715.0 "
    "C 405.0 692.5, 380.8 669.2, 355.0 645.0 "
    "C 329.2 620.8, 288.3 589.2, 270.0 570.0 "
    "C 251.7 550.8, 244.2 540.0, 245.0 530.0 "
    "C 245.8 520.0, 258.3 517.5, 275.0 510.0 "
    "C 291.7 502.5, 320.0 495.8, 345.0 485.0 "
    "C 370.0 474.2, 405.0 456.7, 425.0 445.0 "
    "C 445.0 433.3, 472.5 422.5, 465.0 415.0 "
    "C 457.5 407.5, 405.0 406.7, 380.0 400.0 "
    "C 355.0 393.3, 322.5 384.2, 315.0 375.0 "
    "C 307.5 365.8, 322.5 351.7, 335.0 345.0 "
    "C 347.5 338.3, 369.2 335.0, 390.0 335.0 "
    "C 410.8 335.0, 435.8 340.0, 460.0 345.0 "
    "C 484.2 350.0, 513.3 360.8, 535.0 365.0 "
    "C 556.7 369.2, 575.0 365.8, 590.0 370.0 "
    "C 605.0 374.2, 617.5 393.3, 625.0 390.0 "
    "C 632.5 386.7, 637.5 360.0, 635.0 350.0 "
    "C 632.5 340.0, 609.2 337.5, 610.0 330.0 "
    "C 610.8 322.5, 624.2 308.3, 640.0 305.0 "
    "C 655.8 301.7, 682.5 315.0, 705.0 310.0 "
    "C 727.5 305.0, 763.3 280.8, 775.0 275.0"
)

def get_map_svg(prefix=""):
    img_path = f"{prefix}assets/img/map-jaipur-royal.jpg"
    
    return f"""<svg id="royalExpeditionMap" class="map-ill" viewBox="0 0 1024 1024" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Royal Heritage Territory Map with 3D Motion Trail">
  <defs>
    <clipPath id="royalMapClip">
      <rect x="0" y="0" width="1024" height="1024" rx="14" />
    </clipPath>
    <filter id="horseBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" />
    </filter>
    <filter id="beaconGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="glow" />
      <feMerge>
        <feMergeNode in="glow" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>
    <radialGradient id="goldPulseGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#cca456" stop-opacity="0.8"/>
      <stop offset="60%" stop-color="#cca456" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#cca456" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <g clip-path="url(#royalMapClip)">
    <!-- Base Luxury Watercolor Heritage Map Artwork -->
    <image href="{img_path}" width="1024" height="1024" preserveAspectRatio="xMidYMid meet" />

    <!-- Mathematical Golden Royal Highway Spline (Invisible guide or subtle golden shimmer) -->
    <path id="royalHighwayPath" d="{SPLINE_D}" fill="none" stroke="rgba(215, 180, 106, 0.45)" stroke-width="2.5" stroke-dasharray="6,4" stroke-linecap="round"/>
    
    <!-- Active Travel Progress Trail (Dynamically drawn as horse gallops) -->
    <path id="royalTravelTrail" d="{SPLINE_D}" fill="none" stroke="#d7b46a" stroke-width="4.5" stroke-linecap="round" stroke-dasharray="1525" stroke-dashoffset="1525"/>

    <!-- 5 Royal Milestone Beacons along the Princely Route -->
    <!-- 1. Jaipur Airport (392, 915) -->
    <g class="map-stop-beacon" id="stopBeacon0" transform="translate(392, 915)" data-stop="0" cursor="pointer">
      <circle class="beacon-pulse" r="16" fill="url(#goldPulseGrad)"/>
      <circle class="beacon-ring" r="8" fill="#fcfaf4" stroke="#cca456" stroke-width="2"/>
      <circle class="beacon-core" r="3.5" fill="#8d1711"/>
    </g>

    <!-- 2. Hawa Mahal & Pink City (475, 780) -->
    <g class="map-stop-beacon" id="stopBeacon1" transform="translate(475, 780)" data-stop="1" cursor="pointer">
      <circle class="beacon-pulse" r="18" fill="url(#goldPulseGrad)"/>
      <circle class="beacon-ring" r="9" fill="#fcfaf4" stroke="#d47d6a" stroke-width="2.2"/>
      <circle class="beacon-core" r="4" fill="#8d1711"/>
    </g>

    <!-- 3. Jal Mahal (245, 530) -->
    <g class="map-stop-beacon" id="stopBeacon2" transform="translate(245, 530)" data-stop="2" cursor="pointer">
      <circle class="beacon-pulse" r="18" fill="url(#goldPulseGrad)"/>
      <circle class="beacon-ring" r="9" fill="#fcfaf4" stroke="#5d968b" stroke-width="2.2"/>
      <circle class="beacon-core" r="4" fill="#1b4d45"/>
    </g>

    <!-- 4. Amber Fort (315, 375) -->
    <g class="map-stop-beacon" id="stopBeacon3" transform="translate(315, 375)" data-stop="3" cursor="pointer">
      <circle class="beacon-pulse" r="20" fill="url(#goldPulseGrad)"/>
      <circle class="beacon-ring" r="9" fill="#fcfaf4" stroke="#cca456" stroke-width="2.2"/>
      <circle class="beacon-core" r="4" fill="#8d1711"/>
    </g>

    <!-- 5. The Vijayran Palace · Kukas (775, 275) -->
    <g class="map-stop-beacon" id="stopBeacon4" transform="translate(775, 275)" data-stop="4" cursor="pointer">
      <circle class="beacon-pulse palace-pulse" r="26" fill="url(#goldPulseGrad)"/>
      <circle class="beacon-ring" r="12" fill="#8d1711" stroke="#d7b46a" stroke-width="2.5"/>
      <circle class="beacon-core" r="5" fill="#fcfaf4"/>
    </g>

    <!-- Golden Dust Particle Container -->
    <g id="horseDustParticles"></g>

    <!-- Royal Marwari Stallion in 3D Gallop Motion -->
    <g id="royalHorseRig" class="royal-horse-rig" transform="translate(392, 915)">
      <!-- Ground Shadow that scales with gallop rhythm -->
      <ellipse class="horse-shadow" cx="0" cy="18" rx="20" ry="6.5" fill="rgba(32, 20, 10, 0.4)" filter="url(#horseBlur)" />
      
      <!-- Stallion Body Stride & Gait Group -->
      <g class="horse-stride">
        <!-- Far Hind Leg -->
        <g class="horse-leg hind-far">
          <path d="M -11 3 Q -20 12 -16 21 L -20 25" stroke="#3b2b20" stroke-width="3" stroke-linecap="round" fill="none"/>
          <polygon points="-22,25 -18,25 -19,27 -23,27" fill="#d7b46a"/>
        </g>

        <!-- Far Foreleg -->
        <g class="horse-leg fore-far">
          <path d="M 11 5 Q 20 13 16 21 L 20 25" stroke="#3b2b20" stroke-width="2.8" stroke-linecap="round" fill="none"/>
          <polygon points="18,25 22,25 23,27 19,27" fill="#d7b46a"/>
        </g>

        <!-- Muscular Bay Stallion Torso -->
        <path class="horse-torso" d="M -16 6 C -18 -2, -10 -6, 2 -5 C 12 -5, 18 -1, 19 6 C 18 12, 10 14, -2 13 C -10 13, -15 12, -16 6 Z" fill="#2e1f16"/>

        <!-- Embroidered Rajputana Ceremonial Jhool (Saddle Blanket) -->
        <path d="M -8 -4 L 8 -4 L 10 7 Q 0 11 -10 7 Z" fill="#8d1711" stroke="#d7b46a" stroke-width="1.2"/>
        <line x1="-6" y1="1" x2="6" y2="1" stroke="#d7b46a" stroke-width="0.8" stroke-dasharray="1.5,1.5"/>
        <circle cx="0" cy="3" r="1.6" fill="#d7b46a"/>

        <!-- Arched Marwari Neck & Regal Head -->
        <g class="horse-neck-head">
          <path d="M 14 0 C 17 -8, 22 -14, 28 -17 C 29 -14, 27 -6, 22 5 Z" fill="#2e1f16"/>
          <!-- Mane flowing -->
          <path class="horse-mane" d="M 16 -3 Q 13 -7 18 -12 Q 22 -16 26 -18 Q 23 -11 20 -4 Z" fill="#140c08"/>
          <!-- Head -->
          <path d="M 27 -17 C 32 -18, 36 -15, 38 -12 C 37 -9, 33 -8, 30 -9 C 28 -7, 26 -12, 27 -17 Z" fill="#2e1f16"/>
          <!-- Curved Marwari Inward Ears -->
          <path d="M 28 -18 C 29 -22, 32 -23, 31 -20 C 30 -19, 29 -18, 28 -18 Z" fill="#140c08"/>
          <path d="M 26 -17 C 27 -21, 30 -22, 29 -19 C 28 -18, 27 -17, 26 -17 Z" fill="#140c08"/>
          <!-- Gold Bridle & Kalgi Feather Plume -->
          <line x1="28" y1="-17" x2="36" y2="-12" stroke="#d7b46a" stroke-width="1"/>
          <circle cx="36" cy="-12" r="1" fill="#cca456"/>
          <path d="M 29 -20 Q 34 -27 32 -25 Q 28 -24 29 -20" stroke="#fcfaf4" stroke-width="1.3" fill="none"/>
        </g>

        <!-- Near Hind Leg -->
        <g class="horse-leg hind-near">
          <path d="M -10 5 Q -16 15 -12 23 L -15 27" stroke="#1d130d" stroke-width="3.2" stroke-linecap="round" fill="none"/>
          <polygon points="-17,27 -13,27 -14,29 -18,29" fill="#cca456"/>
        </g>

        <!-- Near Foreleg -->
        <g class="horse-leg fore-near">
          <path d="M 13 6 Q 19 15 23 23 L 25 27" stroke="#1d130d" stroke-width="3.2" stroke-linecap="round" fill="none"/>
          <polygon points="23,27 27,27 28,29 24,29" fill="#cca456"/>
        </g>

        <!-- Dynamic Flying Tail -->
        <path class="horse-tail" d="M -16 3 Q -26 4 -32 10 Q -28 7 -22 8 Q -18 8 -16 6 Z" fill="#140c08"/>
      </g>
    </g>
  </g>
</svg>"""

if __name__ == "__main__":
    out_svg = os.path.join(ROOT, "assets", "img", "map-jaipur.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(get_map_svg())
    print("Wrote map-jaipur.svg successfully!")
