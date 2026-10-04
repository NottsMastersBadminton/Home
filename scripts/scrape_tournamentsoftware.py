import requests
from bs4 import BeautifulSoup
import json

TEAM_URLS = {
    "O40": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=270",
    "O45": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=271",
    "O50": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=272",
    "O55": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=273",
    "O60": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=274",
    "O65": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=357",
    "O70": "https://be.tournamentsoftware.com/sport/league/team?id=62981C29-4B09-4F3D-841D-8403F6E79821&team=411"
}

def fetch(url):
    return BeautifulSoup(
        requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text,
        "html.parser"
    )

def scrape():
    data = {
        "fixtures": [],
        "results": [],
        "teams": [],
        "league": []
    }

    for team_name, url in TEAM_URLS.items():
        soup = fetch(url)

        # TEAM PLAYERS
        players = [
            li.get_text(strip=True)
            for li in soup.select("ul.team-players li")
        ]

        data["teams"].append({
            "name": team_name,
            "players": players
        })

        # FIXTURES & RESULTS
        for row in soup.select("table.team-matches tr"):
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) < 5:
                continue

            date, opponent, venue, score, _ = cols

            if score == "":
                data["fixtures"].append({
                    "date": date,
                    "team": team_name,
                    "opponent": opponent,
                    "venue": venue
                })
            else:
                data["results"].append({
                    "date": date,
                    "team": team_name,
                    "opponent": opponent,
                    "score": score
                })

        # LEAGUE TABLE
        league_rows = soup.select("table.league-table tr")
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

    # SAVE JSON
    with open("Home/data/dashboard.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Dashboard JSON updated.")

if __name__ == "__main__":
    scrape()
