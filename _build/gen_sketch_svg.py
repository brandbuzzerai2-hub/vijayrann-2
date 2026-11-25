#!/usr/bin/env python3
"""Generate the SVG wrapper with progressive architectural drawing mask for palace-sketch.png."""
import xml.etree.ElementTree as ET

def get_sketch_svg(rel_prefix=""):
    img_href = f"{rel_prefix}assets/img/palace-sketch.png"
    svg = f'''<svg class="sk-svg" viewBox="0 0 1376 768" width="100%" height="auto" aria-label="Architectural engraving of The Vijayran Palace">
  <defs>
    <mask id="skHatchMask" maskUnits="userSpaceOnUse" x="0" y="0" width="1376" height="768">
      <!-- Black background hides everything initially -->
      <rect width="1376" height="768" fill="black" />
      <g stroke="white" stroke-linecap="round" stroke-linejoin="round" fill="none">
        <!-- 1. Foundation, courtyard & lotus pool (left-to-right base strokes) -->
        <path class="sk-p sk-p1" d="M 40 710 L 1336 710 M 70 735 L 1306 735 M 100 755 L 1276 755" stroke-width="50" />
        <path class="sk-p sk-p2" d="M 460 675 L 916 675 M 500 700 L 876 700 M 540 720 L 836 720" stroke-width="55" />

        <!-- 2. Central Rajput Gateway & Entrance Portal (vertical masonry strokes) -->
        <path class="sk-p sk-p3" d="M 610 670 L 610 420 M 688 670 L 688 380 M 766 670 L 766 420" stroke-width="70" />
        <path class="sk-p sk-p4" d="M 540 550 L 836 550 M 540 460 L 836 460 M 580 390 L 796 390" stroke-width="80" />

        <!-- 3. Royal Ceremonial Elephant (contour sweeps tracing head, tusk, jhool, legs) -->
        <path class="sk-p sk-p5" d="M 120 680 L 120 480 Q 150 420 230 420 Q 300 420 340 480 L 340 680" stroke-width="85" />
        <path class="sk-p sk-p6" d="M 220 540 L 400 500 Q 440 470 430 420 Q 420 370 390 360" stroke-width="75" />
        <path class="sk-p sk-p7" d="M 170 450 Q 240 480 320 450 Q 240 580 170 540 Z" stroke-width="60" />

        <!-- 4. Galloping Marwari Horses (dynamic leaping diagonal strokes) -->
        <path class="sk-p sk-p8" d="M 980 660 L 1150 520 L 1330 620" stroke-width="90" />
        <path class="sk-p sk-p9" d="M 1060 580 L 1180 460 L 1300 560" stroke-width="80" />
        <path class="sk-p sk-p10" d="M 1120 520 L 1240 430 L 1310 490" stroke-width="70" />

        <!-- 5. Left & Right Haveli Wings and Corner Chattris -->
        <path class="sk-p sk-p11" d="M 270 460 L 270 200 Q 310 150 350 200 L 350 460" stroke-width="75" />
        <path class="sk-p sk-p12" d="M 1026 460 L 1026 200 Q 1066 150 1106 200 L 1106 460" stroke-width="75" />

        <!-- 6. Upper Baradari Pavilion (rooftop 5 arches & vaulted roof) -->
        <path class="sk-p sk-p13" d="M 560 370 L 560 210 Q 688 150 816 210 L 816 370" stroke-width="85" />
        <path class="sk-p sk-p14" d="M 580 270 L 796 270 M 620 210 L 756 210" stroke-width="70" />

        <!-- 7. Distant Aravalli Hills & Sky birds -->
        <path class="sk-p sk-p15" d="M 20 450 Q 350 350 688 380 Q 1026 350 1356 450" stroke-width="65" />
        <path class="sk-p sk-p16" d="M 50 360 Q 350 300 688 330 Q 1026 300 1326 360" stroke-width="60" />

        <!-- 8. Royal Sun Crest: expanding circular burst -->
        <circle class="sk-p-sun" cx="475" cy="120" r="85" fill="white" stroke="none" />

        <!-- 9. Final unmask flood layer for 100% full opacity -->
        <rect class="sk-p-full" width="1376" height="768" fill="white" opacity="0" />
      </g>
    </mask>
  </defs>
  <!-- Architectural Line Engraving Image -->
  <image class="sk-img" href="{img_href}" width="1376" height="768" mask="url(#skHatchMask)" preserveAspectRatio="xMidYMid meet" />
</svg>'''
    ET.fromstring(svg)
    return svg

if __name__ == '__main__':
    svg = get_sketch_svg("")
    print("SVG generated and parsed successfully! Length:", len(svg))
