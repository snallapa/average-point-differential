import requests
from bs4 import BeautifulSoup

QUARTER = 15 * 60

API = "https://www.pro-football-reference.com"

def score_col(score, column):
    return score.find(**{"data-stat": column})

def scores(url):
    source = requests.get(url)

    soup = BeautifulSoup(source.text,"lxml")

    # wtf why
    ot = BeautifulSoup(soup.find(id="all_pbp").contents[-2].string, "lxml")
    is_ot = ot.find(string="Overtime")
    if is_ot:
        ot_time = score_col(ot.find(string="Overtime").parent.parent.next_sibling.next_sibling.next_sibling.next_sibling, "qtr_time_remain")
        m, _ = ot_time.a.text.split(":")
        OT_TIME = int(m) * 60


    scoring_table = soup.find("table", id="scoring")
    visiting_team = score_col(scoring_table.find("thead"), "vis_team_score").text
    home_team = score_col(scoring_table.find("thead"), "home_team_score").text
    scores = scoring_table.find("tbody").find_all("tr")
    quarter = "1"
    all_scores = []
    for score in scores:
        q = score_col(score, "quarter").text
        if q:
            quarter = q
        scored_time = score_col(score, "time").text
        if quarter == "OT":
            scored_time_m, scored_time_s = scored_time.split(":")
            time = 4 * QUARTER + (OT_TIME - (int(scored_time_m) * 60 + int(scored_time_s)))
        else:
            scored_time_m, scored_time_s = scored_time.split(":")
            time = (int(quarter) - 1) * QUARTER + (QUARTER - (int(scored_time_m) * 60 + int(scored_time_s)))
        visiting_score = int(score_col(score, "vis_team_score").text)
        home_score = int(score_col(score, "home_team_score").text)
        all_scores.append({
            "quarter": quarter,
            "time": time,
            "score": {
                visiting_team: visiting_score,
                home_team: home_score
            }
        })
    # wtf why
    stats = BeautifulSoup(soup.find(id="all_team_stats").contents[-2].string,"lxml")
    time_possession = stats.find(id="team_stats").find("tbody").find_all("tr")[-1].find_all("td")
    total_time = 0
    for pos in time_possession:
        time_string = pos.text
        m, s = time_string.split(":")
        total_time += int(m) * 60 + int(s)
    return {
        "total_time": total_time,
        "scores": all_scores
    }

def linkify(l):
    return API + l

def get_games(week, season="2019"):
    url = f"https://www.pro-football-reference.com/years/{season}/week_{week}.htm"
    source = requests.get(url)
    soup = BeautifulSoup(source.text,"lxml")
    games = soup.find_all(class_="game_summary")
    game_links = []
    for game in games:
        game_links.append(linkify(game.find(class_="teams").find("tbody").find(class_="gamelink").find("a")["href"]))
    return game_links