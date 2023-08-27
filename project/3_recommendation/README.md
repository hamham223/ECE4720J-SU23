# Big Data Recommendation

## Method 1: MapReduce

### How to run

```bash
cd MapReduce
time bash ./driver.sh
```

### Function of each python file
+ `mapper_artist.py`: given an artist id as input, find all the similar artists (according to the database)
+ `mapper_song.py`: given the similar artists, find all of their songs
+ `mapper_distance.py`: given the list of songs, calculate their cosine similarity from the given song
+ `reducer.py`: find the song with largest similarity

### Performance
```bash
+ hdfs dfs -cat /project_distance/part-00000
('Story Of Two', 'TRMHEEB12903C9F3C9', 0.9140447260983122)

real    4m18.674s
user    1m27.983s
sys     0m5.830s
```

## Method 2: Spark

### How to run (local)

```bash
cd Spark
time python3 bfs.py < input.txt
```
The sample `input.txt`:
```
500 Miles
Sim Redmond Band
2
```
+ The first line is the song name
+ The second line is the artist name
+ The third line is bfs depth

### Performance

```bash
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
Please enter the name of a song: Too many songs have the same name! Please choose a specific author from the list: 
['Bad Astronaut', 'Rosanne Cash', 'Judee Sill', 'Sim Redmond Band', 'Bob The Builder']
The author of your song: The song you choose: 
Name: 500 Miles, Author: Sim Redmond Band, Id: TRLYPBY128F933FB09
Num of similar artists in the 1th layer: 41.                                    
Num of similar artists in the 2th layer: 868.
Num of similar songs: 30489.                                                    
(0.938496722499255, ("b'Down'", "b'TRJPUIN128F93305B6'", "b'Stroke 9'"))        

real    0m17.739s
user    0m4.210s
sys     0m1.872s
```

That is **15** times speed up!
