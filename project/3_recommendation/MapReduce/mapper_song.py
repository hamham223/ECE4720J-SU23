#!/usr/bin/python3.8

import sys
import sqlite3

pathSongArtist = "/home/hadoopuser/project/song_to_artist.db"

def getArtistSongs(artist: str) -> list:
    con = sqlite3.connect(pathSongArtist)
    cursor = con.cursor()
    query = f"SELECT title,track_id FROM songs WHERE artist_id=\"{artist}\""
    tmp = cursor.execute(query).fetchall()
    return [(tup[0], tup[1]) for tup in tmp]
    
for line in sys.stdin:
    line = line.strip("\n").split(",")
    # each line is a list of artist id
    for artist in line:
        res = getArtistSongs(artist)
        for art in res:
            print(f"{art[0]}|{art[1]}")