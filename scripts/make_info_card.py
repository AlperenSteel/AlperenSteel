def render_svg():
    lines = [
        ("Stack", "Java · Spring Boot · React · C · PostgreSQL"),
        ("Studying", "Computer Engineering"),
        ("Interests", "Piano, Travel"),
        ("Fun fact", "Built a custom RPG system for friends"),
    ]

    line_height = 34
    top_padding = 70
    width = 560
    height = top_padding + line_height * len(lines) + 30

    rows = []
    for i, (label, value) in enumerate(lines):
        y = top_padding + i * line_height
        delay = 0.3 + i * 0.25
        rows.append(f'''
    <text x="24" y="{y}" class="label" style="animation-delay:{delay:.2f}s">{label}</text>
    <text x="150" y="{y}" class="value" style="animation-delay:{delay:.2f}s">{value}</text>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="monospace">
  <style>
    .titlebar {{ fill: #21262d; }}
    .dot {{ opacity: 0.8; }}
    .label {{ fill: #39d353; font-size: 15px; font-weight: bold; opacity: 0; animation: fadein 0.5s ease-out forwards; }}
    .value {{ fill: #c9d1d9; font-size: 15px; opacity: 0; animation: fadein 0.5s ease-out forwards; }}
    @keyframes fadein {{
      from {{ opacity: 0; transform: translateX(-6px); }}
      to   {{ opacity: 1; transform: translateX(0); }}
    }}
  </style>

  <rect width="{width}" height="{height}" rx="8" fill="#0d1117" stroke="#30363d" />
  <rect width="{width}" height="34" rx="8" class="titlebar" />
  <rect y="20" width="{width}" height="14" class="titlebar" />
  <circle cx="20" cy="17" r="6" fill="#ff5f56" class="dot" />
  <circle cx="40" cy="17" r="6" fill="#ffbd2e" class="dot" />
  <circle cx="60" cy="17" r="6" fill="#27c93f" class="dot" />
  <text x="{width/2}" y="22" fill="#8b949e" font-size="13" text-anchor="middle">alperen@github: ~</text>
  {"".join(rows)}
</svg>'''
    return svg

if __name__ == "__main__":
    svg = render_svg()
    with open("info-card.svg", "w") as f:
        f.write(svg)
    print("info-card.svg yazıldı.")
