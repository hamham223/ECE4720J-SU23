from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import numpy as np
from numpy import ndarray
import pandas as pd
import sqlite3

pathSimilarity = "/home/hadoopuser/project/artist_similarity.db"
pathSongArtist = "/home/hadoopuser/project/song_to_artist.db"
pathSimilarityFeature = "file:///home/hadoopuser/project/feature_similarity.csv"
pathSimilarityFeature1 = "/home/hadoopuser/project/feature_similarity.csv"

def artistNeighbor(artist: str) -> list:
    """given the input artist (string), return the list contain all neigh artists

    Args:
    ---
        artist (str): the artist id

    Returns:
    ---
        list: similar artists
    """
    con = sqlite3.connect(pathSimilarity)
    cursor = con.cursor()
    query = f"SELECT similar FROM similarity WHERE target=\"{artist}\""
    tmp = cursor.execute(query).fetchall()
    return [tup[0] for tup in tmp]

def getArtistSongs(artist: str) -> list:
    con = sqlite3.connect(pathSongArtist)
    cursor = con.cursor()
    query = f"SELECT title,track_id FROM songs WHERE artist_id=\"{artist}\""
    tmp = cursor.execute(query).fetchall()
    return [(tup[0], tup[1]) for tup in tmp]

def getSongArtist(song: str):
    con = sqlite3.connect(pathSongArtist)
    cursor = con.cursor()
    query = f"SELECT track_id,artist_id,artist_name FROM songs WHERE title=\"{song}\""
    tmp = cursor.execute(query).fetchall()
    return [tup[0] for tup in tmp], [tup[1] for tup in tmp], [tup[2] for tup in tmp]

def getFeatures(songIds: list, spark: SparkSession):
    features = []
    for songId in songIds:
        songId = f"b'{songId}'"
        command = f"SELECT Log_loudness,bar_num,beat_num,section_num,segment_num,tatum_num,duration,mode,end_of_fade_in,fade_out_time,proportion_fade_out,proportion_fade_in,tempo,time_signature,hotness,title,track_id,artist_name FROM data WHERE track_id=\"{songId}\""
        feature_df = spark.sql(command)
        feature = feature_df.toPandas().to_numpy()

        if len(np.shape(feature)) != 0:
            feature = feature[0, :]
            features.append((feature[:-3].astype(np.float64), (feature[-3], feature[-2], feature[-1])))

def calcDistance(song1: tuple, song2: ndarray):

    return (np.dot(song1[0], song2) / (np.linalg.norm(song1[0]) * np.linalg.norm(song2)) - np.sum(np.abs(song1[0]-song2)), song1[1])

def compare(song1: str, song2: str) -> str:
    dis1 = calcDistance(song1, 'Silent Night')
    dis2 = calcDistance(song2, 'Silent Night')
    return (song2 if dis1 < dis2 else song1)

def merge_lists(list1, list2):
    return list(set(list1 + list2))

if __name__ == "__main__":
    # This is the input artist

    conf = SparkConf().setAppName("breadth first search")
    sc = SparkContext(conf=conf)
    spark: SparkSession = SparkSession(sc)
    
    songName = input("Please enter the name of a song: ")
    

    songId, artists, artists_name = getSongArtist(songName)

    if len(artists_name) > 1:
        print("Too many songs have the same name! Please choose a specific author from the list: ")
        print(artists_name)
        artist_name = input("The author of your song: ")
        if not artist_name in artists_name:
            print("No this author!")
            exit(0)
        index = artists_name.index(artist_name)
        artists = [artists[index]]
        songId = songId[index]
    elif len(artists_name) == 1:
        artist_name = artists_name[0]
        songId = songId[0]
    elif len(artists_name) == 0:
        print(f"No song named {songName}.")
        exit(0)

    print(f"The song you choose: ")
    print(f"Name: {songName}, Author: {artist_name}, Id: {songId}")

    depth = int(input("Please enter the depth of the BFS: "))

    for i in range(depth):
        artists += sc.parallelize(artists, 4).map(artistNeighbor).reduce(merge_lists)
        print(f"Num of similar artists in the {i+1}th layer: {len(artists)}.")
    
    songs: list = sc.parallelize(artists, 12).map(getArtistSongs).reduce(merge_lists)
    if (songName, songId) in songs:
        songs.remove((songName, songId))
    songs = [tup[1] for tup in songs]
    print(f"Num of similar songs: {len(songs)}.")
    songs = sc.parallelize(songs, 100).map(lambda x: f"b'{x}'").collect()

    # find the feature of the input song
    feature_df = pd.read_csv(pathSimilarityFeature)
    features = feature_df[feature_df['track_id'].isin(songs)].to_numpy()
    features = sc.parallelize(features, 100).map(lambda x: (np.concatenate((x[1:2], x[3:-7])).astype(np.float64), (x[-6],x[-5],x[-1]))).collect()
    
    songId = f"b'{songId}'"
    songFeature = feature_df[feature_df['track_id']==songId].to_numpy()[0]
    songFeature = np.concatenate((songFeature[1:2], songFeature[3:-7])).astype(np.float64)

    if len(songFeature) == 0:
        print("This song is not include in the feature!")
        exit(0)

    result = sc.parallelize(features, 100).map(lambda x: calcDistance(x, songFeature)).reduce(lambda x, y: max(x, y))

    print(result)

    