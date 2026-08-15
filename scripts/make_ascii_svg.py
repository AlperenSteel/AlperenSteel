from PIL import Image

RAMP = " .`:-=+*cs#%@"  # açık (boşluk) -> koyu (yoğun)

COLS = 70
ROWS = 40
CHAR_W = 6.2
CHAR_H = 11

def image_to_ascii_rows(path):
    img = Image.open(path).convert("L")
    img = img.resize((COLS, ROWS))
    pixels = list(img.getdata())

    rows = []
    for r in range(ROWS):
        row_chars = []
        for c in range(COLS):
            brightness = pixels[r * COLS + c]  # 0=siyah, 255=beyaz
            idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            row_chars.append(RAMP[idx])
        rows.append("".join(row_chars))
    return rows

def escape_xml(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render_svg(rows):
    width = COLS * CHAR_W + 20
    height = ROWS * CHAR_H + 20

    row_elements = []
    for i, row in enumerate(rows):
        y = 15 + i * CHAR_H
        delay = i * 0.035
        safe_row = escape_xml(row)
        row_elements.append(f'''
    <g class="ascii-row" style="animation-delay:{delay:.3f}s">
      <clipPath id="clip{i}">
        <rect x="0" y="{y - CHAR_H + 2}" width="0" height="{CHAR_H}" class="wipe-rect" style="animation-delay:{delay:.3f}s" />
      </clipPath>
      <text x="10" y="{y}" clip-path="url(#clip{i})">{safe_row}</text>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="monospace" font-size="{CHAR_H - 1}">
  <style>
    text {{ fill: #c9d1d9; white-space: pre; }}
    .wipe-rect {{
      animation: wipe 0.5s steps(30) forwards;
    }}
    @keyframes wipe {{
      from {{ width: 0; }}
      to   {{ width: {width}px; }}
    }}
  </style>
  <rect width="{width}" height="{height}" fill="#0d1117" />
  {"".join(row_elements)}
</svg>'''
    return svg

if __name__ == "__main__":
    rows = image_to_ascii_rows("source-prepped.png")
    svg = render_svg(rows)
    with open("avi-ascii.svg", "w") as f:
        f.write(svg)
    print(f"{len(rows)} satır render edildi.")
    print("avi-ascii.svg yazıldı.")
