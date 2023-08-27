#!/usr/bin/python3.8

import sys
import sqlite3
import math

similarityFeaturePath = "/home/hadoopuser/project/feature.db"
song_track_id = "b'TRYESJS12903CDF730'"
song_name = 'Old Man Mose'
artist_name = 'The Bristols'

def getFeature(track_id: str):
    con = sqlite3.connect(similarityFeaturePath)
    cursor = con.cursor()
    query = f"SELECT Log_loudness,bar_num,beat_num,section_num,segment_num,tatum_num,duration,mode,end_of_fade_in,fade_out_time,\
          proportion_fade_out,proportion_fade_in,tempo,time_signature, hotness FROM feature WHERE track_id=\"{track_id}\""
    try:
        feature = list(cursor.execute(query).fetchall()[0])
    except:
        return None
    return [float(i) if i!='' else float(0) for i in feature]

song_feature = getFeature(song_track_id)

def Mul(v1: list, v2: list) -> float:
    res = 0
    for i in range(len(v1)):
        res += v1[i] * v2[i]
    return res

def Sum(v: list):
    res = 0
    for i in v:
        res += i
    return res

def absSub(v1: list, v2: list):
    res = []
    for i in range(len(v1)):
        res.append(abs(v1[i] - v2[i]))
    return res

def Norm(v: list) -> float:
    res = Mul(v, v)
    return math.sqrt(res)

def calcDistance(v1: list, v2: list) -> float:

    return Mul(v1, v2) / (Norm(v1) * Norm(v2)) - Sum(absSub(v1, v2))
    # return np.dot(song1, song2) / (np.linalg.norm(song1) * np.linalg.norm(song2)) - np.sum(np.abs(song1-song2))

for line in sys.stdin:
    line = line.strip("\n").strip("\t").split("|")
    track_id_i = f"b'{line[1]}'"
    # each line is a list of artist id
    feature_i = getFeature(track_id_i)
    if feature_i:
        res = calcDistance(song_feature, feature_i)
    else:
        continue
    print(f"{line[0]}|{line[1]}|{res}")