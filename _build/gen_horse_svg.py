# -*- coding: utf-8 -*-
"""
Design a regal Marwari horse with royal saddlery, galloping animation, and 3D shadow.
"""

def get_marwari_horse_svg():
    return '''<g id="royalHorseRig" class="royal-horse-rig" transform="translate(0,0)">
  <!-- 3D Ground Shadow that scales during gallop stride -->
  <ellipse class="horse-shadow" cx="0" cy="18" rx="22" ry="7" fill="rgba(30, 20, 10, 0.35)" filter="url(#horseBlur)" />
  
  <!-- Galloping Marwari Stallion Body Group -->
  <g class="horse-stride">
    <!-- Hind Leg Far (animated stride) -->
    <g class="leg hind-far">
      <path d="M -12 2 Q -22 10 -18 20 L -22 24" stroke="#4a3b32" stroke-width="3" stroke-linecap="round" fill="none"/>
      <!-- Hoof Far -->
      <polygon points="-24,24 -20,24 -21,26 -25,26" fill="#cca456"/>
    </g>

    <!-- Foreleg Far (animated stride) -->
    <g class="leg fore-far">
      <path d="M 12 4 Q 22 12 18 20 L 22 24" stroke="#4a3b32" stroke-width="2.8" stroke-linecap="round" fill="none"/>
      <!-- Hoof Far -->
      <polygon points="20,24 24,24 25,26 21,26" fill="#cca456"/>
    </g>

    <!-- Main Torso & Musculature (Dark Chestnut / Bay Royal Stallion) -->
    <path class="horse-body" d="M -16 6 C -18 -2, -10 -6, 2 -5 C 12 -5, 18 -1, 19 6 C 18 12, 10 14, -2 13 C -10 13, -15 12, -16 6 Z" fill="#3b2b20"/>

    <!-- Royal Rajputana Ceremonial Jhool (Embroidered Saddle Cloth) -->
    <path d="M -8 -4 L 8 -4 L 10 7 Q 0 11 -10 7 Z" fill="#8d1711" stroke="#d7b46a" stroke-width="1.2"/>
    <path d="M -6 1 L 6 1" stroke="#d7b46a" stroke-width="0.8" stroke-dasharray="1.5,1.5"/>
    <!-- Gold Medallion on Jhool -->
    <circle cx="0" cy="3" r="1.8" fill="#d7b46a"/>

    <!-- Arched Neck & Marwari Head -->
    <g class="horse-head-group">
      <!-- Arched Muscular Neck -->
      <path d="M 14 0 C 17 -8, 22 -14, 28 -17 C 29 -14, 27 -6, 22 5 Z" fill="#3b2b20"/>
      <!-- Flowing Dark Mane -->
      <path class="horse-mane" d="M 16 -3 Q 13 -7 18 -12 Q 22 -16 26 -18 Q 23 -11 20 -4 Z" fill="#20150e"/>
      <!-- Head -->
      <path d="M 27 -17 C 32 -18, 36 -15, 38 -12 C 37 -9, 33 -8, 30 -9 C 28 -7, 26 -12, 27 -17 Z" fill="#3b2b20"/>
      <!-- Marwari Lyre-shaped Curving Ears (Signature breed trait) -->
      <path d="M 28 -18 C 29 -22, 32 -23, 31 -20 C 30 -19, 29 -18, 28 -18 Z" fill="#20150e"/>
      <path d="M 26 -17 C 27 -21, 30 -22, 29 -19 C 28 -18, 27 -17, 26 -17 Z" fill="#20150e"/>
      <!-- Gold Royal Bridle & Headstall -->
      <line x1="28" y1="-17" x2="36" y2="-12" stroke="#d7b46a" stroke-width="0.9"/>
      <circle cx="36" cy="-12" r="1" fill="#cca456"/>
      <!-- Royal Plume / Kalgi -->
      <path d="M 29 -20 Q 33 -26 31 -24 Q 28 -23 29 -20" stroke="#fbf9f6" stroke-width="1.2" fill="none"/>
    </g>

    <!-- Hind Leg Near -->
    <g class="leg hind-near">
      <path d="M -10 4 Q -16 14 -12 22 L -14 26" stroke="#2a1e16" stroke-width="3.2" stroke-linecap="round" fill="none"/>
      <!-- Hoof Near -->
      <polygon points="-16,26 -12,26 -13,28 -17,28" fill="#cca456"/>
    </g>

    <!-- Foreleg Near -->
    <g class="leg fore-near">
      <path d="M 14 6 Q 20 14 24 22 L 26 26" stroke="#2a1e16" stroke-width="3" stroke-linecap="round" fill="none"/>
      <!-- Hoof Near -->
      <polygon points="24,26 28,26 29,28 25,28" fill="#cca456"/>
    </g>

    <!-- Flowing Royal Tail (animated swish) -->
    <path class="horse-tail" d="M -16 3 Q -26 4 -32 10 Q -28 7 -22 8 Q -18 8 -16 6 Z" fill="#1b120c"/>
  </g>
</g>'''

print("Marwari horse SVG defined successfully")
