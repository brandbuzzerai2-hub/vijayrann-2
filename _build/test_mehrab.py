#!/usr/bin/env python3
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 480" width="960" height="480" style="background:#F6F3EF;">
  <defs>
    <!-- Variation 1: 5-Cusp Rajput Mehrab Arch (Mughal-Rajput) -->
    <clipPath id="m1" clipPathUnits="objectBoundingBox">
      <path d="M 0 1 L 1 1 L 1 0.40 C 1 0.32, 0.93 0.26, 0.86 0.26 C 0.86 0.19, 0.77 0.13, 0.68 0.13 C 0.68 0.07, 0.58 0.02, 0.50 0.00 C 0.42 0.02, 0.32 0.07, 0.32 0.13 C 0.23 0.13, 0.14 0.19, 0.14 0.26 C 0.07 0.26, 0 0.32, 0 0.40 Z" />
    </clipPath>
    <!-- Variation 2: Classical Pointed Mehrab Arch (Ogee / Jharoka alcove) -->
    <clipPath id="m2" clipPathUnits="objectBoundingBox">
      <path d="M 0 1 L 1 1 L 1 0.45 C 1 0.22, 0.76 0.14, 0.50 0.00 C 0.24 0.14, 0 0.22, 0 0.45 Z" />
    </clipPath>
    <!-- Variation 3: Trefoil Cusped Mehrab with Scalloped Shoulders -->
    <clipPath id="m3" clipPathUnits="objectBoundingBox">
      <path d="M 0 1 L 1 1 L 1 0.42 C 1 0.32, 0.90 0.24, 0.80 0.24 C 0.80 0.15, 0.66 0.08, 0.50 0.00 C 0.34 0.08, 0.20 0.15, 0.20 0.24 C 0.10 0.24, 0 0.32, 0 0.42 Z" />
    </clipPath>
  </defs>

  <g transform="translate(60, 40)">
    <rect width="240" height="340" fill="#d7b46a" clip-path="url(#m1)" />
    <image href="../media/wp-content/uploads/2021/06/g10.jpg" x="0" y="0" width="240" height="340" preserveAspectRatio="xMidYMid slice" clip-path="url(#m1)" />
    <text x="120" y="375" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#333">1. 5-Cusp Rajput Mehrab</text>
  </g>

  <g transform="translate(360, 40)">
    <rect width="240" height="340" fill="#d7b46a" clip-path="url(#m2)" />
    <image href="../media/wp-content/uploads/2021/06/g10.jpg" x="0" y="0" width="240" height="340" preserveAspectRatio="xMidYMid slice" clip-path="url(#m2)" />
    <text x="120" y="375" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#333">2. Classic Pointed Mehrab</text>
  </g>

  <g transform="translate(660, 40)">
    <rect width="240" height="340" fill="#d7b46a" clip-path="url(#m3)" />
    <image href="../media/wp-content/uploads/2021/06/g10.jpg" x="0" y="0" width="240" height="340" preserveAspectRatio="xMidYMid slice" clip-path="url(#m3)" />
    <text x="120" y="375" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="14" fill="#333">3. Trefoil Cusped Mehrab</text>
  </g>
</svg>'''
with open('assets/img/test_mehrab.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print("Saved assets/img/test_mehrab.svg")
