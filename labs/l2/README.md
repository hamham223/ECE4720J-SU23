# ECE4720J Lab2

> Author: :crossed_swords: :car: :hamster::palm_tree:

### Ex 2

1. ```python
   #!/usr/bin/env python3
   FirstnameTime = 5000
   LastnameTime = 80000
   totalNames = 100000000 # modify here to change the total number of records
   
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
   	genCsv("records.csv")
   except Exception as error:
      	logger.exception(error)
   ```
   
   Then upload the `records.csv` onto hdfs:

   ```bash
   hdfs dfs -put ./records.csv /
   ```
   
2. ```python
   #!/usr/bin/env python3
   import sys
   
   for i in sys.stdin:
   	parts = i.strip().split(",")
   	print(parts[1]+"\t"+parts[2])
   ```

3. ```python
   #!/usr/bin/env python3
   import sys
   from operator import itemgetter
   
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
   ```

4. We use the hadoop streaming tool

   ```bash
   hadoop jar \
   	$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar \
   	-file mapper.py \
   	-file reducer.py \
   	-mapper "python3 mapper.py" \
   	-reducer "python3 reducer.py" \
   	-input /records.csv \
   	-output /output
   ```

   