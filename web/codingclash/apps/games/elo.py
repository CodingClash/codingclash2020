# Affects how fast ratings change; higher value -> faster changes
K = 20

def win_probability(winner_elo, loser_elo):
	return 1.0 / (1 + (10 ** ((loser_elo - winner_elo) / 400)))

def update_elo(elo1, elo2, winner):
	probability1 = win_probability(elo1, elo2)
	probability2 = win_probability(elo2, elo1)

	if winner == 1:
		elo1 += K * (1 - probability1)
		elo2 += K * (0 - probability2)
	else:
		elo1 += K * (0 - probability1)
		elo2 += K * (1 - probability2)

	return elo1, elo2
