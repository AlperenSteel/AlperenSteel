import json
import requests
from bs4 import BeautifulSoup

USERNAME = "AlperenSteel"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_contributions():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    day_cells = soup.find_all("td", class_="ContributionCalendar-day")

    days = []
    for cell in day_cells:
        date = cell.get("data-date")
        level = cell.get("data-level")
        if date is None or level is None:
            continue
        days.append({"date": date, "level": int(level)})

    days.sort(key=lambda d: d["date"])
    return days

if __name__ == "__main__":
    days = fetch_contributions()
    print(f"{len(days)} gün bulundu.")
    with open("data/contributions.json", "w") as f:
        json.dump(days, f, indent=2)
    print("data/contributions.json yazıldı.")
