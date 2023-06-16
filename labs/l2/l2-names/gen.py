#!/usr/bin/env python3
FirstnameTime = 5000
LastnameTime = 80000
totalNames = 50000000

from random import randint
from loguru import logger
from tqdm import tqdm

def readNames(fname:str, linenum:int):
	names = []
	with open(fname, 'r') as file:
		for i in range(linenum):
			line = file.readline()
			if not line:
				break
			names.append(line.strip())
	return names

def genID():
	id = ""
	for i in range(10):
		id = id + str(randint(0,9))
	return id

def genCsv(fname):
	firstnames = readNames("firstnames.txt",FirstnameTime)
	lastnames = readNames("lastnames.txt",LastnameTime)
	with open(fname, 'w') as file:
		for i in tqdm(range(totalNames)):
			name = firstnames[randint(0,FirstnameTime-1)] + " " + lastnames[randint(0,LastnameTime-1)]
			id = genID()
			scoreNum = randint(3,5)
			for j in range(scoreNum):
				score = str(randint(0,100))
				file.write(name+","+id+","+score+"\n")

try:
	genCsv("./records_50m.csv")
except Exception as error:
   	logger.exception(error)

				
