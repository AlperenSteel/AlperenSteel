import json
from datetime import datetime

# GitHub'ın kullandığı yeşil ton paleti (level 0 = katkı yok, level 4 = en yoğun)
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

CELL_SIZE = 11      # her kutucuğun kenar uzunluğu
CELL_GAP = 3         # kutucuklar arası boşluk
STEP = CELL_SIZE + CELL_GAP

def load_days():
    with open("data/contributions.json") as f:
        return json.load(f)

def group_by_week(days):
    # ilk günün haftanın hangi günü olduğunu bul (Pazartesi=0 ... Pazar=6)
    weeks = []
    current_week = []
    for day in days:
        date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
        weekday = date_obj.weekday()  # Pazartesi=0
        if not current_week and weekday != 0 and weeks == [] and current_week == []:
            pass
        current_week.append(day)
        if weekday == 6 or day == days[-1]:  # Pazar günü haftayı kapat
            weeks.append(current_week)
            current_week = []
    return weeks

def render_svg(weeks):
    num_weeks = len(weeks)
    width = num_weeks * STEP + 20
    height = 7 * STEP + 20

    rects = []
    delay_index = 0
    for week_index, week in enumerate(weeks):
        for day in week:
            date_obj = datetime.strptime(day["date"], "%Y-%m-%d")
            weekday = date_obj.weekday()  # 0=Pazartesi
            x = 10 + week_index * STEP
            y = 10 + weekday * STEP
            color = COLORS[day["level"]]
            delay = delay_index * 0.015  # her kutucukta artan gecikme
            rects.append(
                f'<rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                f'rx="2" fill="{color}" class="day-box" '
                f'style="animation-delay:{delay:.3f}s" />'
            )
            delay_index += 1

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .day-box {{
      opacity: 0;
      animation: reveal 0.4s ease-out forwards;
    }}
    @keyframes reveal {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to   {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
  <rect width="{width}" height="{height}" fill="#0d1117" />
  {"".join(rects)}
</svg>'''
    return svg

if __name__ == "__main__":
    days = load_days()
    weeks = group_by_week(days)
    svg = render_svg(weeks)
    with open("contrib-heatmap.svg", "w") as f:
        f.write(svg)
    print(f"{len(weeks)} hafta render edildi.")
    print("contrib-heatmap.svg yazıldı.")
