#!/usr/bin/bash

set -ex

echo "Deleting existing files! Win?"

hdfs dfs -rm -r -f /project_artists 
hdfs dfs -rm -r -f /project_songs 
hdfs dfs -rm -r -f /project_distance

STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.2.2.jar"

# The first mapper create a list of artist ids
echo "Runing the first mapper (mapper_artist.py)"
hadoop jar ${STREAMING_JAR} \
-input /testfile.txt \
-file /home/hadoopuser/project/*.db \
-file *.py \
-mapper "./mapper_artist.py | ./mapper_artist.py" \
-reducer "/bin/cat" \
-output /project_artists

hdfs dfs -get /project_artists/part-00000
mv ./part-00000 artists.txt
hdfs dfs -rm -f /artists.txt
hdfs dfs -put artists.txt /
rm -f artists.txt

# The second mapper return a file containing songs
echo "Runing the second mapper (mapper_song.py)"
hadoop jar ${STREAMING_JAR} \
-input /artists.txt \
-file /home/hadoopuser/project/*.db \
-file *.py \
-mapper "./mapper_song.py" \
-reducer "/bin/cat" \
-output /project_songs

hdfs dfs -get /project_songs/part-00000
mv ./part-00000 songs.txt
hdfs dfs -rm -f /songs.txt
hdfs dfs -put songs.txt /
rm -f songs.txt

# The third mapper calculate the distance and reduce (min)
echo "Runing the third mapper (mapper_distance.py)"
hadoop jar ${STREAMING_JAR} \
-input /songs.txt \
-file *.py \
-mapper "./mapper_distance.py" \
-reducer "./reducer.py" \
-output /project_distance

hdfs dfs -cat /project_distance/part-00000

