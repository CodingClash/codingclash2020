def in_between(pointa, pointb, pointc):

	dx = pointb[0]-pointa[0]
	dy = pointb[1]-pointa[1]

	linex = lambda x: pointa[1]+dy/dx*x

	if (linex(pointc[0])<=pointc[1] and linex(pointc[0])+1>pointc[1]) or (linex(pointc[0])>=pointc[1] and linex(pointc[0])+1<pointc[1]):
		return True

	return False

