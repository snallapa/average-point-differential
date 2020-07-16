def calculate_apd(game_stats):
    total_time = game_stats["total_time"]
    scores = game_stats["scores"]
    away, home = scores[0]["score"].keys()
    total_pd = 0.0
    for x in range(len(scores) - 1):
        deltatime = scores[x + 1]["time"] - scores[x]["time"]
        s1, s2 = scores[x]["score"].values()
        delta = s1 - s2
        total_pd += deltatime * delta
    # last score
    s1, s2 = scores[-1]["score"].values()
    delta = s1 - s2
    total_pd += (total_time - scores[-1]["time"]) *  delta
    apd = total_pd / total_time
    return {away: apd, home: -apd}
