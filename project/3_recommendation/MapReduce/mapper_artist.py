#!/usr/bin/python3.8

import sys
import sqlite3

pathSimilarity = "/home/hadoopuser/project/artist_similarity.db"


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
    
for line in sys.stdin:
     line = line.strip("\n").strip("\t").split(",")
     # each line is a list of artist id
     for artist in line:
          res = artistNeighbor(artist)
          outputline = ""
          for art in res:
               outputline += f"{art},"
          print(outputline[:-1])
