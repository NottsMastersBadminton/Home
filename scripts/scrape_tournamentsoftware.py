import requests
from bs4 import BeautifulSoup
import json

URL = "https://be.tournamentsoftware.com/sport/clubteams.aspx?id=62981C29-4B09-4F3D-841D-8403F6E79821&cid=26"

def scrape():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    data = {
        "fixtures": [],
        "results": [],
        "teams": [],
        "league": []
    }

    # -------------------------
    # Fixtures & Results
    # -------------------------
    rows = soup.select("table.clubteams-table tr")

    for row in rows:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 5:
            continue

        date, team, opponent, venue, score = cols

        if score == "":
            data["fixtures"].append({
                "date": date,
                "team": team,
                "opponent": opponent,
                "venue": venue
            })
        else:
            data["results"].append({
                "date": date,
                "team": team,
                "opponent": opponent,
                "score": score
            })

    # -------------------------
    # Teams (simple list)
    # -------------------------
    team_panels = soup.select(".clubteams-team")
    for panel in team_panels:
        name = panel.select_one("h3").get_text(strip=True)
        players = [li.get_text(strip=True) for li in panel.select("li")]
        data["teams"].append({"name": name, "players": players})

    # -------------------------
    # League Table
    # -------------------------
    league_rows = soup.select("table.clubteams-league tr")

    for row in league_rows[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if len(cols) < 5:
            continue

        team, played, won, lost, points = cols
        data["league"].append({
            "team": team,
            "played": int(played),
            "won": int(won),
            "lost": int(lost),
            "points": int(points)
        })

    # -------------------------
    # Save JSON
    # -------------------------
    with open("Home/data/dashboard.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Dashboard JSON updated.")

if __name__ == "__main__":
    scrape()
