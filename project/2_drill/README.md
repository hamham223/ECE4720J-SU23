# Drill Database Query

### Objective

In this milestone, we used drill to perform simple database queries, including:

+ Find the range of dates covered by the songs in the dataset, i.e. the age of the oldest and of the youngest songs
+ Find the hottest song that is the shortest and has the highest energy with the lowest tempo.
+ Find the name of the album with the most tracks.
+ Find the name of the band(artists) who recorded the longest song.

### Detailed Solution

#### 0. preparation

```sqlite
-- read avro file from local file system (~100M)
create table dfs.tmp.`songs` as select * from dfs.`F:/avro/songs.avro`;
-- change path
use dfs.tmp;
```

#### 1. the oldest and youngest songs

```sqlite
select max(year_end) from songs where year_end > 0;
+--------+ 
| EXPR$0 |
+--------+
| 2011   |
+--------+                                                                      
1 row selected (0.321 seconds)

select min(year_end) from songs where year_end > 0;              
+--------+
| EXPR$0 |
+--------+
| 1922   |
+--------+
1 row selected (0.323 seconds)
```

Therefore, the dataset covered songs from $1922$ to $2011$, namely the age of the songs vary from $12$ years to $101$ years.

#### 2. the hottest, shortest, highest energy, lowest tempo

```sqlite
select id, title from songs 
where hotness <> 'NaN'
order by hotness desc, duration asc, energy desc, tempo asc
limit 5;

+--------------------+-----------------------------------+
|         id         |               title               | 
+--------------------+-----------------------------------+
| SONASKH12A58A77831 | Jingle Bell Rock                  |
| SOAVJBU12AAF3B370C | Rockin' Around The Christmas Tree |
| SOEWAKD12AB01860D5 | Holiday                           |
| SOAAXAK12A8C13C030 | Immigrant Song (Album Version)    |
| SOAXLDX12AC468DE36 | La Tablada                        |
+--------------------+-----------------------------------+
5 rows selected (0.497 seconds) 
```

Therefore, `Jingle Bell Rock` is the song the hottest song that is the shortest and shows highest energy with lowest tempo.

#### 3. the album with the most songs

```sql
select album_id, album_name, count(album_id) as numSongs from songs
group by album_id, album_name
order by numSongs desc
limit 5;

+----------+---------------------------------------------------+----------+
| album_id |                    album_name                     | numSongs |
+----------+---------------------------------------------------+----------+
| 60509    | First Time In A Long Time: The Reprise Recordings | 85       |
| 314748   | The Twilight Zone                                 | 81       |
| 592093   | Keep An Eye On The Sky                            | 77       |
| 71437    | The Complete Mercury Recordings                   | 75       |
| 682543   | Grind Madness at the BBC                          | 74       |
+----------+---------------------------------------------------+----------+
5 rows selected (1.076 seconds) 
```

Therefore, `First Time In A Long Time: The Reprise Recordings` the album with most tracks. Indeed, it has 4CDs and 80+ tracks.

###### reference

> https://www.discogs.com/release/4483625-Fanny-First-Time-In-A-Long-Time-The-Reprise-Recordings

#### 4. the band with longest song

```sqlite
select artist_name, title, duration from songs order by duration desc limit 1;                                     
+--------------------------------+------------+-----------+
|          artist_name           |   title    | duration  |
+--------------------------------+------------+-----------+ 
| Mystic Revelation of Rastafari | Grounation | 3034.9058 | 
+--------------------------------+------------+-----------+  
1 row selected (0.468 seconds) 
```

Therefore, the band `Mystic Revelation of Rastafari` has recorded `Grounation` which has highest duration.
