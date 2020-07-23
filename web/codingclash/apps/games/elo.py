# Affects how fast ratings change; higher value -> faster changes
K = 20

def win_probability(winner_elo, loser_elo):
	return 1.0 / (1 + (10 ** ((loser_elo - winner_elo) / 400)))

def update_elo(elo1, elo2, winner):
	red_probability = win_probability(elo1, elo2)
	blue_probability = win_probability(elo1, elo2)

	if winner == 1:
		elo1 += K * (1 - red_probability)
		elo2 += K * (0 - blue_probability)

	else:
		elo1 += K * (0 - red_probability)
		elo2 += K * (1 - blue_probability)

	return elo1, elo2
