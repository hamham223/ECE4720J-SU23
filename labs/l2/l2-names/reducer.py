#!/usr/bin/env python3
import sys

id = ""
maxscore = 0
for inp in sys.stdin:
	parts = inp.strip().split("\t")
	a = parts[0]
	b = parts[1]
	#a,b = inp.split("\t")
	if not(a==id):
		if not (id == ""):
			print(id +"\t"+ str(maxscore))
		id = a
		maxscore = int(b)
	else:
		if (int(b) > maxscore):
			maxscore = int(b)
