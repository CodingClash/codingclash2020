# Affects how fast ratings change; higher value -> faster changes
K = 20

def win_probability(winner_elo, loser_elo):
	return 1.0 / (1 + (10 ** ((loser_elo - winner_elo) / 400)))

def update_elo(red_team, blue_team, outcome):
	red_elo = red_team.elo
	blue_elo = blue_team.elo
	red_probability = win_probability(red_elo, blue_elo)
	blue_probability = win_probability(blue_elo, red_elo)

	if outcome == "Red":
		red_elo += K * (1 - red_probability)
		blue_elo += K * (0 - blue_probability)

	else:
		red_elo += K * (0 - red_probability)
		blue_elo += K * (1 - blue_probability)

	red_team.elo = red_elo
	blue_team.elo = blue_elo